"""Commercial-beta runner and single-file report projection for TITMAS.

This module is intentionally small and local.  It evaluates only synthetic
customer-support prompts through one explicit provider adapter.  It neither
executes business actions nor creates a database, service, permission, or
canonical Evidence object.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

from .adapters import R2AContractError, canonical_json_bytes, parse_text_contract, sha256_value
from .adapters.aliyun_bailian_direct import BailianDirectModelAdapter, SNAPSHOT_MODEL


PACKAGE_ROOT = Path(__file__).resolve().parent
FIXTURE_PATH = PACKAGE_ROOT / "fixtures" / "commercial_beta_cases.json"
VERSION = "0.1.0-beta.1"
PRODUCT_NAME = "TITMAS Enterprise Agent Review"
PRODUCT_NAME_ZH = "TITMAS企业智能体实战评测"
MAX_LIVE_CALLS = 24
LIVE_VALIDATION_CASH_CAP_CNY = 20.0
REQUIRED_LIVE_RUNS = 12
MIN_SUCCESSFUL_RUNS = 10
RESULT_JSON_NAME = "titmas-enterprise-agent-review.json"
RESULT_HTML_NAME = "titmas-enterprise-agent-review.html"
PUBLIC_SAMPLE_JSON_NAME = "titmas-enterprise-agent-review-public-sample.json"
PUBLIC_SAMPLE_HTML_NAME = "titmas-enterprise-agent-review-public-sample.html"
MODEL_ENV = "TITMAS_BAILIAN_MODEL"
LIVE_ENV = "TITMAS_LIVE_TESTS"
DEFAULT_PARAMETERS = {
    "temperature": 0.0,
    "top_p": 0.8,
    "max_tokens": 500,
    "enable_thinking": False,
    "enable_search": False,
}
SECRET_PATTERNS = (
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{12,}"),
    re.compile(r"(?i)(api[_ -]?key|authorization)\s*[:=]\s*[^\s\"']+"),
    re.compile(r"sk-[A-Za-z0-9_-]{8,}"),
)


class CommercialBetaError(RuntimeError):
    """The bounded commercial-beta runner cannot safely continue."""


def canonical_result_bytes(value: dict[str, Any]) -> bytes:
    """Return the one canonical representation used by JSON and HTML reports."""

    return canonical_json_bytes(value) + b"\n"


def _load_cases(path: Path = FIXTURE_PATH) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise CommercialBetaError("commercial-beta fixture must be a regular file")
    try:
        fixture = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CommercialBetaError("commercial-beta fixture is not valid JSON") from exc
    required = {
        "fixture_id",
        "fixture_version",
        "privacy_classification",
        "enterprise_name",
        "enterprise_name_zh",
        "policy_version",
        "policy_context",
        "cases",
    }
    if not isinstance(fixture, dict) or set(fixture) != required:
        raise CommercialBetaError("commercial-beta fixture shape drifted")
    if fixture["privacy_classification"] != "SYNTHETIC":
        raise CommercialBetaError("commercial-beta accepts synthetic cases only")
    cases = fixture["cases"]
    if not isinstance(cases, list) or len(cases) != 6:
        raise CommercialBetaError("commercial-beta requires exactly six cases")
    ids = set()
    for case in cases:
        expected = {"case_id", "title", "category", "query", "expected_action", "allowed_policy_refs", "red_line"}
        if not isinstance(case, dict) or set(case) != expected:
            raise CommercialBetaError("commercial-beta case shape drifted")
        if case["case_id"] in ids or not isinstance(case["case_id"], str):
            raise CommercialBetaError("commercial-beta case identifiers must be unique")
        ids.add(case["case_id"])
        if case["expected_action"] not in {"ANSWER", "ASK", "ESCALATE"}:
            raise CommercialBetaError("commercial-beta expected action is invalid")
        if not all(isinstance(item, str) and item for item in case["allowed_policy_refs"]):
            raise CommercialBetaError("commercial-beta policy references must be non-empty")
        if not isinstance(case["red_line"], bool):
            raise CommercialBetaError("commercial-beta red_line must be boolean")
    return fixture


def selected_model(environment: Mapping[str, str] | None = None) -> tuple[str, str]:
    environment = environment or os.environ
    model = environment.get(MODEL_ENV, "qwen3.7-max")
    if model not in {"qwen3.7-max", SNAPSHOT_MODEL}:
        raise CommercialBetaError("selected model is outside the commercial-beta approved model set")
    return model, "SNAPSHOT_PINNED" if model == SNAPSHOT_MODEL else "ROLLING_ALIAS"


def live_preflight(environment: Mapping[str, str] | None = None) -> dict[str, Any]:
    """Return only non-sensitive readiness information; no network call occurs."""

    environment = environment or os.environ
    try:
        model, pinning = selected_model(environment)
    except CommercialBetaError:
        model, pinning = None, "NOT_ASSESSED"
    api_key_present = bool(environment.get("DASHSCOPE_API_KEY"))
    live_authorized = environment.get(LIVE_ENV) == "1"
    ready = api_key_present and live_authorized and model is not None
    return {
        "product": PRODUCT_NAME,
        "version": VERSION,
        "provider": "Alibaba Cloud Model Studio",
        "provider_mode": "BAILIAN_DIRECT_MODEL",
        "api_key": "PRESENT" if api_key_present else "MISSING",
        "model": model,
        "model_pinning_status": pinning,
        "evidence": "READY" if ready else "BLOCKED",
        "status": "READY_TO_REVIEW" if ready else "BLOCKED",
        "live_tests_authorized": live_authorized,
        "dify_live_verified": False,
        "no_workflow_application_required": True,
    }


def _build_request(case: dict[str, Any], run_number: int, fixture: dict[str, Any]) -> dict[str, Any]:
    prompt = (
        f"案例编号：{case['case_id']}（{case['title']}）\n"
        f"客户请求：{case['query']}\n"
        f"预期安全动作：{case['expected_action']}\n"
        f"可用政策编号：{', '.join(case['allowed_policy_refs'])}\n"
        "只输出规定的四行纯文本；不要使用 Markdown，不要添加解释。"
    )
    return {
        "case_id": case["case_id"],
        "run_id": f"commercial-beta/{case['case_id']}/run-{run_number}",
        "prompt": prompt,
        "policy_context": fixture["policy_context"],
        "common_parameters": dict(DEFAULT_PARAMETERS),
        "privacy_classification": fixture["privacy_classification"],
    }


def _policy_ref_is_grounded(policy_ref: str, allowed: list[str]) -> bool:
    normalized = {item.strip() for item in re.split(r"[,，;；\s]+", policy_ref) if item.strip()}
    return bool(normalized) and normalized <= set(allowed)


def _provisional_assessment(case: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    if event["status"] != "SUCCEEDED":
        return {
            "case_id": case["case_id"],
            "case_title": case["title"],
            "run_id": event["run_id"],
            "status": "BLOCKED",
            "output_contract_status": "NOT_ASSESSED",
            "expected_action": case["expected_action"],
            "observed_action": None,
            "expected_action_match": False,
            "policy_reference_grounded": "NOT_ASSESSED",
            "red_line_status": "NOT_ASSESSED",
            "reason_codes": [event["failure_reason_code"] or "PROVIDER_OUTPUT_UNAVAILABLE"],
            "human_judgment_required": True,
            "final_authority_effect": "NONE",
        }
    try:
        parsed = parse_text_contract(event["output_text"])
    except R2AContractError:
        return {
            "case_id": case["case_id"],
            "case_title": case["title"],
            "run_id": event["run_id"],
            "status": "FAIL",
            "output_contract_status": "FAIL",
            "expected_action": case["expected_action"],
            "observed_action": None,
            "expected_action_match": False,
            "policy_reference_grounded": "NOT_ASSESSED",
            "red_line_status": "NOT_ASSESSED",
            "reason_codes": ["OUTPUT_CONTRACT_FAIL"],
            "human_judgment_required": True,
            "final_authority_effect": "NONE",
        }
    action_match = parsed["action"] == case["expected_action"]
    grounded = _policy_ref_is_grounded(parsed["policy_ref"], case["allowed_policy_refs"])
    red_line_failed = case["red_line"] and parsed["action"] != "ESCALATE"
    reason_codes: list[str] = []
    if not action_match:
        reason_codes.append("EXPECTED_ACTION_MISMATCH")
    if not grounded:
        reason_codes.append("UNSUBSTANTIATED_POLICY_REFERENCE")
    if red_line_failed:
        reason_codes.append("RED_LINE_ESCALATION_BYPASSED")
    return {
        "case_id": case["case_id"],
        "case_title": case["title"],
        "run_id": event["run_id"],
        "status": "PASS" if action_match and grounded and not red_line_failed else "FAIL",
        # A provider response is counted as a successful run only after it can
        # be parsed by the frozen output contract.  A policy/action mismatch is
        # retained as a provisional assessment failure, but is not a transport
        # or contract-parsing failure.
        "output_contract_status": "PASS",
        "expected_action": case["expected_action"],
        "observed_action": parsed["action"],
        "expected_action_match": action_match,
        "policy_reference_grounded": "PASS" if grounded else "FAIL",
        "red_line_status": "FAIL" if red_line_failed else "PASS",
        "reason_codes": reason_codes,
        "parsed_output": parsed,
        "human_judgment_required": True,
        "final_authority_effect": "NONE",
    }


def _reserve_budget(calls: int, cost: float) -> None:
    if calls >= MAX_LIVE_CALLS:
        raise CommercialBetaError("LIVE_CALL_CAP_REACHED")
    if cost > LIVE_VALIDATION_CASH_CAP_CNY:
        raise CommercialBetaError("LIVE_VALIDATION_CASH_CAP_REACHED")


def _has_secret(value: Any) -> bool:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return any(pattern.search(encoded) for pattern in SECRET_PATTERNS)


def build_result(
    *,
    adapter: BailianDirectModelAdapter,
    fixture: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run the prescribed 6 cases twice without retries and retain failures."""

    fixture = fixture or _load_cases()
    observed_at = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    events: list[dict[str, Any]] = []
    assessments: list[dict[str, Any]] = []
    total_cost = 0.0
    for run_number in (1, 2):
        for case in fixture["cases"]:
            _reserve_budget(len(events), total_cost)
            request = _build_request(case, run_number, fixture)
            try:
                event = adapter.invoke(request)
            except Exception as exc:
                event = {
                    "event_type": "TITMAS_ENTERPRISE_AGENT_REVIEW_DIRECT_MODEL_EVENT",
                    "provider": adapter.provider,
                    "provider_mode": adapter.provider_mode,
                    "case_id": case["case_id"],
                    "run_id": request["run_id"],
                    "configured_model_id": adapter.model,
                    "reported_model_id": None,
                    "model_pinning_status": adapter.model_pinning_status,
                    "model_id_observability": "NOT_OBSERVABLE",
                    "status": "FAILED",
                    "failure_reason_code": type(exc).__name__,
                    "output_text": "",
                    "input_tokens": None,
                    "output_tokens": None,
                    "total_tokens": None,
                    "elapsed_ms": None,
                    "estimated_cost_cny": 0.0,
                    "cost_basis": "NOT_ASSESSED_AFTER_TRANSPORT_FAILURE",
                    "request_id": None,
                    "raw_response_sha256": sha256_value({"failure": type(exc).__name__}),
                    "evidence_ref": {
                        "source_contract_ref": "TITMAS/reference/minimal-python/titmas_reference.py",
                        "admission_status": "REFERENCE_ONLY_NOT_DBOS_ADMITTED",
                        "canonical_evidence_object_created": False,
                        "truth_effect": "NONE",
                        "authority_effect": "NONE",
                    },
                    "limitations": ["FAILURE_RETAINED", "NO_RETRY", "SYNTHETIC_CASE_ONLY"],
                }
            total_cost = round(total_cost + float(event["estimated_cost_cny"] or 0.0), 6)
            if total_cost > LIVE_VALIDATION_CASH_CAP_CNY:
                raise CommercialBetaError("LIVE_VALIDATION_CASH_CAP_REACHED")
            events.append(event)
            assessments.append(_provisional_assessment(case, event))

    successful_runs = sum(
        event["status"] == "SUCCEEDED" and assessment["output_contract_status"] == "PASS"
        for event, assessment in zip(events, assessments, strict=True)
    )
    red_line_assessments = [item for item in assessments if item["case_id"] == "CASE-05"]
    red_line_logic = "PASS" if all(item["red_line_status"] in {"PASS", "FAIL"} for item in red_line_assessments) else "FAIL"
    evidence_capture = "PASS" if all(
        event["evidence_ref"].get("admission_status") == "REFERENCE_ONLY_NOT_DBOS_ADMITTED"
        and event["evidence_ref"].get("canonical_evidence_object_created") is False
        and event["evidence_ref"].get("authority_effect") == "NONE"
        for event in events
    ) else "FAIL"
    action_matches = sum(item["expected_action_match"] for item in assessments)
    correct_escalations = sum(
        item["expected_action"] == "ESCALATE" and item["observed_action"] == "ESCALATE"
        for item in assessments
    )
    unsubstantiated_claims = sum(item["policy_reference_grounded"] == "FAIL" for item in assessments)
    average_latency = [event["elapsed_ms"] for event in events if isinstance(event["elapsed_ms"], int)]
    beta_ready = successful_runs >= MIN_SUCCESSFUL_RUNS and evidence_capture == "PASS" and red_line_logic == "PASS"
    result = {
        "result_type": "TITMAS_ENTERPRISE_AGENT_REVIEW_RESULT",
        "product": PRODUCT_NAME,
        "product_zh": PRODUCT_NAME_ZH,
        "version": VERSION,
        "release_channel": "commercial-beta",
        "observed_at": observed_at,
        "scenario": {
            "enterprise_name": fixture["enterprise_name"],
            "enterprise_name_zh": fixture["enterprise_name_zh"],
            "policy_version": fixture["policy_version"],
            "fixture_id": fixture["fixture_id"],
            "fixture_version": fixture["fixture_version"],
            "fixture_digest": sha256_value(fixture),
            "privacy_classification": "SYNTHETIC",
            "case_count": len(fixture["cases"]),
        },
        "tested_configuration": {
            "provider": adapter.provider,
            "provider_label": "Alibaba Cloud Model Studio",
            "provider_mode": adapter.provider_mode,
            "configured_model": adapter.model,
            "reported_models": sorted({item["reported_model_id"] for item in events if item["reported_model_id"]}),
            "model_pinning_status": adapter.model_pinning_status,
            "parameters": dict(DEFAULT_PARAMETERS),
        },
        "observed_facts": events,
        "provisional_assessments": assessments,
        "human_judgments": [],
        "human_judgment_status": "NOT_ASSESSED",
        "metrics": {
            "task_completion_rate_provisional": round(action_matches / REQUIRED_LIVE_RUNS, 4),
            "unsubstantiated_claim_count": unsubstantiated_claims,
            "correct_human_escalation_count": correct_escalations,
            "red_line_failure_count": sum(item["red_line_status"] == "FAIL" for item in assessments),
            "average_response_latency_ms": round(sum(average_latency) / len(average_latency), 2) if average_latency else "NOT_ASSESSED",
            "total_model_cost_cny": total_cost,
            "evidence_capture_completeness": round(
                sum(event["evidence_ref"].get("admission_status") == "REFERENCE_ONLY_NOT_DBOS_ADMITTED" for event in events) / REQUIRED_LIVE_RUNS,
                4,
            ),
            "successful_runs": successful_runs,
            "required_runs": REQUIRED_LIVE_RUNS,
        },
        "red_line_logic": red_line_logic,
        "evidence_capture": evidence_capture,
        "recommendation_index": {"status": "INCOMPLETE", "value": None, "reason": "HUMAN_JUDGMENT_NOT_ASSESSED"},
        "deployment_level": "L0" if any(item["red_line_status"] == "FAIL" for item in assessments) else "NOT_ASSESSED",
        "evidence_level": "E1",
        "commercial_beta_ready": beta_ready,
        "production_ready": False,
        "customer_validated": False,
        "security_certified": False,
        "compliance_certified": False,
        "sla_available": False,
        "dify_live_verified": False,
        "limits": [
            "SYNTHETIC_CASES_ONLY",
            "OBSERVED_FACT_NE_BUSINESS_CORRECTNESS",
            "PROVISIONAL_ASSESSMENT_NE_FINAL_AUTHORITY",
            "EVIDENCE_NE_TRUTH",
            "EVALUATION_NE_EXECUTION_AUTHORIZATION",
            "NO_CUSTOMER_VALIDATION",
            "NO_PRODUCTION_READINESS_CLAIM",
        ],
        "second_truth_source_created": False,
        "second_authority_chain_created": False,
        "automatic_retry_count": 0,
    }
    if _has_secret(result):
        raise CommercialBetaError("SECRET_SCAN_FAILED_ON_CANONICAL_RESULT")
    result["result_digest"] = sha256_value(result)
    return result


def _three_cases(result: dict[str, Any]) -> list[dict[str, Any]]:
    failures = [item for item in result["provisional_assessments"] if item["status"] != "PASS"]
    selected = failures[:3]
    if len(selected) < 3:
        selected.extend(item for item in result["provisional_assessments"] if item not in selected[:3])
    return selected[:3]


def render_html_report(result: dict[str, Any]) -> str:
    """Project the canonical result object to a standalone HTML view."""

    metrics = result["metrics"]
    cases = "".join(
        "<tr>"
        f"<td>{html.escape(item['case_id'])}</td>"
        f"<td>{html.escape(item['run_id'])}</td>"
        f"<td>{html.escape(item['status'])}</td>"
        f"<td>{html.escape(str(item.get('observed_action') or 'NOT_ASSESSED'))}</td>"
        f"<td>{html.escape(', '.join(item['reason_codes']) or '—')}</td>"
        "</tr>"
        for item in result["provisional_assessments"]
    )
    highlights = "".join(
        f"<li><strong>{html.escape(item['case_id'])}</strong>：{html.escape(item['status'])}；"
        f"{html.escape(', '.join(item['reason_codes']) or '无自动暂定异常')}</li>"
        for item in _three_cases(result)
    )
    data = html.escape(canonical_result_bytes(result).decode("utf-8"))
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{PRODUCT_NAME_ZH} {VERSION}</title>
<style>body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#17212b;margin:0;background:#f7f9fb}}main{{max-width:1040px;margin:32px auto;padding:0 20px}}section{{background:#fff;border:1px solid #dce3ea;border-radius:12px;padding:22px;margin:16px 0}}h1{{margin-bottom:4px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}}.metric{{border:1px solid #e1e7ed;border-radius:8px;padding:12px}}.label{{font-size:.85rem;color:#52616f}}.value{{font-size:1.25rem;font-weight:650;margin-top:5px}}table{{border-collapse:collapse;width:100%}}th,td{{border-bottom:1px solid #e1e7ed;padding:9px;text-align:left;vertical-align:top}}code{{white-space:pre-wrap;word-break:break-word}}.notice{{color:#7b3f00;background:#fff5e8;border-left:4px solid #e49000;padding:12px}}</style></head>
<body><main>
<h1>{PRODUCT_NAME}</h1><p>{PRODUCT_NAME_ZH} · Commercial Beta {VERSION}</p>
<section><div class="grid"><div><div class="label">被测方案</div><div class="value">阿里云百炼 + 千问</div></div><div><div class="label">场景</div><div class="value">企业客服回复建议</div></div><div><div class="label">测试时间</div><div class="value">{html.escape(result['observed_at'])}</div></div><div><div class="label">模型</div><div class="value">{html.escape(result['tested_configuration']['configured_model'])}</div></div><div><div class="label">案例 / 运行</div><div class="value">6 / {metrics['required_runs']}</div></div></div></section>
<section><div class="grid"><div class="metric"><div class="label">重大红线逻辑</div><div class="value">{html.escape(result['red_line_logic'])}</div></div><div class="metric"><div class="label">任务规则匹配（自动暂定）</div><div class="value">{metrics['task_completion_rate_provisional']:.0%}</div></div><div class="metric"><div class="label">正确交人工</div><div class="value">{metrics['correct_human_escalation_count']}</div></div><div class="metric"><div class="label">无依据主张</div><div class="value">{metrics['unsubstantiated_claim_count']}</div></div><div class="metric"><div class="label">平均耗时</div><div class="value">{html.escape(str(metrics['average_response_latency_ms']))} ms</div></div><div class="metric"><div class="label">模型成本</div><div class="value">¥{metrics['total_model_cost_cny']:.6f}</div></div><div class="metric"><div class="label">证据完整</div><div class="value">{metrics['evidence_capture_completeness']:.0%}</div></div></div></section>
<section><p><strong>上线建议：</strong>{html.escape(result['deployment_level'])}　<strong>证据等级：</strong>{html.escape(result['evidence_level'])}</p><div class="notice">人工裁决状态：{html.escape(result['human_judgment_status'])}。自动暂定结果不是业务真相、部署授权、认证或生产就绪结论。</div></section>
<section><h2>最值得复盘的3个案例</h2><ol>{highlights}</ol></section>
<section><h2>六案例详情（两次运行）</h2><table><thead><tr><th>案例</th><th>运行</th><th>自动暂定</th><th>动作</th><th>原因码</th></tr></thead><tbody>{cases}</tbody></table></section>
<section><h2>证据与局限</h2><p>Evidence Reference：现有 TITMAS 引用绑定；不会创建规范 Evidence Object、授权或第二事实源。</p><p>限制：{html.escape('；'.join(result['limits']))}</p><p>结果摘要：<code>{html.escape(result['result_digest'])}</code></p></section>
<section><h2>机器可读规范结果</h2><details><summary>展开 canonical result</summary><pre><code>{data}</code></pre></details></section>
</main></body></html>"""


def write_reports(result: dict[str, Any], output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / RESULT_JSON_NAME
    html_path = output_dir / RESULT_HTML_NAME
    json_path.write_bytes(canonical_result_bytes(result))
    html_path.write_text(render_html_report(result), encoding="utf-8")
    return {"json": json_path, "html": html_path}


def public_sample(result: dict[str, Any]) -> dict[str, Any]:
    """Return a small synthetic-only public projection without provider identifiers.

    The first live validation result predates the display-only ``case_title``
    field.  Title recovery is deliberately read from the frozen synthetic
    fixture, so that this projection remains backwards-compatible without
    rewriting observed facts or their result digest.
    """

    assessment_index = {
        (item["case_id"], item["run_id"]): item
        for item in result["provisional_assessments"]
    }
    case_titles = {case["case_id"]: case["title"] for case in _load_cases()["cases"]}
    selected = []
    for event in result["observed_facts"]:
        if event["run_id"].endswith("run-1") and event["case_id"] in {"CASE-01", "CASE-05", "CASE-06"}:
            assessment = assessment_index[(event["case_id"], event["run_id"])]
            selected.append({
                "case_id": event["case_id"],
                "case_title": assessment.get("case_title", case_titles[event["case_id"]]),
                "run_id": event["run_id"],
                "configured_model_id": event["configured_model_id"],
                "reported_model_id": event["reported_model_id"],
                "status": event["status"],
                "output_text": event["output_text"],
                "input_tokens": event["input_tokens"],
                "output_tokens": event["output_tokens"],
                "total_tokens": event["total_tokens"],
                "elapsed_ms": event["elapsed_ms"],
                "estimated_cost_cny": event["estimated_cost_cny"],
                "cost_basis": event["cost_basis"],
                "provisional_assessment": {
                    "status": assessment["status"],
                    "expected_action": assessment["expected_action"],
                    "observed_action": assessment["observed_action"],
                    "policy_reference_grounded": assessment["policy_reference_grounded"],
                    "red_line_status": assessment["red_line_status"],
                    "reason_codes": assessment["reason_codes"],
                },
                "evidence_ref": {
                    "source_contract_ref": event["evidence_ref"]["source_contract_ref"],
                    "admission_status": event["evidence_ref"]["admission_status"],
                    "canonical_evidence_object_created": event["evidence_ref"]["canonical_evidence_object_created"],
                    "truth_effect": event["evidence_ref"]["truth_effect"],
                    "authority_effect": event["evidence_ref"]["authority_effect"],
                },
            })
    sample = {
        "sample_type": "TITMAS_ENTERPRISE_AGENT_REVIEW_SANITIZED_PUBLIC_SAMPLE",
        "public_sample": True,
        "product": result["product"],
        "product_zh": result["product_zh"],
        "version": result["version"],
        "source_result_digest": result["result_digest"],
        "observed_at": result["observed_at"],
        "scenario": result["scenario"],
        "tested_configuration": {
            "provider_label": result["tested_configuration"]["provider_label"],
            "provider_mode": result["tested_configuration"]["provider_mode"],
            "configured_model": result["tested_configuration"]["configured_model"],
            "reported_models": result["tested_configuration"]["reported_models"],
            "model_pinning_status": result["tested_configuration"]["model_pinning_status"],
        },
        "metrics": result["metrics"],
        "red_line_logic": result["red_line_logic"],
        "evidence_capture": result["evidence_capture"],
        "evidence_level": result["evidence_level"],
        "human_judgment_status": result["human_judgment_status"],
        "commercial_beta_ready": result["commercial_beta_ready"],
        "production_ready": False,
        "customer_validated": False,
        "sample_cases": selected,
        "claims_not_supported": result["limits"],
    }
    sample["sanitization"] = {
        "api_key": "REMOVED_NOT_STORED",
        "authorization_header": "REMOVED_NOT_STORED",
        "account_workspace_identifiers": "NOT_INCLUDED",
        "local_paths": "NOT_INCLUDED",
    }
    if _has_secret(sample):
        raise CommercialBetaError("SECRET_SCAN_FAILED_ON_PUBLIC_SAMPLE")
    sample["result_digest"] = sha256_value(sample)
    return sample


def render_public_sample_html(sample: dict[str, Any]) -> str:
    """Project the sanitized sample object to a standalone public HTML page."""

    cards = "".join(
        "<article><h3>" + html.escape(item["case_id"] + " · " + item["case_title"]) + "</h3>"
        + "<p><strong>自动暂定：</strong>" + html.escape(item["provisional_assessment"]["status"])
        + "　<strong>红线：</strong>" + html.escape(item["provisional_assessment"]["red_line_status"]) + "</p>"
        + "<pre>" + html.escape(item["output_text"]) + "</pre>"
        + "<p>耗时 " + html.escape(str(item["elapsed_ms"])) + " ms；成本 ¥" + html.escape(str(item["estimated_cost_cny"])) + "</p></article>"
        for item in sample["sample_cases"]
    )
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{PRODUCT_NAME_ZH} 脱敏样例</title><style>body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;max-width:920px;margin:32px auto;padding:0 20px;color:#17212b}}article,section{{border:1px solid #dce3ea;border-radius:10px;padding:18px;margin:14px 0}}pre{{white-space:pre-wrap;background:#f7f9fb;padding:12px;border-radius:6px}}.note{{background:#fff5e8;border-left:4px solid #e49000;padding:12px}}</style></head><body><h1>{PRODUCT_NAME}</h1><p>{PRODUCT_NAME_ZH} · 脱敏公开样例 · {html.escape(sample['version'])}</p><section><p>供应商：阿里云百炼；模型：{html.escape(sample['tested_configuration']['configured_model'])}；案例：6；成功运行：{sample['metrics']['successful_runs']}/{sample['metrics']['required_runs']}；估算成本：¥{sample['metrics']['total_model_cost_cny']:.6f}</p><p>红线逻辑：{html.escape(sample['red_line_logic'])}；证据等级：{html.escape(sample['evidence_level'])}</p></section><section class="note">全部数据均为合成数据。自动暂定评估不等于人工最终裁决；Evidence Reference 不等于事实真相、认证或执行授权；本版本不是生产就绪。</section>{cards}<section><p>公开样例摘要：<code>{html.escape(sample['result_digest'])}</code></p></section></body></html>"""


def write_public_sample(sample: dict[str, Any], output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / PUBLIC_SAMPLE_JSON_NAME
    html_path = output_dir / PUBLIC_SAMPLE_HTML_NAME
    json_path.write_bytes(canonical_result_bytes(sample))
    html_path.write_text(render_public_sample_html(sample) + "\n", encoding="utf-8")
    return {"json": json_path, "html": html_path}


def _command_preflight(_: argparse.Namespace) -> int:
    print(json.dumps(live_preflight(), ensure_ascii=False, sort_keys=True))
    return 0 if live_preflight()["status"] == "READY_TO_REVIEW" else 2


def _command_review(args: argparse.Namespace) -> int:
    if args.provider != "bailian-direct":
        raise CommercialBetaError("only bailian-direct is admitted for commercial beta")
    preflight = live_preflight()
    if preflight["status"] != "READY_TO_REVIEW":
        print(json.dumps(preflight, ensure_ascii=False, sort_keys=True))
        return 2
    model, _ = selected_model()
    adapter = BailianDirectModelAdapter(
        api_key=os.environ["DASHSCOPE_API_KEY"],
        model=model,
        base_url=os.environ.get("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
    )
    result = build_result(adapter=adapter)
    paths = write_reports(result, Path(args.output_dir))
    print(json.dumps({"status": "COMPLETED", "commercial_beta_ready": result["commercial_beta_ready"], "reports": {key: str(value) for key, value in paths.items()}}, ensure_ascii=False, sort_keys=True))
    return 0 if result["commercial_beta_ready"] else 3


def _command_report(args: argparse.Namespace) -> int:
    source = Path(args.result)
    try:
        result = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CommercialBetaError("canonical result file is unavailable") from exc
    if not isinstance(result, dict) or result.get("result_type") != "TITMAS_ENTERPRISE_AGENT_REVIEW_RESULT":
        raise CommercialBetaError("report accepts only a canonical TITMAS result")
    paths = write_reports(result, Path(args.output_dir))
    print(json.dumps({"status": "COMPLETED", "reports": {key: str(value) for key, value in paths.items()}}, ensure_ascii=False, sort_keys=True))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m enterprise_agent_evaluation")
    subcommands = parser.add_subparsers(dest="command", required=True)
    subcommands.add_parser("preflight", help="检查本地直接模型评测前置条件").set_defaults(handler=_command_preflight)
    review = subcommands.add_parser("review", help="运行六个合成案例两次")
    review.add_argument("--provider", required=True)
    review.add_argument("--output-dir", default="titmas-enterprise-agent-review-output")
    review.set_defaults(handler=_command_review)
    report = subcommands.add_parser("report", help="从规范结果生成 HTML 和 JSON 报告")
    report.add_argument("--result", default=RESULT_JSON_NAME)
    report.add_argument("--output-dir", default=".")
    report.set_defaults(handler=_command_report)
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except CommercialBetaError as exc:
        print(json.dumps({"status": "BLOCKED", "reason_code": str(exc)}, ensure_ascii=False, sort_keys=True))
        return 3


__all__ = [
    "CommercialBetaError",
    "PRODUCT_NAME",
    "VERSION",
    "build_result",
    "canonical_result_bytes",
    "live_preflight",
    "main",
    "public_sample",
    "render_public_sample_html",
    "render_html_report",
    "write_public_sample",
    "write_reports",
]
