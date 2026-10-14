import * as THREE from "three";

export type SurfaceName = "brick" | "wood" | "door" | "paint" | "jade" | "stone" | "plaster" | "tile" | "bronze" | "recess" | "cloth" | "paper" | "moss" | "glass";

// Calm, deterministic pigment and micro-grain. Sunset in the source photographs
// is lighting evidence, not a reason to make every roof tile reflective gold.
// door = dark lacquered joinery; paint = small blue-green/ochre painted bands.
export function createHeritageMaterials(renderer: THREE.WebGLRenderer) {
  const textures: THREE.Texture[] = [];
  const palette: Record<SurfaceName, string> = {
    brick: "#805547", wood: "#583a30", door: "#493029", paint: "#354a49",
    jade: "#46514b", stone: "#aaa99d",
    plaster: "#c9c6b9", tile: "#635e50", bronze: "#928061", recess: "#282623",
    cloth: "#555c53", paper: "#d9ab70", moss: "#45573a", glass: "#b6c8c3",
  };
  const output = {} as Record<SurfaceName, THREE.MeshStandardMaterial>;
  for (const [name, base] of Object.entries(palette) as [SurfaceName, string][]) {
    if(name==="glass"){
      output[name]=new THREE.MeshPhysicalMaterial({color:base,roughness:.16,metalness:0,transparent:true,opacity:.09,depthWrite:false,clearcoat:.65,clearcoatRoughness:.18,vertexColors:true});
      continue;
    }
    const canvas = document.createElement("canvas");
    const size = name === "plaster" ? 1024 : 512;
    canvas.width = canvas.height = size;
    const ctx = canvas.getContext("2d")!;
    let seed = 83 + name.length * 101;
    const rand = () => ((seed = (seed * 16807) % 2147483647) - 1) / 2147483646;
    ctx.fillStyle = base;
    ctx.fillRect(0, 0, size, size);
    // Low-contrast pigment variation, with no artificial ruined-wall treatment.
    for (let i = 0; i < 65; i++) {
      const x = rand() * size, y = rand() * size, r = size * (.02 + rand() * .13);
      const gradient = ctx.createRadialGradient(x, y, 0, x, y, r);
      gradient.addColorStop(0, name === "tile" ? (i % 3 ? "rgba(25,30,27,.022)" : "rgba(210,217,201,.017)") : (i % 3 ? "rgba(45,34,19,.019)" : "rgba(252,244,217,.018)"));
      gradient.addColorStop(1, "rgba(100,80,50,0)");
      ctx.fillStyle = gradient; ctx.fillRect(x-r, y-r, r*2, r*2);
    }
    if (name === "wood" || name === "door") {
      for (let i = 0; i < 160; i++) {
        const x = rand() * size;
        ctx.strokeStyle = i % 3 ? "rgba(30,19,10,.075)" : "rgba(176,126,87,.065)";
        ctx.lineWidth = .4 + rand() * 1.8;
        ctx.beginPath(); ctx.moveTo(x, 0);
        for (let y = 0; y <= size; y += 8) ctx.lineTo(x + Math.sin(y*.035 + x)*2 + Math.sin(y*.008)*5, y);
        ctx.stroke();
      }
    }
    if (name === "paint") {
      // A restrained generic painted-beam register, not a claim to transcribe
      // the unresolved historic ornament. Geometry still supplies every beam.
      ctx.strokeStyle = "#a09572"; ctx.lineWidth = 4;
      for (const y of [30, 482]) {
        ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(size,y); ctx.stroke();
      }
      ctx.strokeStyle = "#628281"; ctx.lineWidth = 11;
      for (const y of [61, 451]) {
        ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(size,y); ctx.stroke();
      }
      for (let motif=0;motif<4;motif++) {
        const x=motif*128+64;
        ctx.fillStyle="#263b45";ctx.fillRect(x-50,100,100,312);
        ctx.strokeStyle="#8d825f";ctx.lineWidth=5;ctx.beginPath();
        ctx.moveTo(x-37,256);ctx.lineTo(x,156);ctx.lineTo(x+37,256);
        ctx.lineTo(x,356);ctx.closePath();ctx.stroke();
        ctx.strokeStyle="#819084";ctx.lineWidth=3;ctx.beginPath();
        ctx.moveTo(x-19,256);ctx.lineTo(x,199);ctx.lineTo(x+19,256);
        ctx.lineTo(x,313);ctx.closePath();ctx.stroke();
      }
    }
    for(let i=0;i<(name==="plaster"?14000:6500);i++){
      ctx.globalAlpha=name==="tile"?.14:.28;
      ctx.fillStyle=rand()>.45?`rgba(255,242,214,${.04+rand()*.13})`:`rgba(31,26,18,${.025+rand()*.1})`;
      const s=.4+rand()*1.6;ctx.fillRect(rand()*size,rand()*size,s,s);
    }
    ctx.globalAlpha=1;
    const texture=new THREE.CanvasTexture(canvas);
    texture.colorSpace=THREE.SRGBColorSpace;
    texture.wrapS=texture.wrapT=THREE.RepeatWrapping;
    texture.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
    textures.push(texture);
    // Micro-height and roughness are independent of pigment: stains are not craters.
    const detail=document.createElement("canvas");detail.width=detail.height=256;
    const dc=detail.getContext("2d")!,pixels=dc.createImageData(256,256);
    for(let y=0;y<256;y++)for(let x=0;x<256;x++){
      const i=(y*256+x)*4;
      const grain=["wood","door"].includes(name)?Math.sin(x*.83+Math.sin(y*.033)*2)*10:0;
      const v=128+(rand()-.5)*(name==="stone"?38:18)+grain;
      pixels.data[i]=pixels.data[i+1]=pixels.data[i+2]=v;pixels.data[i+3]=255;
    }
    dc.putImageData(pixels,0,0);
    const bump=new THREE.CanvasTexture(detail);bump.wrapS=bump.wrapT=THREE.RepeatWrapping;bump.anisotropy=texture.anisotropy;textures.push(bump);
    const roughCanvas=document.createElement("canvas");roughCanvas.width=roughCanvas.height=256;
    const rc=roughCanvas.getContext("2d")!;rc.fillStyle=name==="tile"?"#dddddd":["wood","door"].includes(name)?"#dfdfdf":"#ededed";rc.fillRect(0,0,256,256);
    for(let i=0;i<90;i++){rc.fillStyle=`rgba(60,60,60,${.02+rand()*.045})`;rc.fillRect(rand()*256,rand()*256,8+rand()*35,8+rand()*35);}
    const roughness=new THREE.CanvasTexture(roughCanvas);roughness.wrapS=roughness.wrapT=THREE.RepeatWrapping;textures.push(roughness);
    output[name]=new THREE.MeshStandardMaterial({map:texture,bumpMap:bump,roughnessMap:roughness,bumpScale:name==="plaster"?.006:name==="tile"?.004:name==="paint"?.003:.010,roughness:name==="bronze"?.92:name==="tile"?.96:.97,metalness:name==="bronze"?.12:0,vertexColors:true});
    if(["tile","wood","door","bronze"].includes(name))output[name].side=THREE.DoubleSide;
    if(name==="paper"){output[name].emissive.set("#9d5020");output[name].emissiveIntensity=.28;}
  }
  return {materials:output,dispose(){textures.forEach(t=>t.dispose());Object.values(output).forEach(m=>m.dispose());}};
}
