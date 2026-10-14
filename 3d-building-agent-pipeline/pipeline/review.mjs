/**
 * Application-owned, synchronous review-contract evaluator. No models, network,
 * TITMAS authentication, release authority, or claims of semantic image accuracy.
 *
 * Agent entry: evaluateReview(root, jobId, { builderId, expectedBindings,
 * outputBinding }) reads current contract,
 * results and every bound file. A local access record documents an observation;
 * its hash does NOT prove that a person/model looked at or understood the media.
 * Schema: schemas/review.schema.json. Test fixtures are protocol-only synthetic data.
 */
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, realpathSync, statSync } from 'node:fs';
import path from 'node:path';

const HASH = /^[a-f0-9]{64}$/;
const ID = /^[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$/;
const GROUPS = ['architectural_fidelity', 'reference_demo_match', 'technical', 'titmas_evidence'];
const ROLES = ['reference', 'output', 'requirements', 'source', 'model', 'camera'];
const KINDS = ['image', 'video', 'document', 'source'];
const STATES = ['PASS', 'FAIL', 'UNKNOWN', 'NOT_APPLICABLE', 'NOT_RUN'];
const object = (value) => value !== null && typeof value === 'object' && !Array.isArray(value);
const text = (value) => typeof value === 'string' && value.trim().length > 0;
const assigned = (value) => text(value) && !['UNKNOWN', 'UNASSIGNED', 'NOT_RUN'].includes(value);
const texts = (value, nonempty = false) => Array.isArray(value) && (!nonempty || value.length > 0) && value.every(text);
// Allow at most one minute of local clock skew; future-dated work is not done.
const date = (value) => text(value) && /^\d{4}-\d{2}-\d{2}T.*(?:Z|[+-]\d{2}:\d{2})$/.test(value) && Number.isFinite(Date.parse(value)) && Date.parse(value) <= Date.now() + 60_000;
const digest = (bytes) => createHash('sha256').update(bytes).digest('hex');
const refShape = (value) => shape(value, ['path', 'sha256']) && text(value.path) && HASH.test(value.sha256);
const unique = (values) => new Set(values).size === values.length;

function shape(value, required, optional = []) {
  return object(value) && required.every((key) => Object.hasOwn(value, key)) &&
    Object.keys(value).every((key) => required.includes(key) || optional.includes(key));
}

function beneath(root, target) {
  const rel = path.relative(root, target);
  return rel !== '' && rel !== '..' && !rel.startsWith(`..${path.sep}`) && !path.isAbsolute(rel);
}

/** Separate bounded resolver; deliberately does not broaden lib.mjs references. */
function resolveReviewReference(root, id, referencePath) {
  if (!ID.test(id ?? '') || typeof id !== 'string') throw new Error('Invalid job ID.');
  if (!text(referencePath) || path.isAbsolute(referencePath) || referencePath.includes('\\') || referencePath.includes('\0')) throw new Error('Expected repository-relative POSIX path.');
  const parts = referencePath.split('/');
  if (parts.some((part) => !part || part === '.' || part === '..' || part.includes(':'))) throw new Error('Forbidden path segment.');
  const directoryPrefix = [`jobs/${id}/`, 'artifacts/', 'docs/', 'app/src/', 'vendor/', 'pipeline/video/'].find((prefix) => referencePath.startsWith(prefix));
  const exactAppFile = /^app\/(?:package[^/]*\.json|tsconfig[^/]*\.json|vite\.config\.ts)$/.test(referencePath);
  if (!directoryPrefix && !exactAppFile) throw new Error('Path outside review allowlist or references another job.');
  const realRoot = realpathSync(root);
  const target = path.join(realRoot, ...parts);
  const resolved = realpathSync(target);
  const allowed = path.join(realRoot, directoryPrefix ? directoryPrefix.slice(0, -1) : 'app');
  if (!beneath(realRoot, allowed) || realpathSync(allowed) !== allowed || !beneath(allowed, resolved)) throw new Error('Reference escapes its allowed directory through a symlink.');
  if (exactAppFile && resolved !== target) throw new Error('Exact application file must not be redirected.');
  if (!statSync(resolved).isFile()) throw new Error('Reference is not a regular file.');
  return resolved;
}

function validMedia(bytes, kind) {
  if (kind === 'image') return (bytes.length > 24 && bytes.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]))) ||
    (bytes.length > 4 && bytes[0] === 255 && bytes[1] === 216 && bytes[2] === 255 && bytes.at(-2) === 255 && bytes.at(-1) === 217) ||
    (bytes.length > 16 && bytes.toString('ascii', 0, 4) === 'RIFF' && bytes.toString('ascii', 8, 12) === 'WEBP');
  if (kind === 'video') return bytes.length > 32 && (bytes.toString('ascii', 4, 8) === 'ftyp' || bytes.subarray(0, 4).equals(Buffer.from([26, 69, 223, 163])));
  return true; // Documents/source are byte-bound; their truth is not inferred.
}

function contractErrors(contract, id) {
  const errors = [];
  const fail = (detail) => errors.push(detail);
  if (!shape(contract, ['schema_version', 'job_id', 'revision', 'scope', 'source_checklist', 'input_bindings', 'criteria'])) return ['Invalid contract object fields.'];
  if (contract.schema_version !== 'review-contract.v1' || contract.job_id !== id || !text(contract.revision) || !text(contract.scope)) fail('Invalid schema version, job identity, revision or scope.');
  if (!refShape(contract.source_checklist)) fail('source_checklist requires path and SHA-256.');
  if (!Array.isArray(contract.input_bindings) || !contract.input_bindings.length) return [...errors, 'input_bindings must be a nonempty array.'];
  const inputs = new Map();
  for (const input of contract.input_bindings) {
    if (!shape(input, ['id', 'role', 'kind', 'path', 'sha256']) || !text(input.id) || !ROLES.includes(input.role) || !KINDS.includes(input.kind) || !text(input.path) || !HASH.test(input.sha256)) { fail('Invalid input binding fields.'); continue; }
    if (inputs.has(input.id)) fail(`Duplicate input ID: ${input.id}.`);
    inputs.set(input.id, input);
  }
  if (!Array.isArray(contract.criteria) || !contract.criteria.length) return [...errors, 'criteria must be a nonempty array.'];
  const criterionIds = new Set();
  for (const criterion of contract.criteria) {
    if (!shape(criterion, ['id', 'group', 'required', 'external', 'severity', 'title', 'expected', 'input_ids', 'required_evidence_roles']) ||
        !text(criterion.id) || !GROUPS.includes(criterion.group) || typeof criterion.required !== 'boolean' || typeof criterion.external !== 'boolean' ||
        !['P1', 'P2'].includes(criterion.severity) || !text(criterion.title) || !texts(criterion.expected, true) || !texts(criterion.input_ids, true) ||
        !texts(criterion.required_evidence_roles, true) || !unique(criterion.input_ids) || !unique(criterion.required_evidence_roles) || !criterion.required_evidence_roles.every((role) => ROLES.includes(role))) {
      fail('Invalid criterion fields, group or evidence roles.'); continue;
    }
    if (criterionIds.has(criterion.id)) fail(`Duplicate criterion ID: ${criterion.id}.`);
    criterionIds.add(criterion.id);
    if (criterion.group === 'titmas_evidence' && !criterion.external) fail(`${criterion.id}: TITMAS criteria must be external.`);
    if (criterion.group !== 'titmas_evidence' && criterion.external) fail(`${criterion.id}: only TITMAS criteria may be external.`);
    if (criterion.input_ids.some((inputId) => !inputs.has(inputId))) fail(`${criterion.id}: unknown input binding.`);
    const boundInputs = criterion.input_ids.map((inputId) => inputs.get(inputId)).filter(Boolean);
    if (criterion.required_evidence_roles.some((role) => !boundInputs.some((input) => input.role === role))) fail(`${criterion.id}: required evidence role has no bound input.`);
    const mediaCriterion = ['architectural_fidelity', 'reference_demo_match'].includes(criterion.group) && criterion.required_evidence_roles.some((role) => ['reference', 'output'].includes(role));
    if (mediaCriterion) {
      for (const role of ['reference', 'output']) {
        if (!criterion.required_evidence_roles.includes(role) || !boundInputs.some((input) => input.role === role && ['image', 'video'].includes(input.kind))) fail(`${criterion.id}: visual comparison requires reference AND output media.`);
      }
    }
  }
  for (const group of ['architectural_fidelity', 'reference_demo_match', 'technical']) if (!contract.criteria.some((criterion) => object(criterion) && criterion.group === group && criterion.required === true && criterion.external === false)) fail(`Missing required nonexternal ${group} criterion.`);
  for (const group of ['architectural_fidelity', 'reference_demo_match']) if (!contract.criteria.some((criterion) => object(criterion) && criterion.group === group && criterion.required === true && criterion.external === false && Array.isArray(criterion.required_evidence_roles) && ['reference', 'output'].every((role) => criterion.required_evidence_roles.includes(role)))) fail(`Missing required reference/output media comparison in ${group}.`);
  return errors;
}

/**
 * ready/content_ready means only that the declared application contract has
 * complete admissible passing records. It never means release-ready, visually
 * correct, authenticated TITMAS execution, or independent-model consensus.
 */
export function evaluateReview(root, id, { builderId, expectedBindings = [], outputBinding = null } = {}) {
  const issues = [];
  const groups = Object.fromEntries(GROUPS.map((group) => [group, { status: 'NOT_RUN', required: 0, reviewed: 0, passed: 0 }]));
  const coverage = { required: 0, reviewed: 0, passed: 0, unknown: [], failed: [], missing: [] };
  const evaluated = [];
  let contractHash = null;
  const add = (code, detail, severity = 'ERROR') => issues.push({ station: 'visual', code, detail, severity });
  const output = (status, ready = false) => ({ status, ready, content_ready: ready, contract_sha256: contractHash, groups, coverage, issues, results: evaluated });
  const read = (referencePath) => readFileSync(resolveReviewReference(root, id, referencePath));
  const reference = (ref, label, kind) => {
    if (!refShape(ref)) { add('INVALID_REVIEW_REFERENCE', `${label}: expected {path, sha256}.`); return null; }
    try {
      const bytes = read(ref.path);
      if (digest(bytes) !== ref.sha256) { add('STALE_REVIEW_INPUT', `${label}: current SHA-256 differs from the recorded binding.`); return null; }
      if (!validMedia(bytes, kind)) { add('INVALID_REVIEW_MEDIA', `${label}: bytes do not have a supported ${kind} header.`); return null; }
      return bytes;
    } catch (error) { add('INVALID_REVIEW_REFERENCE', `${label}: ${error.message}`); return null; }
  };
  if (typeof id !== 'string' || !ID.test(id)) { add('INVALID_REVIEW_JOB_ID', 'Invalid job ID.'); return output('NEEDS_REVISION'); }
  const contractPath = `jobs/${id}/review-contract.json`;
  const resultsPath = `jobs/${id}/review-results.json`;
  if (!existsSync(path.join(root, contractPath))) { add('REVIEW_CONTRACT_MISSING', 'review-contract.json has not been recorded.', 'BLOCKER'); return output('NOT_RUN'); }
  let contract;
  try { const bytes = read(contractPath); contractHash = digest(bytes); contract = JSON.parse(bytes.toString('utf8')); }
  catch (error) { add('INVALID_REVIEW_CONTRACT', error.message); return output('NEEDS_REVISION'); }
  const errors = contractErrors(contract, id);
  if (errors.length) { for (const detail of errors) add('INVALID_REVIEW_CONTRACT', detail); return output('NEEDS_REVISION'); }
  for (const criterion of contract.criteria) if (criterion.required) {
    groups[criterion.group].required += 1;
    if (!criterion.external) coverage.required += 1;
  }
  const checklistBytes = reference(contract.source_checklist, 'source_checklist');
  // A deliberately bounded adapter for this application's existing frozen rubric.
  // Generic documents are byte-bound only; we cannot infer rubric completeness.
  if (checklistBytes) {
    let checklist;
    try { checklist = JSON.parse(checklistBytes.toString('utf8')); } catch { /* Ordinary source documents are allowed. */ }
    if (checklist?.schema_version === 'architecture-rework-acceptance-proposal.v1') {
      if (checklist.job_id !== id || !Array.isArray(checklist.items) || !checklist.items.length) add('INVALID_SOURCE_CHECKLIST', 'Known application checklist has invalid job identity or items.');
      else {
        const ids = new Set();
        for (const item of checklist.items) {
          if (!object(item) || !text(item.id) || ids.has(item.id) || !GROUPS.includes(item.group) || !['P1', 'P2'].includes(item.priority) || !texts(item.expected, true)) { add('INVALID_SOURCE_CHECKLIST', 'Known checklist contains an invalid or duplicate item.'); continue; }
          ids.add(item.id);
          const criterion = contract.criteria.find((entry) => entry.id === item.id);
          if (!criterion || criterion.group !== item.group || criterion.required !== true || criterion.external !== (item.group === 'titmas_evidence') || criterion.severity !== item.priority || JSON.stringify(criterion.expected) !== JSON.stringify(item.expected)) add('SOURCE_CHECKLIST_COVERAGE_MISSING', `${item.id}: contract must retain the known checklist's group, required status, priority and expected statements.`);
        }
      }
    }
  }
  const inputMap = new Map(contract.input_bindings.map((input) => [input.id, input]));
  for (const input of contract.input_bindings) reference({ path: input.path, sha256: input.sha256 }, `input ${input.id}`, input.kind);
  // The caller supplies current job-selected artifacts, so an intact older
  // contract/output cannot be substituted for a newly selected job version.
  if (!Array.isArray(expectedBindings)) add('REVIEW_JOB_BINDING_MISSING', 'expectedBindings must be an array of current {path, sha256} references.');
  else for (const expected of expectedBindings) if (!refShape(expected) || !contract.input_bindings.some((input) => input.path === expected.path && input.sha256 === expected.sha256)) add('REVIEW_JOB_BINDING_MISSING', `Current job binding is absent from this contract: ${text(expected?.path) ? expected.path : '(invalid binding)'}.`);
  const currentOutputIds = new Set(outputBinding && refShape(outputBinding) ? contract.input_bindings.filter((input) => input.role === 'output' && input.kind === 'video' && input.path === outputBinding.path && input.sha256 === outputBinding.sha256).map((input) => input.id) : []);
  const requiresCurrentOutput = (criterion) => outputBinding !== null && criterion.required && ['architectural_fidelity', 'reference_demo_match'].includes(criterion.group) && criterion.required_evidence_roles.includes('output');
  if (outputBinding !== null) {
    if (!refShape(outputBinding) || !currentOutputIds.size) add('REVIEW_OUTPUT_NOT_COVERED', 'Current job video must be registered as an output/video binding.');
    for (const criterion of contract.criteria) if (requiresCurrentOutput(criterion) && !criterion.input_ids.some((inputId) => currentOutputIds.has(inputId))) add('REVIEW_OUTPUT_NOT_COVERED', `${criterion.id}: criterion does not cover the actual current job video.`);
  }
  const inputsInvalid = issues.length > 0;
  const staleInputs = issues.some((issue) => issue.code === 'STALE_REVIEW_INPUT');
  if (!existsSync(path.join(root, resultsPath))) {
    coverage.missing = contract.criteria.filter((criterion) => criterion.required && !criterion.external).map((criterion) => criterion.id);
    add('REVIEW_RESULTS_MISSING', 'review-results.json has not been recorded.', 'BLOCKER');
    if (staleInputs) for (const group of Object.values(groups)) if (group.required) group.status = 'STALE';
    return output(inputsInvalid ? 'NEEDS_REVISION' : 'NOT_RUN');
  }
  let document;
  try { document = JSON.parse(read(resultsPath).toString('utf8')); }
  catch (error) { add('INVALID_REVIEW_RESULTS', error.message); return output('NEEDS_REVISION'); }
  if (!shape(document, ['schema_version', 'job_id', 'contract_sha256', 'status', 'results']) || document.schema_version !== 'review-results.v1' || document.job_id !== id ||
      !HASH.test(document.contract_sha256 ?? '') || !['NOT_RUN', 'RECORDED'].includes(document.status) || !Array.isArray(document.results)) {
    add('INVALID_REVIEW_RESULTS', 'Invalid results document fields, version, job identity, status or contract hash.'); return output('NEEDS_REVISION');
  }
  if (document.contract_sha256 !== contractHash) { add('STALE_REVIEW_CONTRACT', 'Results bind an earlier contract; new results must review the current contract.'); for (const group of Object.values(groups)) if (group.required) group.status = 'STALE'; return output('NEEDS_REVISION'); }
  if (document.status === 'NOT_RUN' && document.results.length) { add('INVALID_REVIEW_RESULTS', 'NOT_RUN document must have empty results.'); return output('NEEDS_REVISION'); }
  const criterionMap = new Map(contract.criteria.map((criterion) => [criterion.id, criterion]));
  const resultMap = new Map();
  const duplicateIds = new Set();
  for (const result of document.results) {
    if (!object(result) || !criterionMap.has(result.criterion_id)) { add('UNKNOWN_REVIEW_CRITERION', 'Result references an undeclared criterion.'); continue; }
    if (resultMap.has(result.criterion_id)) { duplicateIds.add(result.criterion_id); add('DUPLICATE_REVIEW_CRITERION', `Duplicate result for ${result.criterion_id}.`); continue; }
    resultMap.set(result.criterion_id, result);
  }
  for (const criterion of contract.criteria) {
    const result = resultMap.get(criterion.id);
    const group = groups[criterion.group];
    const contentRequired = criterion.required && !criterion.external;
    const start = issues.length;
    let valid = true;
    let openP1 = false;
    if (result) {
      if (!shape(result, ['criterion_id', 'status', 'reviewer_id', 'reviewed_at', 'observation', 'limitations', 'shared_dependencies', 'evidence', 'issues']) ||
          !STATES.includes(result.status) || !assigned(result.reviewer_id) || !date(result.reviewed_at) || !text(result.observation) || !texts(result.limitations) || !texts(result.shared_dependencies) || !Array.isArray(result.evidence) || !Array.isArray(result.issues)) {
        add('INVALID_REVIEW_RESULT', `${criterion.id}: invalid result fields, reviewer, timestamp, observation or arrays.`); valid = false;
      } else {
        if (result.status !== 'NOT_RUN' && (!assigned(builderId) || result.reviewer_id === builderId)) add('REVIEWER_NOT_INDEPENDENT', `${criterion.id}: a known builder and a different reviewer identity are required.`);
        const evidenceRoles = new Set();
        const mediaRoles = new Set();
        const observedInputs = new Set();
        for (const evidence of result.evidence) {
          if (!shape(evidence, ['input_id', 'locator', 'access_record']) || !text(evidence.locator) || !criterion.input_ids.includes(evidence.input_id) || !refShape(evidence.access_record)) {
            add('INVALID_REVIEW_EVIDENCE', `${criterion.id}: evidence must identify a bound input, a location and an access record.`); continue;
          }
          const input = inputMap.get(evidence.input_id);
          const beforeAccess = issues.length;
          const bytes = reference(evidence.access_record, `${criterion.id}/${input.id} access record`);
          if (bytes) {
            try {
              const access = JSON.parse(bytes.toString('utf8'));
              if (!shape(access, ['schema_version', 'input_id', 'input_sha256', 'method', 'observer_id', 'observed_at', 'trace_reference']) ||
                  access.schema_version !== 'review-access.v1' || access.input_id !== input.id || access.input_sha256 !== input.sha256 ||
                  access.observer_id !== result.reviewer_id || !date(access.observed_at) || Date.parse(access.observed_at) > Date.parse(result.reviewed_at) || !text(access.trace_reference)) throw new Error('Access record identity, digest, observer, time or trace does not match.');
              const methods = { image: ['IMAGE_VIEW'], video: ['VIDEO_REVIEW', 'FRAME_EXTRACTION'], document: ['DOCUMENT_READ'], source: ['DOCUMENT_READ'] };
              if (!methods[input.kind].includes(access.method)) throw new Error('Access method is incompatible with input kind.');
            } catch (error) { add('INVALID_REVIEW_ACCESS', `${criterion.id}/${input.id}: ${error.message}`); }
          }
          if (issues.length === beforeAccess) {
            evidenceRoles.add(input.role);
            observedInputs.add(input.id);
            if (['image', 'video'].includes(input.kind)) mediaRoles.add(input.role);
          }
        }
        if (result.status === 'PASS') {
          if (requiresCurrentOutput(criterion) && ![...currentOutputIds].some((inputId) => observedInputs.has(inputId))) add('REVIEW_OUTPUT_NOT_COVERED', `${criterion.id}: PASS evidence must record access to the actual current job video.`);
          if (!result.evidence.length || criterion.required_evidence_roles.some((role) => !evidenceRoles.has(role))) add('INCOMPLETE_REVIEW_EVIDENCE', `${criterion.id}: PASS must cover each required evidence role with valid access records.`);
          if (['architectural_fidelity', 'reference_demo_match'].includes(criterion.group) && criterion.required_evidence_roles.some((role) => ['reference', 'output'].includes(role)) && ['reference', 'output'].some((role) => !mediaRoles.has(role))) add('MISSING_VISUAL_MEDIA_EVIDENCE', `${criterion.id}: document text cannot replace observed reference/output media.`);
        }
        const issueIds = new Set();
        for (const issue of result.issues) {
          if (!shape(issue, ['id', 'severity', 'status'], ['resolution_evidence']) || !text(issue.id) || issueIds.has(issue.id) || !['P1', 'P2'].includes(issue.severity) || !['OPEN', 'CLOSED'].includes(issue.status)) { add('INVALID_REVIEW_ISSUE', `${criterion.id}: invalid or duplicate issue.`); continue; }
          issueIds.add(issue.id);
          if (issue.status === 'CLOSED') reference(issue.resolution_evidence, `${criterion.id}/${issue.id} closure`);
          if (issue.status === 'OPEN' && issue.severity === 'P1') { openP1 = true; if (!criterion.external) add('OPEN_P1_REVIEW_ISSUE', `${criterion.id}/${issue.id}: P1 issue remains open.`, 'BLOCKER'); }
        }
        valid = issues.length === start && !duplicateIds.has(criterion.id);
      }
    }
    const status = !result ? 'MISSING' : result.status;
    const reviewed = Boolean(result && valid && status !== 'NOT_RUN' && !inputsInvalid);
    const passed = Boolean(reviewed && status === 'PASS' && !openP1);
    evaluated.push({ criterion_id: criterion.id, group: criterion.group, required: criterion.required, external: criterion.external, status, valid: Boolean(result && valid && !inputsInvalid), reviewer_id: result?.reviewer_id ?? null });
    if (criterion.required) { if (reviewed) group.reviewed += 1; if (passed && !criterion.external) group.passed += 1; }
    if (contentRequired) {
      if (reviewed) coverage.reviewed += 1;
      if (passed) coverage.passed += 1;
      else if (!result || status === 'NOT_RUN') { coverage.missing.push(criterion.id); add('REVIEW_CRITERION_NOT_RUN', `${criterion.id}: required criterion is not reviewed.`, 'BLOCKER'); }
      else if (status === 'UNKNOWN' || status === 'NOT_APPLICABLE') { coverage.unknown.push(criterion.id); add('REVIEW_CRITERION_UNRESOLVED', `${criterion.id}: required criterion is ${status}.`, 'BLOCKER'); }
      else { coverage.failed.push(criterion.id); if (status === 'FAIL') add('REVIEW_CRITERION_FAILED', `${criterion.id}: reviewer reported FAIL.`, 'BLOCKER'); }
    }
  }
  for (const [name, group] of Object.entries(groups)) {
    const members = evaluated.filter((result) => result.group === name && result.required);
    if (!group.required) continue;
    if (staleInputs) group.status = 'STALE';
    else if (members.some((result) => result.status === 'FAIL' || (result.status !== 'MISSING' && !result.valid))) group.status = 'FAIL';
    else if (name === 'titmas_evidence') group.status = group.reviewed ? 'UNKNOWN' : 'NOT_RUN'; // Never authenticate a hand-written receipt.
    else if (group.passed === group.required) group.status = 'PASS';
    else if (members.some((result) => ['UNKNOWN', 'NOT_APPLICABLE'].includes(result.status))) group.status = 'UNKNOWN';
    else group.status = 'NOT_RUN';
  }
  const ready = issues.length === 0 && coverage.required > 0 && coverage.passed === coverage.required;
  return output(ready ? 'READY_FOR_SCOPED_REVIEW' : document.status === 'NOT_RUN' && !inputsInvalid && !issues.some((issue) => issue.severity === 'ERROR') ? 'NOT_RUN' : 'NEEDS_REVISION', ready);
}
