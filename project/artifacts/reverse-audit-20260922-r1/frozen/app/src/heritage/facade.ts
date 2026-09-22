/** Photo-informed Guanque Tower infill, separate from the structural columns.
 *
 * Evidence: guanque-user-02 shows a continuous dark red-brown screen behind
 * pale bay casings; solid lower panels and transverse rails interrupt the fine
 * lattice. The brighter framing belongs to bays, not every narrow door leaf.
 * Neither photograph resolves a measured lattice motif or fabric curtains.
 * Rear elevation and unresolved leaf subdivisions are documented inference.
 * +Z is the principal facade; rx/rz locate the structural column axes.
 */
import { HeritageBuilder, type Point } from './builder';
import type { SurfaceName } from './materials';

export type FacadeSpec = {
  floor: number;
  height: number;
  rx: number;
  rz: number;
  baysX: number;
  baysZ: number;
  start: number;
  mode: 'doors' | 'windows' | 'open-gallery';
};

const rotate = (x: number, y: number, z: number, a: number): Point => [
  x * Math.cos(a) + z * Math.sin(a), y,
  z * Math.cos(a) - x * Math.sin(a),
];

/** Four-leaf infill with solid skirts, waist panels, dark lattice and bay trim.
 * `open-gallery` means an exposed exterior gallery in front of recessed infill,
 * not a missing central doorway. Only the main ground-floor entrance is open.
 * Assembly remains deterministic within start + .100 .. start + .159.
 * Back/side repetition is inferred from the visible elevations, not surveyed.
 */
export function addFacade(b: HeritageBuilder, spec: FacadeSpec) {
  const { floor, height, rx, rz, baysX, baysZ, start, mode } = spec;
  if (![floor, height, rx, rz, start].every(Number.isFinite)
    || height <= 1.5 || rx <= 0 || rz <= 0
    || ![baysX, baysZ].every(n => Number.isInteger(n) && n >= 3)) {
    throw new Error('addFacade requires finite dimensions, height > 1.5 and integer bay counts >= 3.');
  }

  const inset = mode === 'open-gallery' ? 1.12 : .47;
  // Short clerestory registers need proportionate sills rather than the full
  // lower panel of the main storey. This also keeps every grille height valid.
  const bottom = mode === 'windows' ? Math.min(.51, height * .17) : .13;
  const leafHeight = height - bottom - .43;
  const skirtHeight = leafHeight * (mode === 'doors' ? .31 : .26);
  const waistHeight = Math.min(.17, leafHeight * .09);
  const casingTint: Point = [1.025, .97, .87];

  for (let side = 0; side < 4; side++) {
    const angle = side * Math.PI / 2;
    const halfSpan = side % 2 ? rz : rx;
    const depth = side % 2 ? rx : rz;
    const bays = side % 2 ? baysZ : baysX;
    const pitch = halfSpan * 2 / bays;
    const openingWidth = pitch - .34;
    const leafWidth = openingWidth / 4;
    const wallDepth = depth - inset;
    const frameWidth = Math.min(.052, leafWidth * .11);
    const localBox = (
      size: Point, x: number, y: number, z: number,
      material: SurfaceName, time: number, shade = 1, tint?: Point,
    ) => b.box(size, rotate(x, floor + y, z, angle), material, time, {
      r: [0, angle, 0], duration: .012, lift: .34, shade, tint,
    });

    for (let bay = 0; bay < bays; bay++) {
      const center = -halfSpan + (bay + .5) * pitch;
      const entrance = mode === 'doors' && side === 0 && bay === Math.floor(bays / 2);
      const time = start + .100 + side * .0008 + bay * .00055;
      const front = wallDepth + .065;
      const top = bottom + leafHeight;

      if (mode === 'windows') {
        localBox([openingWidth, bottom - .06, .16], center, (bottom - .06) / 2,
          wallDepth, 'door', time, .98);
      }
      localBox([openingWidth + .10, .075, .27], center, bottom - .025,
        wallDepth + .025, 'stone', time + .004, .95, casingTint);

      if (entrance) {
        // The recess is inside a real gap between the entrance leaves. Its
        // return boards are dark and do not add a second row of outer columns.
        localBox([openingWidth * .56, leafHeight, .09], center,
          bottom + leafHeight / 2, wallDepth - .88, 'recess', time + .003, .66);
        for (const sign of [-1, 1]) {
          localBox([.05, leafHeight, .78], center + sign * leafWidth,
            bottom + leafHeight / 2, wallDepth - .39, 'door', time + .005, .83);
        }
      }

      for (let leaf = 0; leaf < 4; leaf++) {
        if (entrance && (leaf === 1 || leaf === 2)) continue;
        const x = center - openingWidth / 2 + (leaf + .5) * leafWidth;
        const width = leafWidth - .018;
        const innerWidth = width - frameWidth * 2;
        const leafTime = time + leaf * .0006;
        const skirtTop = bottom + skirtHeight;
        const grilleBottom = skirtTop + waistHeight / 2 + frameWidth;
        const transom = bottom + leafHeight * .80;
        const grilleTop = top - frameWidth;

        // Recessed wood and dark backing give the screen physical depth; no
        // transparent glass or photograph is used to stand in for the joinery.
        localBox([width - frameWidth, leafHeight - frameWidth, .055], x,
          bottom + leafHeight / 2, wallDepth - .045, 'recess', leafTime + .006, .80);
        localBox([innerWidth, skirtHeight - frameWidth, .075], x,
          bottom + skirtHeight / 2, wallDepth + .005, 'door', leafTime + .010, 1.07);
        // Shallow inset field in the solid skirt, bounded by real frame rails.
        localBox([innerWidth * .77, skirtHeight * .69, .026], x,
          bottom + skirtHeight / 2, wallDepth + .056, 'wood', leafTime + .011, .92);

        // All leaf stiles are dark wood. The original pale line on each side
        // of every leaf was the main cause of the bright cage-like appearance.
        for (const sign of [-1, 1]) {
          localBox([frameWidth, leafHeight, .11], x + sign * (width - frameWidth) / 2,
            bottom + leafHeight / 2, front, 'door', leafTime + .014, 1.08);
        }
        for (const [railY, railHeight] of [
          [bottom + frameWidth / 2, frameWidth],
          [skirtTop, waistHeight],
          [transom, Math.min(.105, leafHeight * .048)],
          [top - frameWidth / 2, frameWidth],
        ]) {
          localBox([width, railHeight, .115], x, railY, front,
            'door', leafTime + .017, 1.10);
        }

        // Narrow dark grille with more short crossbars than tall bright lines.
        // The exact traditional motif is unresolved by the supplied photos.
        const grilleHeight = grilleTop - grilleBottom;
        const latticeWidth = Math.min(.024, innerWidth * .075);
        for (let division = 1; division <= 3; division++) {
          localBox([latticeWidth, grilleHeight, .038],
            x - innerWidth / 2 + division * innerWidth / 4,
            (grilleBottom + grilleTop) / 2, front + .009,
            'door', leafTime + .021, 1.15);
        }
        const rows = Math.max(5, Math.round(grilleHeight / .20));
        for (let row = 1; row <= rows; row++) {
          localBox([innerWidth, latticeWidth, .039], x,
            grilleBottom + grilleHeight * row / (rows + 1),
            front + .010, 'door', leafTime + .024 + row * .00025, 1.13);
        }
        if (mode === 'doors') {
          const handleSide = leaf % 2 ? -1 : 1;
          localBox([.027, .09, .035], x + handleSide * width * .28,
            skirtTop + waistHeight / 2 + .09, front + .069,
            'bronze', leafTime + .029, .85);
        }
      }

      // Cream-grey accents enclose whole bays only. No extra heavy upright
      // railing is inserted in front of the dark screen or its structural grid.
      for (const sign of [-1, 1]) {
        localBox([.066, leafHeight + .07, .13],
          center + sign * (openingWidth / 2 + .009), bottom + leafHeight / 2,
          front + .008, 'stone', time + .030, .97, casingTint);
      }
      localBox([openingWidth + .13, .10, .15], center, top + .035,
        front + .008, 'stone', time + .031, .99, casingTint);
      localBox([openingWidth + .025, .10, .09], center, top + .13,
        wallDepth + .025, 'paint', time + .033, .96);
    }
  }
}
