import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { evaluateReview } from '../review.mjs';

const ID = 'review-fixture';
const NOW = '2026-09-22T12:00:00Z';
const BUILDER = 'synthetic-builder';
const REVIEWER = 'synthetic-reviewer';
// These tiny media headers and observation traces are SYNTHETIC, protocol-only.
// No test observes architecture, measures fidelity or authenticates TITMAS.
const PNG = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScLbtAAAAABJRU5ErkJggg==', 'base64');
const MP4 = Buffer.alloc(64);
MP4.writeUInt32BE(24, 0);
MP4.write('ftyp', 4);
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');

function fixture(t) {
  const root = mkdtempSync(path.join(os.tmpdir(), 'architecture-review-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const prefix = `jobs/${ID}/`;
  const write = (name, value) => {
    const filename = path.join(root, name);
    mkdirSync(path.dirname(filename), { recursive: true });
    writeFileSync(filename, typeof value === 'string' || Buffer.isBuffer(value) ? value : `${JSON.stringify(value, null, 2)}\n`);
  };
  const read = (name) => JSON.parse(readFileSync(path.join(root, name), 'utf8'));
  const ref = (name) => ({ path: name, sha256: hash(readFileSync(path.join(root, name))) });
  write('docs/checklist.md', 'Synthetic protocol-only rubric, not an architectural standard.');
  write('docs/correction.md', 'Current synthetic user requirement version A.');
  write(`${prefix}reference.png`, PNG);
  write('vendor/demo.mp4', MP4);
  write(`${prefix}output.mp4`, Buffer.concat([MP4, Buffer.from('synthetic-output')]));
  write('app/src/model.ts', 'export const SYNTHETIC = true;');
  const inputs = [
    ['photo', 'reference', 'image', `${prefix}reference.png`],
    ['demo', 'reference', 'video', 'vendor/demo.mp4'],
    ['output', 'output', 'video', `${prefix}output.mp4`],
    ['source', 'source', 'source', 'app/src/model.ts'],
    ['correction', 'requirements', 'document', 'docs/correction.md'],
  ].map(([id, role, kind, file]) => ({ id, role, kind, ...ref(file) }));
  const criterion = (id, group, inputIds, roles) => ({ id, group, required: true, external: group === 'titmas_evidence', severity: 'P1', title: `Synthetic ${id}`, expected: ['Protocol fixture only; not actual fidelity.'], input_ids: inputIds, required_evidence_roles: roles });
  const contract = {
    schema_version: 'review-contract.v1', job_id: ID, revision: 'synthetic-1', scope: 'Synthetic protocol-only local testing.', source_checklist: ref('docs/checklist.md'), input_bindings: inputs,
    criteria: [criterion('AF-1', 'architectural_fidelity', ['photo', 'output'], ['reference', 'output']), criterion('RD-1', 'reference_demo_match', ['demo', 'output'], ['reference', 'output']), criterion('TE-1', 'technical', ['source'], ['source']), criterion('TM-1', 'titmas_evidence', ['source'], ['source'])],
  };
  write(`${prefix}review-contract.json`, contract);
  const access = new Map();
  for (const input of inputs) {
    const file = `${prefix}access/${input.id}.json`;
    write(file, { schema_version: 'review-access.v1', input_id: input.id, input_sha256: input.sha256, method: { image: 'IMAGE_VIEW', video: 'VIDEO_REVIEW', source: 'DOCUMENT_READ', document: 'DOCUMENT_READ' }[input.kind], observer_id: REVIEWER, observed_at: NOW, trace_reference: 'SYNTHETIC_PROTOCOL_FIXTURE: no actual media observation.' });
    access.set(input.id, ref(file));
  }
  const record = (criterion) => ({ criterion_id: criterion.id, status: 'PASS', reviewer_id: REVIEWER, reviewed_at: NOW, observation: 'Synthetic record for evaluator verification only.', limitations: ['Does not claim any real architecture was reviewed.'], shared_dependencies: ['Shared synthetic fixture generator.'], evidence: criterion.input_ids.map((inputId) => ({ input_id: inputId, locator: 'Synthetic frame 0 / whole fixture', access_record: access.get(inputId) })), issues: [] });
  const results = { schema_version: 'review-results.v1', job_id: ID, contract_sha256: ref(`${prefix}review-contract.json`).sha256, status: 'RECORDED', results: contract.criteria.filter((item) => !item.external).map(record) };
  write(`${prefix}review-results.json`, results);
  const saveContract = (value, rebind = true) => { write(`${prefix}review-contract.json`, value); if (rebind) { const current = read(`${prefix}review-results.json`); current.contract_sha256 = ref(`${prefix}review-contract.json`).sha256; write(`${prefix}review-results.json`, current); } };
  const mutateResults = (change) => { const current = read(`${prefix}review-results.json`); change(current); write(`${prefix}review-results.json`, current); };
  const evaluate = (options = {}) => evaluateReview(root, ID, { builderId: BUILDER, outputBinding: ref(`${prefix}output.mp4`), ...options });
  return { root, prefix, write, read, ref, contract, record, evaluate, saveContract, mutateResults };
}

function blocked(result, code) {
  assert.equal(result.ready, false);
  assert.equal(result.content_ready, false);
  if (code) assert.ok(result.issues.some((issue) => issue.code === code), JSON.stringify(result.issues));
  assert.ok(result.issues.every((issue) => issue.station === 'visual' && ['ERROR', 'BLOCKER'].includes(issue.severity)));
}

test('complete synthetic protocol records open only scoped content review; external TITMAS remains unrun', (t) => {
  const f = fixture(t);
  const result = f.evaluate();
  assert.equal(result.status, 'READY_FOR_SCOPED_REVIEW');
  assert.equal(result.ready, true);
  assert.equal(result.content_ready, true);
  assert.deepEqual(result.coverage, { required: 3, reviewed: 3, passed: 3, unknown: [], failed: [], missing: [] });
  assert.deepEqual(result.groups.titmas_evidence, { status: 'NOT_RUN', required: 1, reviewed: 0, passed: 0 });
  assert.equal(result.issues.length, 0);
});

test('absent contract/results and explicit NOT_RUN stay unrun and never throw', (t) => {
  const f = fixture(t);
  f.mutateResults((doc) => { doc.status = 'NOT_RUN'; doc.results = []; });
  assert.equal(f.evaluate().status, 'NOT_RUN');
  assert.deepEqual(f.evaluate().coverage.missing, ['AF-1', 'RD-1', 'TE-1']);
  rmSync(path.join(f.root, f.prefix, 'review-results.json'));
  assert.equal(f.evaluate().status, 'NOT_RUN');
  rmSync(path.join(f.root, f.prefix, 'review-contract.json'));
  blocked(f.evaluate(), 'REVIEW_CONTRACT_MISSING');
  assert.equal(f.evaluate().status, 'NOT_RUN');
});

test('each required outcome and omitted criterion are reported in separate coverage lists', (t) => {
  for (const status of ['FAIL', 'UNKNOWN', 'NOT_APPLICABLE', 'NOT_RUN', 'MISSING']) {
    const f = fixture(t);
    f.mutateResults((doc) => { if (status === 'MISSING') doc.results.shift(); else doc.results[0].status = status; });
    const result = f.evaluate();
    blocked(result);
    const key = status === 'FAIL' ? 'failed' : ['UNKNOWN', 'NOT_APPLICABLE'].includes(status) ? 'unknown' : 'missing';
    assert.deepEqual(result.coverage[key], ['AF-1']);
  }
});

test('all UNKNOWN records cannot satisfy content review', (t) => {
  const f = fixture(t);
  f.mutateResults((doc) => doc.results.forEach((result) => { result.status = 'UNKNOWN'; }));
  const result = f.evaluate();
  blocked(result, 'REVIEW_CRITERION_UNRESOLVED');
  assert.equal(result.coverage.reviewed, 3);
  assert.equal(result.coverage.passed, 0);
  assert.equal(result.coverage.unknown.length, 3);
});

test('duplicate or undeclared result IDs fail closed even when every normal result passes', (t) => {
  for (const code of ['DUPLICATE_REVIEW_CRITERION', 'UNKNOWN_REVIEW_CRITERION']) {
    const f = fixture(t);
    f.mutateResults((doc) => doc.results.push({ ...doc.results[0], criterion_id: code === 'DUPLICATE_REVIEW_CRITERION' ? 'AF-1' : 'UNDECLARED' }));
    blocked(f.evaluate(), code);
  }
});

test('conflicting duplicate result cannot remain valid, counted as passed or display group PASS', (t) => {
  const f = fixture(t);
  f.mutateResults((doc) => doc.results.push({ ...doc.results[0], status: 'FAIL' }));
  const result = f.evaluate();
  blocked(result, 'DUPLICATE_REVIEW_CRITERION');
  assert.equal(result.results.find((entry) => entry.criterion_id === 'AF-1').valid, false);
  assert.equal(result.groups.architectural_fidelity.status, 'FAIL');
  assert.equal(result.coverage.passed, 2);
  assert.deepEqual(result.coverage.failed, ['AF-1']);
});

test('strict runtime contract validation rejects empty, malformed, missing groups and binding IDs', (t) => {
  const edits = [
    (c) => { c.criteria = []; },
    (c) => { c.criteria[0].group = 'invented'; },
    (c) => { c.criteria[0].expected = [' ']; },
    (c) => { c.criteria[0].required = 'true'; },
    (c) => { c.criteria.push(c.criteria[0]); },
    (c) => { c.input_bindings.push(c.input_bindings[0]); },
    (c) => { c.criteria[0].input_ids.push('missing'); },
    (c) => { c.criteria = c.criteria.filter((criterion) => criterion.group !== 'technical'); },
    (c) => { c.criteria[3].external = false; },
    (c) => { c.criteria[0].external = true; },
    (c) => { c.authoritative = true; },
    (c) => { c.criteria[0].required_evidence_roles = ['requirements']; c.criteria[0].input_ids = ['correction']; },
  ];
  for (const edit of edits) { const f = fixture(t); edit(f.contract); f.saveContract(f.contract); blocked(f.evaluate(), 'INVALID_REVIEW_CONTRACT'); }
});

test('builder self-signature and unknown builder cannot pass independent review', (t) => {
  const f = fixture(t);
  blocked(f.evaluate({ builderId: REVIEWER }), 'REVIEWER_NOT_INDEPENDENT');
  blocked(f.evaluate({ builderId: 'UNASSIGNED' }), 'REVIEWER_NOT_INDEPENDENT');
});

test('open P1 cannot be hidden by PASS; closure needs matching current evidence', (t) => {
  const f = fixture(t);
  f.mutateResults((doc) => doc.results[0].issues.push({ id: 'ISSUE-1', severity: 'P1', status: 'OPEN' }));
  blocked(f.evaluate(), 'OPEN_P1_REVIEW_ISSUE');
  f.mutateResults((doc) => { doc.results[0].issues[0].status = 'CLOSED'; });
  blocked(f.evaluate(), 'INVALID_REVIEW_REFERENCE');
  f.write(`${f.prefix}resolution.txt`, 'Synthetic closure evidence only.');
  f.mutateResults((doc) => { doc.results[0].issues[0].resolution_evidence = f.ref(`${f.prefix}resolution.txt`); });
  assert.equal(f.evaluate().ready, true);
  f.write(`${f.prefix}resolution.txt`, 'Changed closure bytes');
  blocked(f.evaluate(), 'STALE_REVIEW_INPUT');
});

test('PASS requires actual bound evidence roles and valid observation metadata', (t) => {
  const edits = [
    (r) => { r.evidence = []; },
    (r) => { r.evidence.pop(); },
    (r) => { r.evidence[0].input_id = 'correction'; },
    (r) => { delete r.evidence[0].access_record; },
    (r) => { r.evidence[0].locator = ' '; },
    (r) => { r.observation = ''; },
    (r) => { r.shared_dependencies = 'none'; },
    (r) => { r.reviewed_at = 'yesterday'; },
    (r) => { r.status = 'APPROVED'; },
  ];
  for (const edit of edits) { const f = fixture(t); f.mutateResults((doc) => edit(doc.results[0])); blocked(f.evaluate()); }
});

test('media access cannot be a document read or a record for a different input/reviewer/time', (t) => {
  for (const [field, value] of [['method', 'DOCUMENT_READ'], ['observer_id', 'other-reviewer'], ['input_id', 'demo'], ['input_sha256', '0'.repeat(64)], ['observed_at', '2026-09-24T01:00:00Z'], ['trace_reference', '']]) {
    const f = fixture(t);
    const accessPath = `${f.prefix}access/photo.json`;
    const record = f.read(accessPath); record[field] = value; f.write(accessPath, record);
    f.mutateResults((doc) => { doc.results[0].evidence[0].access_record = f.ref(accessPath); });
    blocked(f.evaluate(), 'INVALID_REVIEW_ACCESS');
  }
});

test('future review and matching future access records cannot claim completed work', (t) => {
  const f = fixture(t);
  f.mutateResults((doc) => {
    for (const result of doc.results) {
      result.reviewed_at = '2099-01-01T00:00:00Z';
      for (const evidence of result.evidence) {
        const access = f.read(evidence.access_record.path);
        access.observed_at = result.reviewed_at;
        f.write(evidence.access_record.path, access);
        evidence.access_record = f.ref(evidence.access_record.path);
      }
    }
  });
  blocked(f.evaluate(), 'INVALID_REVIEW_RESULT');
});

test('FRAME_EXTRACTION supports video access, and document bytes cannot impersonate media', (t) => {
  const f = fixture(t);
  const accessPath = `${f.prefix}access/demo.json`;
  const record = f.read(accessPath); record.method = 'FRAME_EXTRACTION'; f.write(accessPath, record);
  f.mutateResults((doc) => { doc.results[1].evidence[0].access_record = f.ref(accessPath); });
  assert.equal(f.evaluate().ready, true);
  f.write(`${f.prefix}reference.png`, 'This is text pretending to be an image.');
  f.contract.input_bindings[0].sha256 = f.ref(`${f.prefix}reference.png`).sha256;
  f.saveContract(f.contract);
  blocked(f.evaluate(), 'INVALID_REVIEW_MEDIA');
});

test('user corrections, source, checklist and output changes invalidate even unused bound inputs', (t) => {
  for (const file of ['docs/correction.md', 'docs/checklist.md', 'app/src/model.ts', `jobs/${ID}/output.mp4`, `jobs/${ID}/reference.png`, 'vendor/demo.mp4']) {
    const f = fixture(t);
    f.write(file, Buffer.concat([readFileSync(path.join(f.root, file)), Buffer.from('\nchanged')]));
    const result = f.evaluate();
    blocked(result, 'STALE_REVIEW_INPUT');
    assert.equal(result.groups.architectural_fidelity.status, 'STALE');
    assert.equal(result.coverage.passed, 0);
    // Rewriting a report is not a valid way to refresh the old source bindings.
    f.mutateResults((doc) => { doc.results[0].observation = 'New report but old bindings.'; });
    blocked(f.evaluate(), 'STALE_REVIEW_INPUT');
  }
});

test('contract changes require results bound to its exact new bytes', (t) => {
  const f = fixture(t);
  f.contract.revision = 'synthetic-2';
  f.saveContract(f.contract, false);
  const result = f.evaluate();
  blocked(result, 'STALE_REVIEW_CONTRACT');
  assert.equal(result.groups.architectural_fidelity.status, 'STALE');
});

test('absolute/traversal/cross-job paths and symlink escapes are rejected', (t) => {
  for (const name of ['/etc/passwd', 'docs/../docs/correction.md', 'jobs/other/output.mp4', 'docs\\correction.md', 'pipeline/lib.mjs']) {
    const f = fixture(t);
    f.contract.input_bindings[4].path = name; f.saveContract(f.contract);
    blocked(f.evaluate(), 'INVALID_REVIEW_REFERENCE');
  }
  const f = fixture(t);
  f.write('outside.txt', 'Outside allowed directory.');
  symlinkSync(path.join(f.root, 'outside.txt'), path.join(f.root, 'docs', 'escape.txt'));
  f.contract.input_bindings[4] = { ...f.contract.input_bindings[4], ...f.ref('docs/escape.txt') }; f.saveContract(f.contract);
  blocked(f.evaluate(), 'INVALID_REVIEW_REFERENCE');
});

test('source checklist adapter prevents omitted, downgraded or weakened known requirements', (t) => {
  for (const edit of [(c) => c.criteria.pop(), (c) => { c.criteria[1].required = false; }, (c) => { c.criteria[1].severity = 'P2'; }, (c) => { c.criteria[1].expected = ['Recognizable is sufficient']; }]) {
    const f = fixture(t);
    const items = f.contract.criteria.map((c) => ({ id: c.id, group: c.group, priority: c.severity, expected: c.expected }));
    f.write('docs/checklist.json', { schema_version: 'architecture-rework-acceptance-proposal.v1', job_id: ID, items });
    f.contract.source_checklist = f.ref('docs/checklist.json');
    // Keep an additional required architectural criterion so optional-downgrade
    // failure specifically exercises checklist coverage rather than group minima.
    const extra = { ...f.contract.criteria[0], id: 'AF-extra' };
    f.contract.criteria.unshift(extra);
    f.mutateResults((doc) => doc.results.push(f.record(extra)));
    edit(f.contract); f.saveContract(f.contract);
    blocked(f.evaluate());
  }
});

test('job context cannot select new artifacts while a complete old contract stays present', (t) => {
  const f = fixture(t);
  assert.equal(f.evaluate({ expectedBindings: [f.ref(`${f.prefix}output.mp4`)] }).ready, true);
  f.write(`${f.prefix}new-output.mp4`, Buffer.concat([MP4, Buffer.from('new-version')]));
  const current = f.ref(`${f.prefix}new-output.mp4`);
  blocked(f.evaluate({ expectedBindings: [current], outputBinding: current }), 'REVIEW_JOB_BINDING_MISSING');
  f.contract.input_bindings.push({ id: 'new-output', role: 'output', kind: 'video', ...current }); f.saveContract(f.contract);
  blocked(f.evaluate({ expectedBindings: [current], outputBinding: current }), 'REVIEW_OUTPUT_NOT_COVERED');
  for (const criterion of f.contract.criteria.slice(0, 2)) criterion.input_ids.push('new-output');
  f.saveContract(f.contract);
  blocked(f.evaluate({ expectedBindings: [current], outputBinding: current }), 'REVIEW_OUTPUT_NOT_COVERED');
});

test('external handwritten TITMAS PASS cannot override a content failure or become authentication', (t) => {
  const f = fixture(t);
  f.mutateResults((doc) => doc.results.push(f.record(f.contract.criteria[3])));
  let result = f.evaluate();
  assert.equal(result.ready, true);
  assert.equal(result.groups.titmas_evidence.status, 'UNKNOWN');
  assert.equal(result.groups.titmas_evidence.passed, 0);
  f.mutateResults((doc) => { doc.results[0].status = 'FAIL'; });
  result = f.evaluate();
  blocked(result, 'REVIEW_CRITERION_FAILED');
  assert.deepEqual(result.coverage.failed, ['AF-1']);
});

test('malformed JSON, invalid results envelope and extra fields never become PASS', (t) => {
  for (const edit of [(doc) => { doc.job_id = 'other'; }, (doc) => { doc.status = 'PASS'; }, (doc) => { doc.authority = 'trusted'; }, (doc) => { doc.results = {}; }, (doc) => { doc.status = 'NOT_RUN'; }]) {
    const f = fixture(t); f.mutateResults(edit); blocked(f.evaluate(), 'INVALID_REVIEW_RESULTS');
  }
  const f = fixture(t);
  f.write(`${f.prefix}review-results.json`, '{broken');
  blocked(f.evaluate(), 'INVALID_REVIEW_RESULTS');
  f.write(`${f.prefix}review-contract.json`, '{broken');
  blocked(f.evaluate(), 'INVALID_REVIEW_CONTRACT');
  blocked(evaluateReview(f.root, '../escape'), 'INVALID_REVIEW_JOB_ID');
});
