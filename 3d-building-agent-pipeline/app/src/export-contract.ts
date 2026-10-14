/** Local, deterministic capture API. No interface is exposed outside ?export=1. */
export type ExportVector = [number, number, number];
export type ExportFrame = {
  progress: number;
  position: ExportVector;
  target: ExportVector;
};
export type ArchitectureExport = {
  version: "architecture-export.v1";
  adapterId: "guanque";
  ready: boolean;
  setFrame(frame: ExportFrame): {
    progress: number;
    width: number;
    height: number;
    calls: number;
    triangles: number;
  };
};

declare global {
  interface Window { __ARCHITECTURE_EXPORT__?: ArchitectureExport; }
}

export const EXPORT_MODE = new URLSearchParams(window.location.search).get("export") === "1";

export function validateExportFrame(frame: ExportFrame): void {
  if (!frame || !Number.isFinite(frame.progress) || frame.progress < 0 || frame.progress > 1) {
    throw new Error("Export progress must be finite and within [0, 1].");
  }
  for (const vector of [frame.position, frame.target]) {
    if (!Array.isArray(vector) || vector.length !== 3 || !vector.every(Number.isFinite)) {
      throw new Error("Export camera vectors must contain three finite numbers.");
    }
  }
  if (frame.position.every((value, i) => value === frame.target[i])) {
    throw new Error("Export camera position and target must differ.");
  }
}
