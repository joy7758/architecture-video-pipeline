#!/usr/bin/env node
/**
 * Deterministic local renderer. Runs against an already started localhost server.
 * Each frame is explicitly sought, saved as PNG, then encoded at fixed FPS.
 * Existing runs are never overwritten. Unsupported building adapters fail closed.
 */
import { createHash, randomUUID } from 'node:crypto';
import { createWriteStream } from 'node:fs';
import { access, copyFile, mkdir, readFile, readdir, realpath, writeFile } from 'node:fs/promises';
import { homedir } from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const hash = (data) => createHash('sha256').update(data).digest('hex');
if (process.argv.includes('--help') || process.argv.includes('-h')) {
  console.log(`Usage: node pipeline/render-video.mjs [options]

Deterministically capture the supported guanque adapter from an existing local server.
The output is a new directory under artifacts/pipeline/guanque-pilot/ on every run.

  --config PATH   Shot config; default pipeline/video/guanque-pilot.json
  --app-root PATH App source and built dist root; default app (use a fixed snapshot for parallel work)
  --url URL       HTTP localhost server; default http://127.0.0.1:4188/
  --width N       Even video width; config default 1080
  --height N      Even video height; config default 1920
  --fps N         Integer frame rate; config default 30
  --smoke         Defaults to 360x640 and 4 FPS; retains the 24-second shot timeline
  --help, -h      Show this help without launching a browser

Prerequisites: production build, running localhost server, Chrome, Playwright,
ffmpeg with libx264, and ffprobe. No dependencies are installed by this command.
Runtime overrides: ARCHITECTURE_CHROME_PATH, ARCHITECTURE_PLAYWRIGHT_PATH.
Successful file checks return TECHNICAL_PASS_CONTENT_REVIEW_PENDING, not publication approval.`);
  process.exit(0);
}
const options = { config: 'pipeline/video/guanque-pilot.json', url: 'http://127.0.0.1:4188/' };
for (let i = 2; i < process.argv.length; i++) {
  const flag = process.argv[i];
  if (flag === '--smoke') { options.smoke = true; continue; }
  if (!['--config', '--app-root', '--url', '--width', '--height', '--fps'].includes(flag) || !process.argv[i + 1]) {
    throw new Error(`Unknown or incomplete argument: ${flag}`);
  }
  options[flag.slice(2)] = process.argv[++i];
}
const appRoot = await realpath(path.resolve(root, options['app-root'] ?? 'app'));
const configPath = path.resolve(root, options.config);
const config = JSON.parse(await readFile(configPath, 'utf8'));
const url = new URL(options.url);
if (!['127.0.0.1', 'localhost', '[::1]'].includes(url.hostname) || url.protocol !== 'http:' || url.username || url.password) {
  throw new Error('Video capture requires an uncredentialed HTTP localhost URL.');
}
url.searchParams.set('export', '1');
if (config.schemaVersion !== 'architecture-film.v1' || config.adapterId !== 'guanque') {
  throw new Error('UNSUPPORTED_ADAPTER: this renderer currently implements only guanque.');
}
if (config.audio !== 'silent') throw new Error('Only silent local exports are supported.');
const width = Number(options.width ?? (options.smoke ? 360 : config.width));
const height = Number(options.height ?? (options.smoke ? 640 : config.height));
const fps = Number(options.fps ?? (options.smoke ? 4 : config.fps));
if (![width, height].every((v) => Number.isInteger(v) && v >= 128 && v <= 3840 && v % 2 === 0)) {
  throw new Error('Width and height must be even integers within [128, 3840].');
}
if (!Number.isInteger(fps) || fps < 1 || fps > 60) throw new Error('FPS must be an integer within [1, 60].');
const frames = config.durationSeconds * fps;
if (!Number.isInteger(frames) || frames < 1 || frames > 36000) throw new Error('Invalid or excessive frame count.');
function validatePose(pose) {
  if (!pose || !Number.isFinite(pose.progress) || pose.progress < 0 || pose.progress > 1) throw new Error('Invalid progress.');
  if (![pose.position, pose.target].every((v) => Array.isArray(v) && v.length === 3 && v.every(Number.isFinite))) throw new Error('Invalid camera vectors.');
  if (pose.position.every((v, i) => v === pose.target[i])) throw new Error('Camera cannot equal target.');
}
if (!Array.isArray(config.shots) || config.shots.length === 0) throw new Error('Shots are required.');
let nextStart = 0;
for (const shot of config.shots) {
  if (shot.start !== nextStart || !Number.isFinite(shot.end) || shot.end <= shot.start || typeof shot.label !== 'string') throw new Error('Shots must be positive, contiguous and labelled.');
  validatePose(shot.from); validatePose(shot.to); nextStart = shot.end;
}
if (nextStart !== config.durationSeconds) throw new Error('Shot durations must match durationSeconds.');

function frameAt(index) {
  const seconds = index / fps;
  const shot = config.shots.find((s) => seconds >= s.start && seconds < s.end) ?? config.shots.at(-1);
  const t = Math.max(0, Math.min(1, (seconds - shot.start) / (shot.end - shot.start)));
  const cameraT = t * t * (3 - 2 * t);
  const lerp = (a, b, amount) => a + (b - a) * amount;
  return {
    index, seconds, shotId: shot.id, label: shot.label,
    pose: {
      progress: lerp(shot.from.progress, shot.to.progress, t),
      position: shot.from.position.map((v, i) => lerp(v, shot.to.position[i], cameraT)),
      target: shot.from.target.map((v, i) => lerp(v, shot.to.target[i], cameraT)),
    },
  };
}

async function snapshotSources() {
  const files = [];
  async function walk(dir) {
    for (const entry of (await readdir(dir, { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name))) {
      if (entry.name.startsWith('._') || entry.name === '.DS_Store') continue;
      const filename = path.join(dir, entry.name);
      if (entry.isDirectory()) await walk(filename); else if (entry.isFile()) files.push(filename);
    }
  }
  await walk(path.join(appRoot, 'src'));
  await walk(path.join(appRoot, 'dist'));
  files.push(configPath, fileURLToPath(import.meta.url));
  for (const file of ['index.html', 'package.json', 'package-lock.json', 'vite.config.ts', 'tsconfig.json']) files.push(path.join(appRoot, file));
  const entries = await Promise.all([...new Set(files)].sort().map(async (file) => {
    const relative = path.relative(appRoot, file);
    const inApp = relative !== '..' && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative);
    return { path: inApp ? `app/${relative}` : path.relative(root, file), sha256: hash(await readFile(file)) };
  }));
  entries.sort((a, b) => a.path.localeCompare(b.path));
  return { source_root: appRoot, sha256: hash(JSON.stringify(entries)), files: entries };
}
async function executable(command, args, logfile) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, { cwd: root, stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '', stderr = '';
    const log = logfile ? createWriteStream(logfile, { flags: 'wx' }) : null;
    child.stdout.on('data', (chunk) => { stdout += chunk; log?.write(chunk); });
    child.stderr.on('data', (chunk) => { stderr += chunk; log?.write(chunk); });
    child.on('error', reject);
    child.on('close', (code) => {
      log?.end();
      if (code === 0) resolve(stdout || stderr); else reject(new Error(`${command} exited ${code}: ${stderr.slice(-1600)}`));
    });
  });
}
async function loadPlaywright() {
  const candidates = [process.env.ARCHITECTURE_PLAYWRIGHT_PATH, path.join(appRoot, 'node_modules/playwright/index.mjs'), path.join(homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright/index.js')].filter(Boolean);
  for (const candidate of candidates) {
    try { await access(candidate); const module = await import(pathToFileURL(candidate).href); return module.chromium ? module : module.default; } catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  throw new Error('Playwright runtime unavailable. Set ARCHITECTURE_PLAYWRIGHT_PATH to an installed module; no install is performed.');
}

const runId = `${new Date().toISOString().replaceAll(':', '-').replaceAll('.', '-')}-${options.smoke ? 'smoke' : 'film'}-${randomUUID().slice(0, 8)}`;
const out = path.join(root, 'artifacts/pipeline/guanque-pilot', runId);
await mkdir(path.dirname(out), { recursive: true }); await mkdir(out);
await mkdir(path.join(out, 'frames')); await mkdir(path.join(out, 'previews'));
const json = async (name, value) => writeFile(path.join(out, name), `${JSON.stringify(value, null, 2)}\n`, { flag: 'wx' });
const manifest = {
  schemaVersion: 'architecture-video-run.v1', schema_version: 'architecture-video-run.v1', runId, adapterId: config.adapterId, title: config.title,
  status: 'RUNNING', contentReview: 'NOT_RUN', publication: 'NOT_RUN', startedAt: new Date().toISOString(),
  source_root: appRoot,
  input: { appRoot, sourceMode: options['app-root'] ? 'EXPLICIT_APP_ROOT' : 'WORKSPACE_APP', configPath: path.relative(root, configPath), configSha256: hash(await readFile(configPath)), url: url.href },
  capture: { width, height, fps, requestedFrames: frames, capturedFrames: 0, durationSeconds: config.durationSeconds, mode: options.smoke ? 'smoke' : 'film', dpr: 1, audio: 'silent' },
  assemblySemantics: config.assemblySemantics,
  servedBundleVerified: false,
  browserErrors: [], networkErrors: [], consoleWarnings: [], frameRepeats: [],
};
let browser;
console.log(`OUTPUT ${out}`);
try {
  manifest.sourceBefore = (await snapshotSources()); await json('source-before.json', manifest.sourceBefore);
  await json('config-resolved.json', { ...config, width, height, fps });
  const exporterBytes = await readFile(fileURLToPath(import.meta.url));
  await writeFile(path.join(out, 'exporter-source.mjs'), exporterBytes, { flag: 'wx' });
  manifest.exporter = { path: 'exporter-source.mjs', sha256: hash(exporterBytes) };
  // Bind the selected filesystem snapshot to the bytes actually served. Merely
  // passing --app-root alongside an unrelated localhost URL is not sufficient.
  const serverBase = new URL('.', url);
  const bundleFiles = manifest.sourceBefore.files.filter((entry) => entry.path.startsWith('app/dist/'))
    .map((entry) => ({ path: entry.path.slice('app/dist/'.length), sha256: entry.sha256 }));
  const expectedBundle = new Map(bundleFiles.map((entry) => [entry.path, entry.sha256]));
  if (!expectedBundle.has('index.html')) throw new Error('Selected app root has no production dist/index.html.');
  manifest.servedBundle = { expectedFingerprint: hash(JSON.stringify(bundleFiles)), preflight: [], browserResponses: [] };
  await Promise.all(bundleFiles.map(async (entry) => {
    try {
      const fileUrl = new URL(entry.path.split('/').map(encodeURIComponent).join('/'), serverBase);
      const response = await fetch(fileUrl, { redirect: 'error', signal: AbortSignal.timeout(30000) });
      const actualSha256 = hash(Buffer.from(await response.arrayBuffer()));
      manifest.servedBundle.preflight.push({ path: entry.path, expectedSha256: entry.sha256, actualSha256, httpStatus: response.status, equal: response.ok && actualSha256 === entry.sha256 });
    } catch (error) {
      manifest.servedBundle.preflight.push({ path: entry.path, expectedSha256: entry.sha256, equal: false, error: error.message });
    }
  }));
  manifest.servedBundle.preflight.sort((a, b) => a.path.localeCompare(b.path));
  if (manifest.servedBundle.preflight.some((entry) => !entry.equal)) throw new Error('SERVED_BUNDLE_MISMATCH: localhost files differ from selected app root dist.');
  manifest.ffmpegVersion = (await executable('ffmpeg', ['-version'])).split('\n')[0];
  const { chromium } = await loadPlaywright();
  browser = await chromium.launch({ headless: true, executablePath: process.env.ARCHITECTURE_CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', args: ['--disable-background-timer-throttling', '--disable-renderer-backgrounding'] });
  manifest.browserVersion = browser.version();
  const context = await browser.newContext({ viewport: { width, height }, deviceScaleFactor: 1, reducedMotion: 'reduce', locale: 'zh-CN', colorScheme: 'light' });
  await context.route('**/*', async (route) => {
    const requestUrl = new URL(route.request().url());
    if (requestUrl.origin === url.origin || ['data:', 'blob:'].includes(requestUrl.protocol)) await route.continue();
    else { manifest.networkErrors.push(`BLOCKED_NONLOCAL ${requestUrl.origin}`); await route.abort(); }
  });
  const page = await context.newPage();
  const responseChecks = [];
  page.on('response', (response) => {
    const resourceType = response.request().resourceType();
    if (!['document', 'script', 'stylesheet'].includes(resourceType)) return;
    const check = (async () => {
      const responseUrl = new URL(response.url());
      const sameBase = responseUrl.origin === serverBase.origin && responseUrl.pathname.startsWith(serverBase.pathname);
      let filename = sameBase ? decodeURIComponent(responseUrl.pathname.slice(serverBase.pathname.length)) : '';
      if (!filename || filename.endsWith('/')) filename += 'index.html';
      const expectedSha256 = expectedBundle.get(filename);
      const actualSha256 = hash(await response.body());
      manifest.servedBundle.browserResponses.push({ path: filename, resourceType, expectedSha256: expectedSha256 ?? null, actualSha256, httpStatus: response.status(), equal: sameBase && response.ok() && !!expectedSha256 && actualSha256 === expectedSha256 });
    })().catch((error) => {
      manifest.servedBundle.browserResponses.push({ url: response.url(), resourceType, equal: false, error: error.message });
    });
    responseChecks.push(check);
  });
  async function verifyLoadedBundle() {
    await Promise.all(responseChecks);
    const responses = manifest.servedBundle.browserResponses;
    manifest.servedBundleVerified = responses.some((entry) => entry.resourceType === 'document') &&
      responses.some((entry) => entry.resourceType === 'script') && responses.every((entry) => entry.equal);
    if (!manifest.servedBundleVerified) throw new Error('SERVED_BUNDLE_MISMATCH: actual browser document/JS/CSS differs from selected app root dist.');
  }
  page.on('pageerror', (error) => manifest.browserErrors.push(error.message));
  page.on('console', (message) => {
    if (message.type() === 'error') manifest.browserErrors.push(message.text());
    else if (message.type() === 'warning') manifest.consoleWarnings.push(message.text());
  });
  page.on('requestfailed', (request) => manifest.networkErrors.push(`${request.method()} ${request.url()} ${request.failure()?.errorText}`));
  page.on('response', (response) => { if (response.status() >= 400) manifest.networkErrors.push(`HTTP ${response.status()} ${response.url()}`); });
  const response = await page.goto(url.href, { waitUntil: 'networkidle', timeout: 90000 });
  if (!response?.ok()) throw new Error(`Capture page failed: HTTP ${response?.status()}`);
  await verifyLoadedBundle();
  await page.waitForFunction(() => window.__ARCHITECTURE_EXPORT__?.ready === true, undefined, { timeout: 90000 });
  await page.evaluate(() => document.fonts.ready);
  const contract = await page.evaluate(() => ({ version: window.__ARCHITECTURE_EXPORT__.version, adapterId: window.__ARCHITECTURE_EXPORT__.adapterId, controls: document.querySelectorAll('button,input,a').length }));
  if (contract.version !== 'architecture-export.v1' || contract.adapterId !== config.adapterId || contract.controls !== 0) throw new Error('Export contract or clean-film surface mismatch.');
  manifest.contract = contract;
  async function seek(frame) {
    return page.evaluate(({ pose, label }) => {
      document.querySelector('.film-phase').textContent = label;
      return window.__ARCHITECTURE_EXPORT__.setFrame(pose);
    }, frame);
  }
  async function capture(frame, filename) {
    const stats = await seek(frame);
    if (stats.width !== width || stats.height !== Math.round(height * .73)) {
      // Canvas spans 73% of the film height; actual CSS rounding may differ by one.
      if (stats.width !== width || Math.abs(stats.height - height * .73) > 1) throw new Error('Unexpected render canvas dimensions.');
    }
    const png = await page.screenshot({ type: 'png', path: filename, animations: 'disabled', caret: 'hide' });
    return { sha256: hash(png), stats };
  }
  for (const index of [...new Set([0, Math.floor(frames / 2), frames - 1])]) {
    const frame = frameAt(index);
    const first = await capture(frame, path.join(out, 'previews', `repeat-${index}-a.png`));
    await seek(frameAt((index + Math.floor(frames / 3)) % frames));
    const second = await capture(frame, path.join(out, 'previews', `repeat-${index}-b.png`));
    const result = { index, firstSha256: first.sha256, repeatedSha256: second.sha256, equal: first.sha256 === second.sha256 };
    manifest.frameRepeats.push(result);
    if (!result.equal) throw new Error(`Frame determinism failed at ${index}.`);
  }
  const frameRecords = [];
  for (let index = 0; index < frames; index++) {
    const frame = frameAt(index);
    const filename = `frame-${String(index).padStart(6, '0')}.png`;
    const result = await capture(frame, path.join(out, 'frames', filename));
    frameRecords.push({ ...frame, file: `frames/${filename}`, ...result });
    manifest.capture.capturedFrames++;
    if (index % Math.max(fps * 2, 1) === 0 || index === frames - 1) console.log(`FRAMES ${index + 1}/${frames}`);
  }
  await json('frame-index.json', frameRecords);
  for (const [label, index] of [['first', 0], ['middle', Math.floor(frames / 2)], ['last', frames - 1]]) await copyFile(path.join(out, frameRecords[index].file), path.join(out, 'previews', `${label}.png`));
  await copyFile(path.join(out, frameRecords[0].file), path.join(out, 'cover.png'));
  await verifyLoadedBundle();
  await browser.close(); browser = undefined;
  const video = path.join(out, 'guanque-pilot.mp4');
  await executable('ffmpeg', ['-hide_banner', '-nostdin', '-n', '-framerate', String(fps), '-start_number', '0', '-i', path.join(out, 'frames/frame-%06d.png'), '-frames:v', String(frames), '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', video], path.join(out, 'ffmpeg.log'));
  const metadata = JSON.parse(await executable('ffprobe', ['-v', 'error', '-count_frames', '-show_entries', 'stream=codec_name,codec_type,pix_fmt,width,height,r_frame_rate,nb_read_frames,nb_frames,duration:format=duration,size', '-of', 'json', video]));
  await json('ffprobe.json', metadata); manifest.ffprobe = metadata;
  const stream = metadata.streams.find((s) => s.codec_type === 'video');
  const [rateNumerator, rateDenominator] = stream.r_frame_rate.split('/').map(Number);
  if (metadata.streams.length !== 1 || stream.codec_name !== 'h264' || stream.pix_fmt !== 'yuv420p' || stream.width !== width || stream.height !== height || Number(stream.nb_read_frames) !== frames || rateNumerator / rateDenominator !== fps || Math.abs(Number(metadata.format.duration) - config.durationSeconds) > 1 / fps) throw new Error('Encoded MP4 metadata mismatch.');
  const videoBytes = await readFile(video);
  manifest.output = { video: 'guanque-pilot.mp4', cover: 'cover.png', sha256: hash(videoBytes), coverSha256: hash(await readFile(path.join(out, 'cover.png'))), bytes: videoBytes.length, faststart: videoBytes.indexOf(Buffer.from('moov')) >= 0 && videoBytes.indexOf(Buffer.from('moov')) < videoBytes.indexOf(Buffer.from('mdat')) };
  if (!manifest.output.faststart) throw new Error('MP4 faststart atom ordering failed.');
  manifest.sourceAfter = await snapshotSources(); await json('source-after.json', manifest.sourceAfter);
  manifest.sourceUnchanged = manifest.sourceBefore.sha256 === manifest.sourceAfter.sha256;
  if (!manifest.sourceUnchanged) throw new Error('SOURCE_HASH_CHANGED during capture.');
  if (manifest.browserErrors.length || manifest.networkErrors.length) throw new Error('Browser or network errors occurred; inspect run.json.');
  manifest.status = 'TECHNICAL_PASS_CONTENT_REVIEW_PENDING';
  console.log(`VIDEO ${video}`);
} catch (error) {
  manifest.status = 'FAILED'; manifest.failure = error.stack || String(error); process.exitCode = 1;
  console.error(error.message);
} finally {
  await browser?.close();
  manifest.finishedAt = new Date().toISOString();
  await json('run.json', manifest);
  console.log(`RESULT ${manifest.status}`);
}
