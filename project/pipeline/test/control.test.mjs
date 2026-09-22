import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readFileSync, realpathSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { evaluateJob, handoffJob, initJob, resolveReference, sha256File } from '../lib.mjs';

const ID = 'test-building';
const TIME = '2026-09-22T12:00:00Z';
// Synthetic file-header fixtures exercise control integrity only, not media quality.
const PNG = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScLbtAAAAABJRU5ErkJggg==', 'base64');

function fixture(t) {
  const root = mkdtempSync(path.join(os.tmpdir(), 'architecture-control-'));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  initJob(root, { id: ID, building: '测试建筑', location: '测试地点', era: '现代艺术版本' });
  const file = (name) => path.join(root, 'jobs', ID, name);
  const read = (name) => JSON.parse(readFileSync(file(name), 'utf8'));
  const write = (name, value) => writeFileSync(file(name), `${JSON.stringify(value, null, 2)}\n`);
  const ref = (name) => ({ path: `jobs/${ID}/${name}`, sha256: sha256File(file(name)) });
  const status = () => evaluateJob(root, ID);
  const ready = (sourceType = 'WEB') => {
    writeFileSync(file('front.png'), PNG);
    writeFileSync(file('side.png'), Buffer.concat([PNG, Buffer.from('fixture-two')]));
    const source = { id: 'reference', source_type: sourceType, title: 'Synthetic reference fixture', accessed_at: TIME, license: { usage: 'RESEARCH_ONLY', publish_permission: 'UNKNOWN' } };
    if (sourceType === 'USER_PROVIDED') source.provenance = { task_id: 'original-task', note: 'User supplied two original attachments.' };
    else source.url = 'https://example.org/building';
    write('sources.json', { schema_version: '1.0', job_id: ID, bindings: { request_sha256: sha256File(file('request.json')) }, entries: [source], views: [{ id: 'front', source_id: 'reference', angle: 'front', image: ref('front.png') }, { id: 'side', source_id: 'reference', angle: 'side', image: ref('side.png') }] });
    const plan = read('model-plan.json');
    Object.assign(plan, { status: 'READY', builder_id: 'builder-agent', bindings: { request_sha256: sha256File(file('request.json')), sources_sha256: sha256File(file('sources.json')) }, recognizable_features: ['Roof profile'], components: ['Base, columns, roof'], assembly: ['Base before columns before roof'], camera: ['Front to three-quarter'] });
    write('model-plan.json', plan);
  };
  const preview = () => {
    const mp4 = Buffer.alloc(64);
    mp4.writeUInt32BE(24, 0);
    mp4.write('ftyp', 4);
    writeFileSync(file('preview.mp4'), mp4);
    write('video-manifest.json', { schema_version: '1.0', job_id: ID, status: 'RENDERED', video: ref('preview.mp4'), spec: { duration_seconds: 24, fps: 30, width: 1920, height: 1080 }, bindings: { request_sha256: sha256File(file('request.json')), sources_sha256: sha256File(file('sources.json')), model_plan_sha256: sha256File(file('model-plan.json')) } });
    const checks = read('checks.json');
    checks.video = { status: 'RENDERED', manifest: ref('video-manifest.json') };
    write('checks.json', checks);
  };
  const passLocalChecks = () => {
    writeFileSync(file('technical.txt'), 'Synthetic technical evidence for protocol testing only.');
    const checks = read('checks.json');
    for (const station of ['technical', 'visual']) checks[station] = { status: 'PASS', reviewer_id: `${station}-reviewer`, checked_at: TIME, evidence: [ref(station === 'technical' ? 'technical.txt' : 'front.png')], bindings: { request_sha256: sha256File(file('request.json')), sources_sha256: sha256File(file('sources.json')), model_plan_sha256: sha256File(file('model-plan.json')), video_manifest_sha256: sha256File(file('video-manifest.json')) }, findings: [] };
    write('checks.json', checks);
    // Protocol-only positive controls. These records do not claim semantic media quality.
    const inputs = [
      { id: 'photo', role: 'reference', kind: 'image', ...ref('front.png') },
      { id: 'demo', role: 'reference', kind: 'video', ...ref('preview.mp4') },
      { id: 'output', role: 'output', kind: 'video', ...ref('preview.mp4') },
      { id: 'technical', role: 'source', kind: 'document', ...ref('technical.txt') },
      ...['request.json', 'sources.json', 'model-plan.json', 'video-manifest.json'].map((name) => ({ id: name, role: 'source', kind: 'document', ...ref(name) })),
    ];
    const criteria = [
      { id: 'AF', group: 'architectural_fidelity', input_ids: ['photo', 'output'], required_evidence_roles: ['reference', 'output'] },
      { id: 'RD', group: 'reference_demo_match', input_ids: ['demo', 'output'], required_evidence_roles: ['reference', 'output'] },
      { id: 'TE', group: 'technical', input_ids: ['technical'], required_evidence_roles: ['source'] },
    ].map((c) => ({ ...c, required: true, external: false, severity: 'P1', title: 'Synthetic control', expected: ['Synthetic expected result'] }));
    write('review-contract.json', { schema_version: 'review-contract.v1', job_id: ID, revision: 'test-r1', scope: 'SYNTHETIC_PROTOCOL_ONLY', source_checklist: ref('technical.txt'), input_bindings: inputs, criteria });
    for (const input of inputs) write(`access-${input.id}.json`, { schema_version: 'review-access.v1', input_id: input.id, input_sha256: input.sha256, method: input.kind === 'image' ? 'IMAGE_VIEW' : input.kind === 'video' ? 'VIDEO_REVIEW' : 'DOCUMENT_READ', observer_id: 'visual-reviewer', observed_at: TIME, trace_reference: 'synthetic-test-only' });
    write('review-results.json', { schema_version: 'review-results.v1', job_id: ID, contract_sha256: ref('review-contract.json').sha256, status: 'RECORDED', results: criteria.map((c) => ({ criterion_id: c.id, status: 'PASS', reviewer_id: 'visual-reviewer', reviewed_at: TIME, observation: 'Synthetic protocol control only.', limitations: ['Does not assess real media'], shared_dependencies: ['same synthetic fixture'], evidence: c.input_ids.map((id) => ({ input_id: id, locator: 'synthetic fixture', access_record: ref(`access-${id}.json`) })), issues: [] })) });
  };
  return { root, file, read, write, ref, status, ready, preview, passLocalChecks };
}

test('initialization is an unrun DRAFT and never overwrites existing files', (t) => {
  const f = fixture(t);
  const original = readFileSync(f.file('request.json'));
  assert.equal(f.status().stage, 'DRAFT');
  assert.equal(f.read('checks.json').titmas.status, 'NOT_CONNECTED');
  assert.throws(() => initJob(f.root, { id: ID, building: 'Overwrite' }), /will not overwrite/);
  assert.deepEqual(readFileSync(f.file('request.json')), original);
  assert.match(handoffJob(f.root, ID), /1\. 发现层/);
});

test('IDs, traversal, other jobs and symlink escapes are rejected', (t) => {
  const f = fixture(t);
  for (const id of ['../escape', '/absolute', 'a/b', 'UPPER', '-first', 'last-']) assert.throws(() => initJob(f.root, { id, building: 'Bad' }));
  for (const ref of ['/etc/passwd', `jobs/${ID}/../request.json`, 'jobs/other/request.json', `jobs/${ID}\\request.json`]) assert.throws(() => resolveReference(f.root, ID, ref));
  writeFileSync(path.join(f.root, 'outside.txt'), 'outside job');
  symlinkSync(path.join(f.root, 'outside.txt'), f.file('escape.txt'));
  assert.throws(() => resolveReference(f.root, ID, `jobs/${ID}/escape.txt`), /escapes/);
  mkdirSync(path.join(f.root, 'artifacts'));
  writeFileSync(path.join(f.root, 'artifacts', 'allowed.txt'), 'allowed');
  assert.equal(resolveReference(f.root, ID, 'artifacts/allowed.txt'), realpathSync(path.join(f.root, 'artifacts', 'allowed.txt')));
});

test('one view is insufficient; two attributable distinct views and a bound plan are ready to build', (t) => {
  const f = fixture(t);
  f.ready();
  assert.equal(f.status().stage, 'READY_TO_BUILD');
  assert.equal(f.status().gates.sources, true);
  assert.equal(f.status().ready_for_user_review, false);
  const sources = f.read('sources.json');
  sources.views.pop();
  f.write('sources.json', sources);
  const model = f.read('model-plan.json');
  model.bindings.sources_sha256 = sha256File(f.file('sources.json'));
  f.write('model-plan.json', model);
  assert.equal(f.status().stage, 'NEEDS_REFERENCE');
  assert.equal(f.status().gates.sources, false);
});

test('USER_PROVIDED references preserve original provenance without inventing a URL', (t) => {
  const f = fixture(t);
  f.ready('USER_PROVIDED');
  assert.equal(f.status().stage, 'READY_TO_BUILD');
  assert.equal(f.read('sources.json').entries[0].url, undefined);
  const sources = f.read('sources.json');
  delete sources.entries[0].provenance.task_id;
  f.write('sources.json', sources);
  assert.equal(f.status().gates.sources, false);
  assert.ok(f.status().blockers.some((issue) => issue.code === 'SOURCE_PROVENANCE_INCOMPLETE'));
});

test('unknown building location or era cannot enter construction', (t) => {
  const f = fixture(t);
  f.ready();
  for (const field of ['location', 'era']) {
    const request = f.read('request.json');
    request.building = { name: '测试建筑', location: '实际地点', era: '实际版本', [field]: 'UNKNOWN' };
    f.write('request.json', request);
    assert.equal(f.status().stage, 'NEEDS_REVISION');
    assert.ok(f.status().blockers.some((issue) => issue.code === 'BUILDING_IDENTITY_UNRESOLVED'));
    assert.equal(f.status().gates.sources, false);
  }
});

test('valid local checks and rendered video remain PREVIEW_ONLY without TITMAS', (t) => {
  const f = fixture(t);
  f.ready();
  f.preview();
  f.passLocalChecks();
  const result = f.status();
  assert.equal(result.stage, 'PREVIEW_ONLY');
  assert.deepEqual(result.gates, { sources: true, model_plan: true, technical: true, visual: true, titmas: false, video: true });
  assert.equal(result.ready_for_user_review, false);
  assert.deepEqual(result.blockers.map((issue) => issue.code), ['TITMAS_NOT_CONNECTED']);
});

test('handwritten TITMAS PASS and invented connector cannot open the release gate', (t) => {
  const f = fixture(t);
  f.ready();
  f.preview();
  f.passLocalChecks();
  const checks = f.read('checks.json');
  checks.titmas.status = 'PASS';
  checks.titmas.connector_id = 'invented-trusted-service';
  checks.titmas.independent_verification.status = 'PASS';
  f.write('checks.json', checks);
  const result = f.status();
  assert.equal(result.stage, 'NEEDS_REVISION');
  assert.equal(result.gates.titmas, false);
  assert.equal(result.ready_for_user_review, false);
  assert.ok(result.blockers.some((issue) => issue.code === 'UNTRUSTED_TITMAS_ASSERTION'));
});

test('changed source or video bytes invalidate previously passing evidence', (t) => {
  const f = fixture(t);
  f.ready();
  f.preview();
  f.passLocalChecks();
  const original = readFileSync(f.file('sources.json'));
  writeFileSync(f.file('sources.json'), Buffer.concat([original, Buffer.from('\n')]));
  let result = f.status();
  assert.equal(result.stage, 'NEEDS_REVISION');
  assert.equal(result.gates.technical, false);
  assert.equal(result.gates.visual, false);
  assert.ok(result.blockers.some((issue) => issue.code === 'STALE_HASH_BINDING'));
  writeFileSync(f.file('sources.json'), original);
  writeFileSync(f.file('preview.mp4'), 'changed video bytes');
  result = f.status();
  assert.equal(result.gates.video, false);
  assert.equal(result.gates.visual, false);
  assert.equal(result.stage, 'NEEDS_REVISION');
  assert.ok(result.blockers.some((issue) => issue.code === 'INVALID_REFERENCE'));
});

test('builder cannot sign the independent visual check', (t) => {
  const f = fixture(t);
  f.ready();
  f.preview();
  f.passLocalChecks();
  const checks = f.read('checks.json');
  checks.visual.reviewer_id = 'builder-agent';
  f.write('checks.json', checks);
  const result = f.status();
  assert.equal(result.stage, 'NEEDS_REVISION');
  assert.equal(result.gates.visual, false);
  assert.ok(result.blockers.some((issue) => issue.code === 'BUILDER_SELF_SIGNED_VISUAL'));
});

test('missing files, absent visual evidence and UNKNOWN cannot become completed checks', (t) => {
  const f = fixture(t);
  f.ready();
  f.preview();
  f.passLocalChecks();
  const checks = f.read('checks.json');
  checks.technical.status = 'UNKNOWN';
  checks.visual.evidence = [];
  f.write('checks.json', checks);
  let result = f.status();
  assert.equal(result.gates.technical, false);
  assert.equal(result.gates.visual, false);
  assert.equal(result.ready_for_user_review, false);
  rmSync(f.file('side.png'));
  result = f.status();
  assert.equal(result.gates.sources, false);
  assert.equal(result.stage, 'NEEDS_REVISION');
});

test('renaming the request invalidates every downstream identity binding', (t) => {
  const f = fixture(t);
  f.ready();
  f.preview();
  f.passLocalChecks();
  assert.equal(f.status().stage, 'PREVIEW_ONLY');
  const request = f.read('request.json');
  request.building.name = 'Different building';
  f.write('request.json', request);
  const result = f.status();
  assert.equal(result.stage, 'NEEDS_REVISION');
  assert.deepEqual(result.gates, { sources: false, model_plan: false, technical: false, visual: false, titmas: false, video: false });
  for (const station of ['discovery', 'construction', 'technical', 'visual', 'video']) assert.ok(result.blockers.some((issue) => issue.station === station && issue.code === 'STALE_HASH_BINDING' && issue.detail.includes('request identity')));
});


test('legacy visual PASS cannot pass without scoped criteria and real input access records', (t) => {
  const f = fixture(t); f.ready(); f.preview(); f.passLocalChecks();
  rmSync(f.file('review-contract.json'));
  const result = f.status();
  assert.equal(result.stage, 'NEEDS_REVISION');
  assert.equal(result.gates.visual, false);
  assert.ok(result.blockers.some((i) => i.code === 'SCOPED_REVIEW_NOT_READY'));
});

test('nested provenance, source snapshot and render evidence are checked independently of their parent files', (t) => {
  const f = fixture(t); f.ready('USER_PROVIDED'); f.preview(); f.passLocalChecks();
  writeFileSync(f.file('nested.txt'), 'original');
  const source = f.read('sources.json'); source.entries[0].provenance.evidence = f.ref('nested.txt'); f.write('sources.json', source);
  const model = f.read('model-plan.json'); model.source_snapshot = f.ref('nested.txt'); f.write('model-plan.json', model);
  const video = f.read('video-manifest.json'); video.render_evidence = f.ref('nested.txt'); video.source_snapshot = f.ref('nested.txt'); f.write('video-manifest.json', video);
  const checks = f.read('checks.json'); checks.video.manifest = f.ref('video-manifest.json'); f.write('checks.json', checks);
  writeFileSync(f.file('nested.txt'), 'changed behind unchanged parent references');
  const result = f.status();
  for (const station of ['discovery', 'construction', 'video']) assert.ok(result.blockers.some((i) => i.code === 'INVALID_REFERENCE' && i.station === station));
  assert.equal(result.gates.sources, false); assert.equal(result.gates.model_plan, false); assert.equal(result.gates.video, false);
});


test('switching the current output while retaining old files cannot reuse the old scoped review', (t) => {
  const f = fixture(t); f.ready(); f.preview(); f.passLocalChecks();
  assert.equal(f.status().gates.visual, true);
  writeFileSync(f.file('new-preview.mp4'), Buffer.concat([readFileSync(f.file('preview.mp4')), Buffer.from('new-output')]));
  const video = f.read('video-manifest.json'); video.video = f.ref('new-preview.mp4'); f.write('video-manifest.json', video);
  const checks = f.read('checks.json'); checks.video.manifest = f.ref('video-manifest.json');
  for (const station of ['technical', 'visual']) checks[station].bindings.video_manifest_sha256 = f.ref('video-manifest.json').sha256;
  f.write('checks.json', checks);
  const result = f.status();
  assert.equal(result.gates.video, true); // New file is a valid container; old review is not its approval.
  assert.equal(result.gates.visual, false); assert.equal(result.stage, 'NEEDS_REVISION');
  assert.ok(result.blockers.some((i) => i.code === 'REVIEW_JOB_BINDING_MISSING' || i.code === 'REVIEW_OUTPUT_NOT_COVERED'));
});
