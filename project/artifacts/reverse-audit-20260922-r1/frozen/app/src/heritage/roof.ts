/** Deterministic roof surfaces for the photo-informed Guanque exterior.
 * All dimensions are scene units, not a measured architectural reconstruction.
 *
 * Roof contracts:
 * - rings start at the actual inner wall, never at a hidden central ridge;
 * - projections participate in one shared height envelope and footprint;
 * - upper tile faces wind upward; underside faces wind downward;
 * - xieshan has two upper slopes, two closed gables and one lower roof skirt.
 */
import * as THREE from 'three';
import type { HeritageBuilder, Point } from './builder';

/** Side order follows a clockwise turn from the front: +Z, +X, -Z, -X. */
export interface RoofProjection {
  side: 0 | 1 | 2 | 3;
  /** Half-width of the projecting eave, including its overhang. */
  halfWidth: number;
  /** Net projection beyond the main roof's eave, always positive. */
  outset: number;
  /** Projecting ridge height above eaveY, not above the main roof surface. */
  rise?: number;
  /** How far the attachment begins inside the main eave. */
  joinDepth?: number;
}

export interface RingRoofOptions {
  outerX: number;
  outerZ: number;
  innerX: number;
  innerZ: number;
  eaveY: number;
  innerY: number;
  start: number;
  projections?: readonly RoofProjection[];
}

type Cell = { i: number; j: number; used: boolean };
type Edge = [Point, Point];
type Projection = RoofProjection & { halfWidth: number; rise: number; joinDepth: number; ridgeS: number; ridgeHalf: number };
type RoofSurface = {
  outerX: number; outerZ: number; innerX: number; innerZ: number;
  eaveY: number; innerY: number; start: number;
  profile: (t: number) => number;
  projections: readonly RoofProjection[];
  place: (p: Point) => Point;
  xieshan?: boolean;
};
type Height = (x: number, z: number) => number;
const TILE_WIDTH = .22;
const THICKNESS = .19;
const EPS = 1e-7;
const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const smooth = (v: number) => { const t = clamp(v); return t * t * (3 - 2 * t); };
/** Steep upper slope, gently easing toward the eave without a flat outer dish. */
const sweep = (t: number) => 1 - t - .14 * Math.sin(Math.PI * t);
const noise = (n: number) => { const v = Math.sin(n * 31.7 + 9.2) * 43758.5; return v - Math.floor(v); };
const identity = (p: Point): Point => p;

function geometry(positions: number[], indices: number[], role: string) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(positions.flatMap((_, i) => i % 3 === 0 ? [positions[i] * .55, positions[i + 2] * .55] : []), 2));
  g.setIndex(indices); g.computeVertexNormals();
  g.userData.roofPart = role;
  return g;
}

/** Mandatory breakpoints make the rectangular union and inner opening exact. */
function axis(values: number[], spacing = TILE_WIDTH) {
  const knots = [...new Set(values.map(v => Number(v.toFixed(7))))].sort((a, b) => a - b);
  const result: number[] = [];
  for (let i = 0; i < knots.length - 1; i++) {
    const a = knots[i], b = knots[i + 1], count = Math.max(1, Math.ceil((b - a) / spacing));
    for (let j = 0; j < count; j++) result.push(a + (b - a) * j / count);
  }
  result.push(knots[knots.length - 1]); return result;
}

function projectedCoordinates(p: RoofProjection, x: number, z: number, roof: RoofSurface) {
  if (p.side === 0) return { a: x, s: z - roof.outerZ };
  if (p.side === 1) return { a: -z, s: x - roof.outerX };
  if (p.side === 2) return { a: -x, s: -z - roof.outerZ };
  return { a: z, s: -x - roof.outerX };
}
function projectedPoint(p: RoofProjection, a: number, s: number, roof: RoofSurface): [number, number] {
  if (p.side === 0) return [a, roof.outerZ + s];
  if (p.side === 1) return [roof.outerX + s, -a];
  if (p.side === 2) return [-a, -roof.outerZ - s];
  return [-roof.outerX - s, a];
}

function normalizeProjections(roof: RoofSurface): Projection[] {
  return roof.projections.map(p => {
    const span = p.side % 2 ? roof.outerZ : roof.outerX;
    const run = p.side % 2 ? roof.outerX - roof.innerX : roof.outerZ - roof.innerZ;
    const joinDepth = Math.min(Math.max(.15, p.joinDepth ?? run * .86), run * .97);
    const halfWidth = Math.min(Math.max(.35, p.halfWidth), span * .78);
    return { ...p, halfWidth, outset: Math.max(.05, p.outset), joinDepth,
      rise: Math.min(Math.max(.12, p.rise ?? (roof.innerY - roof.eaveY) * .78), (roof.innerY - roof.eaveY) * .96),
      ridgeS: -joinDepth * .22, ridgeHalf: halfWidth * .55 };
  });
}

function makeSurface(roof: RoofSurface) {
  const ps = normalizeProjections(roof);
  const runX = roof.outerX - roof.innerX, runZ = roof.outerZ - roof.innerZ;
  const cornerRise = Math.min(.46, (roof.innerY - roof.eaveY) * .26);
  const main: Height = (x, z) => {
    const t = clamp(Math.max((Math.abs(x) - roof.innerX) / runX, (Math.abs(z) - roof.innerZ) / runZ));
    // Compact support leaves the straight central eave exactly at eaveY. This
    // also makes the projection's outside surface continuous at the main eave.
    const corner = cornerRise * smooth((Math.abs(x) / roof.outerX - .80) / .20)
      * smooth((Math.abs(z) / roof.outerZ - .80) / .20) * t ** 4;
    return roof.eaveY + roof.profile(t) + corner;
  };
  const annex = (p: Projection, x: number, z: number) => {
    const { a, s } = projectedCoordinates(p, x, z, roof);
    const across = Math.max(0, (Math.abs(a) - p.ridgeHalf) / (p.halfWidth - p.ridgeHalf));
    const along = s < p.ridgeS ? (p.ridgeS - s) / (p.ridgeS + p.joinDepth) : (s - p.ridgeS) / (p.outset - p.ridgeS);
    // Lift only the two exposed outer corners. At the two re-entrant main-eave
    // corners (s=0), both lift and its first derivative are zero; attachment
    // valleys and the main roof therefore retain their original continuity.
    const corner = cornerRise * smooth((Math.abs(a) / p.halfWidth - .62) / .38) * smooth(s / p.outset);
    return roof.eaveY + p.rise * sweep(clamp(Math.max(across, along))) + corner;
  };
  const insideMain = (x: number, z: number) => Math.abs(x) <= roof.outerX + EPS && Math.abs(z) <= roof.outerZ + EPS;
  const insideProjection = (p: Projection, x: number, z: number) => {
    const { a, s } = projectedCoordinates(p, x, z, roof);
    return Math.abs(a) <= p.halfWidth + EPS && s >= -p.joinDepth - EPS && s <= p.outset + EPS;
  };
  const inside = (x: number, z: number) => {
    if (roof.innerX > 0 && roof.innerZ > 0 && Math.abs(x) < roof.innerX - EPS && Math.abs(z) < roof.innerZ - EPS) return false;
    return insideMain(x, z) || ps.some(p => insideProjection(p, x, z));
  };
  const height: Height = (x, z) => {
    let h = insideMain(x, z) ? main(x, z) : roof.eaveY;
    for (const p of ps) if (insideProjection(p, x, z)) h = Math.max(h, annex(p, x, z));
    return h;
  };
  const xs = [-roof.outerX, -roof.innerX, 0, roof.innerX, roof.outerX];
  const zs = [-roof.outerZ, -roof.innerZ, 0, roof.innerZ, roof.outerZ];
  for (const p of ps) for (const a of [-p.halfWidth, -p.ridgeHalf, p.ridgeHalf, p.halfWidth]) {
    for (const s of [-p.joinDepth, p.ridgeS, 0, p.outset]) {
      const [x, z] = projectedPoint(p, a, s, roof); xs.push(x); zs.push(z);
    }
  }
  return { ps, main, annex, height, inside, xs: axis(xs), zs: axis(zs) };
}

function normalAt(height: Height, x: number, z: number): Point {
  const step = .003, dx = (height(x + step, z) - height(x - step, z)) / (2 * step), dz = (height(x, z + step) - height(x, z - step)) / (2 * step);
  const scale = 1 / Math.hypot(dx, 1, dz); return [-dx * scale, scale, -dz * scale];
}

/** Shared indexed mesh, then shallow ceramic shells displaced along its normal. */
function buildSheet(b: HeritageBuilder, xs: number[], zs: number[], inside: (x: number, z: number) => boolean,
  height: Height, start: number, place: (p: Point) => Point, role: string, eaves = true,
  closeEdge: (p: Point, q: Point) => boolean = () => true,
  decorateEdge: (p: Point, q: Point) => boolean = closeEdge) {
  const nx = xs.length - 1, nz = zs.length - 1;
  const cells = new Map<string, Cell>(), vertexMap = new Map<string, number>();
  const positions: number[] = [], indices: number[] = [], boundary: Edge[] = [];
  const point = (i: number, j: number): Point => [xs[i], height(xs[i], zs[j]), zs[j]];
  const vertex = (i: number, j: number) => {
    const key = `${i}/${j}`; let n = vertexMap.get(key);
    if (n === undefined) { n = positions.length / 3; vertexMap.set(key, n); positions.push(...place(point(i, j))); }
    return n;
  };
  for (let j = 0; j < nz; j++) for (let i = 0; i < nx; i++) {
    if (!inside((xs[i] + xs[i + 1]) / 2, (zs[j] + zs[j + 1]) / 2)) continue;
    cells.set(`${i}/${j}`, { i, j, used: false });
    const a = vertex(i, j), c = vertex(i, j + 1), d = vertex(i + 1, j + 1), e = vertex(i + 1, j);
    indices.push(a, c, e, e, c, d);
  }
  const shell = geometry(positions, indices, `${role}:top`);
  b.add(shell, 'tile', start, { duration: .023, lift: .55 }); shell.dispose();
  const underside = geometry(positions.map((v, i) => i % 3 === 1 ? v - THICKNESS : v),
    indices.flatMap((_, i) => i % 3 === 0 ? [indices[i], indices[i + 2], indices[i + 1]] : []), `${role}:underside`);
  b.add(underside, 'wood', start, { duration: .023, lift: .55 }); underside.dispose();

  for (const { i, j } of cells.values()) {
    if (!cells.has(`${i}/${j - 1}`)) boundary.push([point(i + 1, j), point(i, j)]);
    if (!cells.has(`${i + 1}/${j}`)) boundary.push([point(i + 1, j + 1), point(i + 1, j)]);
    if (!cells.has(`${i}/${j + 1}`)) boundary.push([point(i, j + 1), point(i + 1, j + 1)]);
    if (!cells.has(`${i - 1}/${j}`)) boundary.push([point(i, j), point(i, j + 1)]);
  }
  const sides: number[] = [], sideIndices: number[] = [];
  for (const [p, q] of boundary) {
    if (!closeEdge(p, q)) continue;
    const n = sides.length / 3;
    sides.push(...place(p), ...place(q), ...place([p[0], p[1] - THICKNESS, p[2]]), ...place([q[0], q[1] - THICKNESS, q[2]]));
    sideIndices.push(n, n + 2, n + 1, n + 1, n + 2, n + 3);
  }
  const fascia = geometry(sides, sideIndices, `${role}:fascia`);
  b.add(fascia, 'jade', start + .014, { duration: .018, lift: .4 }); fascia.dispose();

  let tileIndex = 0;
  for (const cell of cells.values()) {
    if (cell.used) continue;
    const { i, j } = cell, n = normalAt(height, (xs[i] + xs[i + 1]) / 2, (zs[j] + zs[j + 1]) / 2);
    const alongZ = Math.abs(n[2]) >= Math.abs(n[0]);
    const next = cells.get(alongZ ? `${i}/${j + 1}` : `${i + 1}/${j}`);
    let endI = i + 1, endJ = j + 1;
    if (next && !next.used) {
      const nn = normalAt(height, (xs[next.i] + xs[next.i + 1]) / 2, (zs[next.j] + zs[next.j + 1]) / 2);
      if ((Math.abs(nn[2]) >= Math.abs(nn[0])) === alongZ && (alongZ ? nn[2] * n[2] >= 0 : nn[0] * n[0] >= 0)) {
        next.used = true; if (alongZ) endJ++; else endI++;
      }
    }
    cell.used = true;
    const xa = xs[i], xb = xs[endI], za = zs[j], zb = zs[endJ];
    if (xb - xa < .035 || zb - za < .035) continue;
    const tile: number[] = [], faces: number[] = [];
    const across = 4, along = 2;
    for (let v = 0; v <= along; v++) for (let u = 0; u <= across; u++) {
      const a = .045 + .91 * u / across, t = .018 + .964 * v / along;
      const x = xa + (xb - xa) * (alongZ ? a : t), z = za + (zb - za) * (alongZ ? t : a);
      const N = normalAt(height, x, z), off = .012 + .028 * Math.sin(Math.PI * u / across);
      tile.push(...place([x + N[0] * off, height(x, z) + N[1] * off, z + N[2] * off]));
    }
    for (let v = 0; v < along; v++) for (let u = 0; u < across; u++) {
      const a = v * (across + 1) + u, c = a + across + 1;
      if (alongZ) faces.push(a, c, a + 1, a + 1, c, c + 1);
      else faces.push(a, a + 1, c, a + 1, c + 1, c);
    }
    const g = geometry(tile, faces, `${role}:tile`);
    b.add(g, 'tile', start + .024 + noise(tileIndex * 13) * .040, { duration: .013, lift: .34, shade: .93 + noise(tileIndex++) * .10 }); g.dispose();
  }

  if (eaves) {
    // Collinear runs are grouped. Re-entrant projection corners stay exact;
    // Catmull-Rom is never allowed to round a 90-degree footprint corner.
    const groups = new Map<string, Edge[]>();
    for (const e of boundary) {
      if (!decorateEdge(...e)) continue;
      const horizontal = Math.abs(e[0][2] - e[1][2]) < EPS;
      const key = `${horizontal ? 'z' : 'x'}/${(horizontal ? e[0][2] : e[0][0]).toFixed(6)}`;
      if (!groups.has(key)) groups.set(key, []); groups.get(key)!.push(e);
    }
    for (const edges of groups.values()) {
      const horizontal = Math.abs(edges[0][0][2] - edges[0][1][2]) < EPS, coord = horizontal ? 0 : 2;
      const pieces = edges.map(e => [...e].sort((p, q) => p[coord] - q[coord]) as Edge).sort((a, c) => a[0][coord] - c[0][coord]);
      let line: Point[] = [];
      const flush = () => {
        if (line.length > 1) {
          b.tube(line.map(p => place([p[0], p[1] - .095, p[2]])), .075, 'jade', start + .072, { duration: .013 }, Math.max(3, line.length * 2));
          // Sparse real cylindrical rafter tails and ceramic tile-end discs.
          // Their axes follow the slope into the fascia, rather than a row of
          // floating spheres or another horizontal eave band.
          const first = line[0], last = line[line.length - 1], length = last[coord] - first[coord];
          const caps = Math.floor(length / (TILE_WIDTH * 2));
          for (let i = 0; i < caps; i++) {
            const t = (i + .5) / caps, x = first[0] + (last[0] - first[0]) * t, z = first[2] + (last[2] - first[2]) * t;
            const positiveInside = horizontal ? inside(x, z + .04) : inside(x + .04, z);
            const sign = positiveInside ? -1 : 1, ox = horizontal ? 0 : sign, oz = horizontal ? sign : 0;
            const tail = place([x - ox * .48, height(x - ox * .48, z - oz * .48) - THICKNESS - .060, z - oz * .48]);
            const tip = place([x + ox * .025, height(x, z) - THICKNESS - .060, z + oz * .025]);
            const direction = new THREE.Vector3(...tip).sub(new THREE.Vector3(...tail)), span = direction.length();
            const rotation = new THREE.Euler().setFromQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), direction.normalize()));
            const r: Point = [rotation.x, rotation.y, rotation.z];
            if (i % 2 === 0) b.cylinder(.043, .049, span, tail.map((v, j) => (v + tip[j]) / 2) as Point, 'wood', start + .036, { r, duration: .013, shade: 1.03 });
            const cap = place([x + ox * .018, height(x, z) + .012, z + oz * .018]);
            b.cylinder(.055, .055, .034, cap, 'tile', start + .069, { r, duration: .013, shade: .91 });
          }
        }
        line = [];
      };
      for (const e of pieces) {
        if (line.length && Math.abs(line[line.length - 1][coord] - e[0][coord]) > .001) flush();
        if (!line.length) line.push(e[0]); line.push(e[1]);
      }
      flush();
    }
  }
  return { tileCount: tileIndex, boundary, height };
}

function constructSkirt(b: HeritageBuilder, roof: RoofSurface) {
  const surface = makeSurface(roof);
  const closeEdge = (p: Point, q: Point) => !(roof.xieshan && Math.abs(Math.abs(p[2]) - roof.innerZ) < EPS
    && Math.abs(Math.abs(q[2]) - roof.innerZ) < EPS && Math.abs(p[0]) <= roof.innerX + EPS && Math.abs(q[0]) <= roof.innerX + EPS);
  const decorateEdge = (p: Point, q: Point) => {
    const x = (p[0] + q[0]) / 2, z = (p[2] + q[2]) / 2;
    const innerRim = (Math.abs(Math.abs(x) - roof.innerX) < EPS && Math.abs(z) <= roof.innerZ + EPS)
      || (Math.abs(Math.abs(z) - roof.innerZ) < EPS && Math.abs(x) <= roof.innerX + EPS);
    return closeEdge(p, q) && !innerRim;
  };
  buildSheet(b, surface.xs, surface.zs, surface.inside, surface.height, roof.start, roof.place, 'skirt', true, closeEdge, decorateEdge);
  // Hip seams follow the same sampled surface as the roof instead of a second
  // hand-written height formula. Projections may cover part of a hip seam.
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) {
    let points: Point[] = [];
    const flush = () => { if (points.length > 1) b.tube(points, .075, 'tile', roof.start + .074, { duration: .013 }, points.length * 2); points = []; };
    for (let i = 0; i <= 40; i++) {
      const t = i / 40, x = sx * (roof.innerX + (roof.outerX - roof.innerX) * t), z = sz * (roof.innerZ + (roof.outerZ - roof.innerZ) * t);
      if (surface.height(x, z) > surface.main(x, z) + .004) { flush(); continue; }
      points.push(roof.place([x, surface.height(x, z) + .055, z]));
    }
    flush();
  }
  for (const p of surface.ps) {
    // Solve the valley against the original main slope; the same maximum is
    // already used for every board and tile. No hidden second roof is emitted.
    const valley: Point[] = [];
    for (let i = 0; i <= 36; i++) {
      const a = p.halfWidth * (-.995 + 1.99 * i / 36);
      let lo = -p.joinDepth, hi = 0;
      const gap = (s: number) => { const [x, z] = projectedPoint(p, a, s, roof); return surface.annex(p, x, z) - surface.main(x, z); };
      if (gap(lo) > 0 || gap(hi) < 0) continue;
      for (let n = 0; n < 24; n++) { const mid = (lo + hi) / 2; if (gap(mid) > 0) hi = mid; else lo = mid; }
      const [x, z] = projectedPoint(p, a, (lo + hi) / 2, roof); valley.push(roof.place([x, surface.height(x, z) + .03, z]));
    }
    if (valley.length > 2) b.tube(valley, .023, 'tile', roof.start + .075, { duration: .013, shade: .80 }, valley.length * 2);
    const ridge: Point[] = [];
    for (let i = 0; i <= 18; i++) {
      const [x, z] = projectedPoint(p, p.ridgeHalf * (-1 + 2 * i / 18), p.ridgeS, roof);
      if (surface.height(x, z) <= roof.eaveY + p.rise + .015) ridge.push(roof.place([x, surface.height(x, z) + .075, z]));
    }
    if (ridge.length > 1) b.tube(ridge, .09, 'tile', roof.start + .078, { duration: .013 }, ridge.length * 2);
    for (const sign of [-1, 1]) {
      const hip: Point[] = [];
      for (let i = 0; i <= 20; i++) {
        const t = i / 20, a = sign * (p.ridgeHalf + (p.halfWidth - p.ridgeHalf) * t), s = p.ridgeS + (p.outset - p.ridgeS) * t;
        const [hx, hz] = projectedPoint(p, a, s, roof);
        if (surface.height(hx, hz) <= surface.annex(p, hx, hz) + .01) hip.push(roof.place([hx, surface.height(hx, hz) + .045, hz]));
      }
      if (hip.length > 1) b.tube(hip, .055, 'tile', roof.start + .077, { duration: .013 }, hip.length * 2);
      const [x, z] = projectedPoint(p, sign * p.ridgeHalf, p.ridgeS, roof);
      if (surface.height(x, z) > roof.eaveY + p.rise + .015) continue;
      // A restrained paired ceramic ridge-end curl, 0.42 units high. It is
      // anchored to this annex's existing ridge, never a separate roof/animal.
      const outline = new THREE.Shape();
      outline.moveTo(-.11, 0); outline.lineTo(.10, .015);
      outline.bezierCurveTo(.22, .065, .23, .20, .17, .31);
      outline.bezierCurveTo(.15, .37, .10, .42, .055, .405);
      outline.lineTo(.045, .31); outline.bezierCurveTo(.13, .23, .06, .14, -.07, .12);
      outline.closePath();
      const g = new THREE.ExtrudeGeometry(outline, { depth: .14, bevelEnabled: true, bevelSize: .012, bevelThickness: .012, bevelSegments: 1, steps: 1 });
      g.translate(0, 0, -.07);
      const positions = g.getAttribute('position');
      for (let i = 0; i < positions.count; i++) {
        const [gx, gz] = projectedPoint(p, sign * (p.ridgeHalf + positions.getX(i)), p.ridgeS + positions.getZ(i), roof);
        positions.setXYZ(i, ...roof.place([gx, roof.eaveY + p.rise + .075 + positions.getY(i), gz]));
      }
      // Reflection at the left ridge end must preserve outward winding.
      if (sign < 0) for (let i = 0; i < positions.count; i += 3) {
        const q: Point = [positions.getX(i + 1), positions.getY(i + 1), positions.getZ(i + 1)];
        positions.setXYZ(i + 1, positions.getX(i + 2), positions.getY(i + 2), positions.getZ(i + 2));
        positions.setXYZ(i + 2, ...q);
      }
      g.computeVertexNormals(); g.userData.roofPart = 'annex-ridge-end';
      b.add(g, 'tile', roof.start + .081, { duration: .013, shade: .93 }); g.dispose();
    }
  }
}

/** A continuous waist/corridor roof between two rectangles; no central ridge. */
export function ringRoof(b: HeritageBuilder, options: RingRoofOptions) {
  const { outerX, outerZ, innerX, innerZ, eaveY, innerY, start, projections = [] } = options;
  if (!(outerX > innerX && outerZ > innerZ && innerY > eaveY && innerX > 0 && innerZ > 0)) throw new Error('ringRoof requires outer > inner and innerY > eaveY');
  constructSkirt(b, { outerX, outerZ, innerX, innerZ, eaveY, innerY, start, projections, place: identity,
    profile: t => (innerY - eaveY) * sweep(t) });
}

/** Complete hip roof, or a xieshan roof when ornaments=true. */
export function hipRoof(b: HeritageBuilder, y: number, w: number, d: number, h: number, start: number,
  center: Point = [0, 0, 0], angle = 0, ornaments = false, projections: readonly RoofProjection[] = []) {
  const place = (p: Point): Point => [p[0] * Math.cos(angle) + p[2] * Math.sin(angle) + center[0], p[1] + center[1], p[2] * Math.cos(angle) - p[0] * Math.sin(angle) + center[2]];
  const ridge = w * (ornaments ? .62 : .42), breakFraction = ornaments ? .43 : 0, breakZ = d * breakFraction;
  const shoulder = y + h * sweep(breakFraction);
  constructSkirt(b, { outerX: w, outerZ: d, innerX: ridge, innerZ: breakZ, eaveY: y, innerY: shoulder,
    start, projections, place, xieshan: ornaments, profile: t => h * sweep(breakFraction + (1 - breakFraction) * t) });
  if (ornaments) {
    const upperHeight: Height = (_x, z) => y + h * sweep(clamp(Math.abs(z) / d));
    buildSheet(b, axis([-ridge, 0, ridge]), axis([-breakZ, 0, breakZ]), () => true,
      upperHeight, start + .007, place, 'upper-slopes', false,
      (p, q) => !(Math.abs(Math.abs(p[2]) - breakZ) < EPS && Math.abs(Math.abs(q[2]) - breakZ) < EPS));
    // Each gable exactly shares its curved top with the upper roof and its
    // horizontal bottom with the skirt. It is a wall, not an extra narrow roof.
    for (const sign of [-1, 1]) {
      const zs = axis([-breakZ, 0, breakZ]), positions: number[] = [], indices: number[] = [];
      for (const z of zs) positions.push(...place([sign * ridge, shoulder, z]), ...place([sign * ridge, Math.max(shoulder, upperHeight(sign * ridge, z) - THICKNESS), z]));
      for (let j = 0; j < zs.length - 1; j++) {
        const a = j * 2;
        if (sign > 0) indices.push(a, a + 1, a + 2, a + 1, a + 3, a + 2);
        else indices.push(a, a + 2, a + 1, a + 1, a + 2, a + 3);
      }
      const g = geometry(positions, indices, 'gable'); b.add(g, 'wood', start + .069, { duration: .013 }); g.dispose();
      b.tube(zs.map(z => place([sign * ridge, upperHeight(sign * ridge, z) + .035, z])), .065, 'jade', start + .075, { duration: .013 }, zs.length * 2);
    }
  }
  b.tube([place([-ridge - .07, y + h + .10, 0]), place([0, y + h + .07, 0]), place([ridge + .07, y + h + .10, 0])], .145, 'tile', start + .080, { duration: .013 }, 32);
  if (ornaments) {
    for (const sign of [-1, 1]) {
      const outline = new THREE.Shape();
      outline.moveTo(-.18, 0); outline.bezierCurveTo(.18, -.02, .43, .13, .43, .43);
      outline.bezierCurveTo(.47, .70, .46, 1.01, .27, 1.16);
      outline.bezierCurveTo(.13, 1.28, -.10, 1.21, -.13, 1.05);
      outline.lineTo(.075, .99); outline.bezierCurveTo(.25, .84, .07, .69, -.09, .54);
      outline.bezierCurveTo(-.26, .38, -.34, .23, -.18, 0); outline.closePath();
      const g = new THREE.ExtrudeGeometry(outline, { depth: .26, bevelEnabled: true, bevelSize: .03, bevelThickness: .025, bevelSegments: 2, steps: 1 });
      g.translate(0, 0, -.13); g.scale(sign, 1, 1); const p = g.getAttribute('position');
      for (let i = 0; i < p.count; i++) p.setXYZ(i, ...place([p.getX(i) + sign * ridge, p.getY(i) + y + h + .09, p.getZ(i)]));
      g.computeVertexNormals(); b.add(g, 'tile', start + .084, { duration: .012, shade: .94 }); g.dispose();
    }
    b.cylinder(.055, .14, .34, place([0, y + h + .33, 0]), 'tile', start + .089, { duration: .013 });
    b.sphere(place([0, y + h + .55, 0]), [.09, .13, .09], 'tile', start + .090, { duration: .013 });
  }
}
