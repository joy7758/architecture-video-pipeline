/** Public, deterministic animation contract. Geometry timing is in heritage/guanque.ts. */
export const DURATION = 24;
export const STAGES = [
  {name:'筑台 · 石阶层起', end:.15},
  {name:'立柱 · 初檐舒展', end:.40},
  {name:'登阁 · 梁枋相承', end:.67},
  {name:'凌空 · 重檐叠翠', end:.85},
  {name:'合脊 · 一楼落成', end:1},
] as const;
export const clampProgress=(p:number)=>Math.max(0,Math.min(1,Number.isFinite(p)?p:0));
export const stageAt=(p:number)=>p>=1?'落成 · 更上一层楼':STAGES.find(s=>p<s.end)?.name??STAGES[0].name;
