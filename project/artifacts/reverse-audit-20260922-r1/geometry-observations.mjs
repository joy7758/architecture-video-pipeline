/** Read-only geometry audit. Run: node artifacts/reverse-audit-20260922-r1/geometry-observations.mjs
 * Reads the delivery-bound source snapshot, compiles TypeScript only in memory,
 * and examines each source vertex after its local transform. Writes nothing.
 * No browser, textures, rendering, external service, or measured real-world survey.
 */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const workspace = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const app = path.join(workspace, 'app');
const require = createRequire(path.join(app, 'package.json'));
const ts = require('typescript');
const url = value => pathToFileURL(value).href;
const three = url(path.join(app, 'node_modules/three/build/three.module.js'));
const utils = url(path.join(app, 'node_modules/three/examples/jsm/utils/BufferGeometryUtils.js'));
const THREE = await import(three);
const snapshot = 'artifacts/pipeline/source-snapshots/2026-09-22T12-27-10-638Z-0fb796b3/app/src/heritage';
const root = path.join(workspace, snapshot);
const compiled = {};
const sha256 = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const sources = [];
for (const name of ['builder', 'facade', 'roof', 'guanque']) {
  const relative = `${snapshot}/${name}.ts`, bytes = fs.readFileSync(path.join(root, `${name}.ts`));
  const current = fs.readFileSync(path.join(app, 'src/heritage', `${name}.ts`));
  sources.push({ path: relative, sha256: sha256(bytes), current_app_sha256: sha256(current), matches_current_app: bytes.equals(current) });
  let src = ts.transpileModule(bytes.toString('utf8'), { compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ES2022 } }).outputText;
  src = src.replaceAll('"three"', JSON.stringify(three)).replaceAll("'three'", JSON.stringify(three))
    .replaceAll('"three/examples/jsm/utils/BufferGeometryUtils.js"', JSON.stringify(utils));
  for (const dependency of ['builder', 'facade', 'roof']) if (compiled[dependency]) {
    src = src.replaceAll(`'./${dependency}'`, JSON.stringify(compiled[dependency]))
      .replaceAll(`"./${dependency}"`, JSON.stringify(compiled[dependency]));
  }
  compiled[name] = 'data:text/javascript;base64,' + Buffer.from(src).toString('base64');
}
const { HeritageBuilder } = await import(compiled.builder);
const { buildArchitecture, TOWER } = await import(compiled.guanque);
class BoundsBuilder extends HeritageBuilder {
  bounds = new THREE.Box3();
  sourceVerticesVisited = 0;
  componentsVisited = 0;
  add(geometry, material, start, options = {}) {
    const object = new THREE.Object3D();
    object.position.set(...(options.p ?? [0, 0, 0]));
    object.rotation.set(...(options.r ?? [0, 0, 0]));
    object.scale.set(...(options.s ?? [1, 1, 1]));
    object.updateMatrix();
    const positions = geometry.getAttribute('position'), point = new THREE.Vector3();
    for (let index = 0; index < positions.count; index++) {
      point.fromBufferAttribute(positions, index).applyMatrix4(object.matrix);
      this.bounds.expandByPoint(point);
    }
    this.sourceVerticesVisited += positions.count;
    this.componentsVisited++;
  }
}
const builder = new BoundsBuilder({});
buildArchitecture(builder);
const maximum = builder.bounds.max.y, podium = TOWER.halls[0].floor, body = maximum - podium;
const userRatio = 16.5 / 57.4, modelRatio = podium / body;
const sweep = t => 1 - t - .14 * Math.sin(Math.PI * t);
const requestedAnnexRise = 1.18;
const effectiveAnnexRise = Math.min(requestedAnnexRise, 2.3 * sweep(.43) * .96);
console.log(JSON.stringify({
  schema_version: '1.0',
  method: 'Delivery snapshot TypeScript transpiled in memory. Every buildArchitecture source vertex is transformed and inspected; courtyard, textures, plaques, GPU animation and rendering are excluded. All values are scene units unless explicitly labelled.',
  sources,
  components_visited: builder.componentsVisited,
  source_vertices_visited: builder.sourceVerticesVisited,
  bounds: { min: builder.bounds.min.toArray(), max: builder.bounds.max.toArray() },
  height_comparison: {
    datum_y: 0, model_highest_y: maximum, podium_to_first_hall_floor: podium, body_above_first_hall_floor: body,
    model_podium_body_ratio: modelRatio, user_provided_podium_metres: 16.5, user_provided_body_metres: 57.4,
    user_provided_ratio: userRatio, ratio_relative_difference_percent: (modelRatio / userRatio - 1) * 100,
    user_provided_total_metres: 73.9, reference_scale: .4, user_provided_total_scaled: 73.9 * .4,
    meaning: 'The roughly 0.13 percent value compares a code-derived ratio with an unverified user-provided ratio. It is NOT real-world reconstruction accuracy. Ground datum is y=0; below-ground source geometry is excluded from the nominal height comparison.'
  },
  footprint_comparison: {
    lower_hall_width: 15.12, lower_hall_depth: 10.32, lower_hall_ratio: 15.12 / 10.32,
    user_provided_lower_hall_ratio: 37.8 / 25.8,
    upper_hall_width: 11.52, upper_hall_depth: 6.72, upper_hall_ratio: 11.52 / 6.72,
    user_provided_upper_hall_ratio: 28.8 / 16.8,
    terrace_front_width: 34, outer_corridor_column_width: 19.92,
    terrace_to_outer_column_width_ratio: 34 / 19.92,
    highest_gallery_width: 17.6, middle_gallery_width: 17.9,
    gallery_width_ratio: 17.6 / 17.9,
    meaning: 'Hall axis dimensions and gallery dimensions are different quantities. Photo perspectives have not been calibrated; these ratios do not establish actual building dimensions.'
  },
  annex_clamp: {
    requested_rise: requestedAnnexRise, main_roof_rise: 2.3, break_fraction: .43,
    formula: 'min(1.18, (2.3 * (1 - .43 - .14 * sin(pi * .43))) * .96)',
    effective_rise: effectiveAnnexRise, reduction_from_request_percent: (1 - effectiveAnnexRise / requestedAnnexRise) * 100,
    outset: .4, origin: 'guanque.ts:213-214; roof.ts:92-100 and 369-372',
    meaning: 'This is the roof generator effective rise parameter, not a surveyed annex height or a complete measure of visible roof silhouette.'
  },
  status: 'CODE_OBSERVATION_ONLY_NOT_PHOTOGRAMMETRIC_VALIDATION'
}, null, 2));
