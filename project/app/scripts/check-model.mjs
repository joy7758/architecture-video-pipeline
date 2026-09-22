/** Headless geometry validation. Does not substitute for visual browser inspection. */
import fs from 'node:fs/promises';
import path from 'node:path';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import ts from 'typescript';
import * as THREE from 'three';
const out=await fs.mkdtemp(path.resolve('.model-check-'));
try {
  for(const file of ['heritage/guanque','heritage/facade','heritage/roof','heritage/builder','timeline']){
    const src=await fs.readFile(`src/${file}.ts`,'utf8');
    const js=ts.transpileModule(src,{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.ES2022}}).outputText.replaceAll("'./roof'","'./roof.mjs'").replaceAll("'./facade'","'./facade.mjs'").replaceAll("'./builder'","'./builder.mjs'").replaceAll('"./builder"','"./builder.mjs"');
    const dst=path.join(out,file+'.mjs');await fs.mkdir(path.dirname(dst),{recursive:true});await fs.writeFile(dst,js);
  }
  const {HeritageBuilder}=await import(path.join(out,'heritage/builder.mjs'));
  const {buildArchitecture,courtyard,TOWER,PLAQUES}=await import(path.join(out,'heritage/guanque.mjs'));
  const {clampProgress,stageAt}=await import(path.join(out,'timeline.mjs'));
  function inspect(){
    const names=['brick','wood','jade','stone','plaster','tile','bronze','recess','cloth','paper','moss','glass','door','paint'];
    const mats=Object.fromEntries(names.map(n=>[n,new THREE.MeshStandardMaterial()]));
    class RoofCheckedBuilder extends HeritageBuilder {
      add(geometry,material,start,options){
        if(geometry.userData.roofPart?.endsWith(':tile')){
          const normals=geometry.getAttribute('normal');
          for(let i=0;i<normals.count;i++)assert.ok(normals.getY(i)>0,'roof tile faces must point upward');
        }
        super.add(geometry,material,start,options);
      }
    }
    const b=new RoofCheckedBuilder(mats),scene=new THREE.Scene();courtyard(b);buildArchitecture(b);b.finish(scene);
    const hash=crypto.createHash('sha256');let vertices=0,maxEnd=0;
    for(const mesh of b.meshes){
      for(const name of ['position','normal','aBuild']){
        const values=mesh.geometry.getAttribute(name).array;assert.ok(values.every(Number.isFinite),`${name} has non-finite data`);hash.update(Buffer.from(values.buffer));
      }
      const schedule=mesh.geometry.getAttribute('aBuild');vertices+=schedule.count;
      for(let i=0;i<schedule.count;i++){
        const start=schedule.getX(i),duration=schedule.getY(i);assert.ok(duration>0,'duration must be positive');maxEnd=Math.max(maxEnd,start+duration);assert.ok(start+duration<=1.00001,'unfinished piece at progress=1');
      }
      mesh.geometry.computeBoundingBox();assert.ok(mesh.geometry.boundingBox.max.y<40,'model outside expected height');
    }
    assert.ok(b.pieces>1000 && b.meshes.length<16,'unexpected batching');
    const result={pieces:b.pieces,batches:b.meshes.length,vertices,maxEnd,digest:hash.digest('hex')};b.dispose();Object.values(mats).forEach(m=>m.dispose());return result;
  }
  assert.deepEqual(TOWER.halls.map(h=>[h.baysX,h.baysZ]),[[7,5],[7,5],[5,3]],'reference column grid');
  assert.equal(TOWER.principalEaves.length,4,'four main eave bands');
  const top=TOWER.halls[2],middle=TOWER.halls[1];
  assert.ok(top.galleryX>top.roofRadius+.4 && top.galleryZ>top.roofDepth+.4,'highest gallery must extend beyond top roof including projecting eaves');
  assert.ok(top.galleryX/middle.galleryX>.94,'reference upper galleries are almost equal in width');
  assert.ok(top.roofHeight>2,'top roof must rise above its projecting galleries');
  assert.deepEqual(PLAQUES.map(p=>[p.text,p.direction]),[['文萃李唐','rtl'],['鸛雀樓','vertical']],'located inscription contract');
  const a=inspect(),b=inspect();assert.equal(a.digest,b.digest,'rebuilding must be deterministic');
  assert.equal(clampProgress(-1),0);assert.equal(clampProgress(3),1);assert.equal(clampProgress(NaN),0);assert.equal(stageAt(1),'落成 · 更上一层楼');
  console.log(JSON.stringify({status:'PASS',checks:['finite geometry','all pieces finished by 100%','material batching','deterministic reconstruction','timeline boundaries','upward roof tiles','photo-derived silhouette constraints'],...a},null,2));
}finally{await fs.rm(out,{recursive:true,force:true});}
