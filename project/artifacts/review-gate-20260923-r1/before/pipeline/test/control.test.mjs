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
