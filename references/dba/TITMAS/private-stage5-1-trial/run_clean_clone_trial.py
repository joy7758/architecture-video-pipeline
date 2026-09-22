#!/usr/bin/env python3
"""Run the deterministic Stage 5.1 clean-clone trial against the core Sandbox.

The trial client reads only the separately reconstructed repository. The core
controller starts the existing loopback-only Stage 5 Gateway and delivers one
ephemeral key in memory. No model or external Provider is called.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from validate_trial_repository import validate


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _run(
    args: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )


def _sha256(value: Any) -> str:
    raw = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode()
    return hashlib.sha256(raw).hexdigest()


def _prepare_sdk(venv: Path, clone: Path) -> Path:
    _run([sys.executable, "-m", "venv", str(venv)], cwd=clone)
    python = venv / "bin" / "python"
    _run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "--no-deps",
            "--no-index",
            str(
                clone
                / "sdk"
                / "python"
                / "titmas_private_trial_sdk-0.1.0-py3-none-any.whl"
            ),
        ],
        cwd=clone,
    )
    smoke = _run(
        [
            str(python),
            "-c",
            (
                "import titmas_stage5_sdk;"
                "print(titmas_stage5_sdk.Stage5Client.__name__)"
            ),
        ],
        cwd=clone,
    )
    if smoke.stdout.strip() != "Stage5Client":
        raise ValueError("installed SDK smoke failed")
    return python


def _installed_sdk(python: Path, clone: Path):
    location = _run(
        [
            str(python),
            "-c",
            "import titmas_stage5_sdk; print(titmas_stage5_sdk.__file__)",
        ],
        cwd=clone,
    ).stdout.strip()
    return _load(Path(location), "titmas_stage51_installed_sdk")


def _load_gateway(core_root: Path):
    gateway_root = (
        core_root / "TITMAS" / "private-customer-evaluation" / "gateway"
    )
    if str(gateway_root) not in sys.path:
        sys.path.insert(0, str(gateway_root))
    import stage5_service  # type: ignore

    return stage5_service


def run(
    core_root: Path,
    trial_repository: str,
    output_path: Path,
    *,
    expected_revision: str | None = None,
) -> dict[str, Any]:
    core_root = core_root.resolve()
    output_path = output_path.resolve()
    with tempfile.TemporaryDirectory(
        prefix="titmas-stage5-1-clean-clone-"
    ) as raw:
        root = Path(raw)
        clone = root / "trial"
        _run(["git", "clone", trial_repository, str(clone)], cwd=root)
        revision = _run(
            ["git", "rev-parse", "HEAD"], cwd=clone
        ).stdout.strip()
        if expected_revision and revision != expected_revision:
            raise ValueError("trial repository revision mismatch")
        package_validation = validate(clone)

        llms = (clone / "llms.txt").read_text(encoding="utf-8")
        agent_index = json.loads(
            (clone / "agent-index.json").read_text(encoding="utf-8")
        )
        task_catalog = json.loads(
            (clone / "tasks" / "trial-task-catalog.json").read_text(
                encoding="utf-8"
            )
        )
        examples = json.loads(
            (clone / "examples" / "synthetic-examples.json").read_text(
                encoding="utf-8"
            )
        )
        if "External trial requires explicit access: true" not in llms:
            raise ValueError("llms.txt current access boundary missing")
        if agent_index["public_core_clone_available"] is not False:
            raise ValueError("agent index core clone boundary drift")
        selected = task_catalog["tasks"][0]
        if selected["task_id"] != "TRIAL-01-NEGATIVE-TEST-VECTOR":
            raise ValueError("deterministic trial task discovery drift")

        venv = root / "venv"
        python = _prepare_sdk(venv, clone)
        sdk = _installed_sdk(python, clone)
        gateway_module = _load_gateway(core_root)
        ids = iter(
            (
                "stage5-submission-STAGE51-valid-negative",
                "stage5-submission-STAGE51-invalid-vector",
            )
        )
        gateway = gateway_module.Stage5GatewayService(
            core_root,
            store=gateway_module.ContributionStore(
                id_factory=lambda: next(ids)
            ),
            principal_ref="zhangbin",
            agent_ref="STAGE5-1-PROGRAMMATIC-TRIAL",
            contributor_kind="PROGRAMMATIC",
        )
        endpoint = gateway.start()
        try:
            client = sdk.Stage5Client(
                endpoint,
                gateway.session.token,
                clone / "schemas",
            )
            catalog_result = client.get_standard_catalog()
            remote_tasks = client.get_tasks()

            valid = json.loads(json.dumps(examples["test_vector"]))
            valid["vector_id"] = "STAGE5-VECTOR-STAGE51-VALID-NEGATIVE"
            valid_status = client.submit_test_vector(valid)
            valid_result = client.validate_submission(
                valid_status["submission_id"]
            )
            if (
                valid_result["conformance_status"] != "CONFORMANCE_PASS"
                or valid_result["human_disposition_required"] is not True
            ):
                raise ValueError("valid negative Test Vector did not pass")

            invalid = json.loads(json.dumps(valid))
            invalid["vector_id"] = "STAGE5-VECTOR-STAGE51-INVALID"
            invalid["failure_classification"] = "NONE"
            invalid_status = client.submit_test_vector(invalid)
            invalid_http_status = 200
            try:
                client.validate_submission(invalid_status["submission_id"])
                invalid_result = {"conformance_status": "UNEXPECTED_PASS"}
            except sdk.TITMASClientError as exc:
                invalid_http_status = exc.status
                invalid_result = client.get_submission_result(
                    invalid_status["submission_id"]
                )
            if (
                invalid_http_status != 422
                or invalid_result["conformance_status"]
                != "CONFORMANCE_FAIL"
            ):
                raise ValueError("invalid Test Vector did not fail closed")

            fixture = (
                clone / "trial" / "programmatic-contribution-fixture.json"
            )
            fixture.write_text(
                json.dumps(valid, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            changed = _run(
                ["git", "status", "--porcelain"], cwd=clone
            ).stdout.strip().splitlines()
            if changed != [
                "?? trial/programmatic-contribution-fixture.json"
            ]:
                raise ValueError("PR fixture scope is not exactly one file")
        finally:
            gateway.stop()

        result = {
            "report_type": "TITMAS_STAGE5_1_PROGRAMMATIC_CLEAN_CLONE_TRIAL",
            "report_version": "1.0",
            "run_at": datetime.now(timezone.utc).isoformat().replace(
                "+00:00", "Z"
            ),
            "trial_repository": "joy7758/titmas-private-developer-trial",
            "trial_revision": revision,
            "private_trial_clean_clone": "PASS",
            "trial_sdk_install": "PASS",
            "trial_task_discovery": "PASS",
            "selected_task": selected["task_id"],
            "trial_contribution_preflight": "PASS",
            "trial_sandbox_submission": "PASS",
            "trial_conformance_result": "PASS",
            "invalid_test_vector": "CONFORMANCE_FAIL",
            "invalid_test_vector_http_status": invalid_http_status,
            "pr_fixture_prepared": True,
            "pr_fixture_committed": False,
            "pr_fixture_pushed": False,
            "standard_catalog_entries": len(
                catalog_result["specifications"]
            ),
            "sandbox_task_entries": len(remote_tasks["tasks"]),
            "trial_task_entries": len(task_catalog["tasks"]),
            "package_validation": package_validation,
            "core_access_count": 0,
            "real_model_call_count": 0,
            "real_provider_call_count": 0,
            "external_participant_invitation_authorized": False,
            "external_developer_trial_executed": False,
            "limitations": [
                "DETERMINISTIC_PROGRAMMATIC_TRIAL_ONLY",
                "CORE_CONTROLLER_HOSTED_EXISTING_LOOPBACK_GATEWAY",
                "NO_EXTERNAL_PARTICIPANT",
                "CONFORMANCE_NE_STANDARD_ADOPTION",
            ],
        }
        result["report_sha256"] = _sha256({
            key: value for key, value in result.items()
            if key != "report_sha256"
        })
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        os.chmod(output_path, 0o600)
        return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--core-root", type=Path, required=True)
    parser.add_argument("--trial-repository", required=True)
    parser.add_argument("--expected-revision")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(
        run(
            args.core_root,
            args.trial_repository,
            args.output,
            expected_revision=args.expected_revision,
        ),
        indent=2,
        sort_keys=True,
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
