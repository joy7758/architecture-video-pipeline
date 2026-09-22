/** Guanque Tower: a photo-informed, artistic exterior, not a measured survey.
 * Units are scene units. Four eave bands + three principal halls on a high terrace.
 * Every component receives deterministic assembly timing through HeritageBuilder.
 */
import * as THREE from 'three';
import { HeritageBuilder, type Point } from './builder';
import type { SurfaceName } from './materials';
import { addFacade } from './facade';
import { hipRoof, ringRoof } from './roof';

/** Exterior topology, not nine exposed storeys. Dimensions use 0.4 units/metre
 * where supplied dimensions are available; roof elevations remain photo estimates.
 * visible level 1 contains the full perimeter lower eave and a taller inner hall.
 */
export const TOWER = {
  referenceScale: .4,
  internalFloors: { podium: 3, tower: 6 },
  principalEaves: ['perimeter-corridor', 'lower-hall', 'middle-hall', 'top-hall'],
  terrace: { width: 34, depth: 29.2, height: 6.6 },
  halls: [
    { floor: 6.6, height: 5.8, radius: 7.56, depth: 5.16, roofY: 13.2, roofRadius: 11.3, roofDepth: 8.2, roofHeight: 1.05, galleryX: 0, galleryZ: 0, baysX: 7, baysZ: 5, start: .15 },
    { floor: 15.6, height: 3.4, radius: 7.56, depth: 5.16, roofY: 19.8, roofRadius: 10.85, roofDepth: 7.9, roofHeight: 1.00, galleryX: 8.95, galleryZ: 6.25, baysX: 7, baysZ: 5, start: .40 },
    { floor: 22.2, height: 3.05, radius: 5.76, depth: 3.36, roofY: 25.95, roofRadius: 8.05, roofDepth: 5.3, roofHeight: 2.3, galleryX: 8.80, galleryZ: 6.15, baysX: 5, baysZ: 3, start: .67 },
  ],
  corridor: { rx: 9.96, rz: 7.56, height: 3.50, roofY: 10.45 },
} as const;
const turn = (x:number,y:number,z:number,a:number):Point => [x*Math.cos(a)+z*Math.sin(a),y,z*Math.cos(a)-x*Math.sin(a)];
const noise=(n:number)=>{const x=Math.sin(n*31.7+9.2)*43758.5;return x-Math.floor(x);};

function rails(b:HeritageBuilder,y:number,rx:number,start:number,material:SurfaceName='wood',entrance=false,rz=rx,centerZ=0) {
  for(let s=0;s<4;s++){
    const a=s*Math.PI/2,n=20,r=s%2?rz:rx,depth=s%2?rx:rz;
    const point=(x:number,y:number,z:number):Point=>{const p=turn(x,y,z,a);p[2]+=centerZ;return p;};
    for(let i=0;i<=n;i++){
      const x=-r+i*2*r/n;
      if(entrance && s===0 && (Math.abs(x)<5.3 || Math.abs(x)>13.6))continue;
      b.box([.11,.65,.11],point(x,y+.33,depth),material,start+i*.0006,{r:[0,a,0]});
      b.sphere(point(x,y+.71,depth),[.085,.07,.085],material,start+.016);
      if(i<n && !(entrance && s===0 && (Math.abs(x+r/n)<5.5 || Math.abs(x+r/n)>13.5))){
        for(const h of [.12,.39,.63])b.box([r*2/n,.065,.075],point(x+r/n,y+h,depth),material,start+.012,{r:[0,a,0]});
        b.box([.05,.49,.06],point(x+r/n,y+.34,depth),material,start+.016,{r:[0,a,0]});
      }
    }
  }
}

/** Curved horizontal gong arm, replacing the earlier stacks of plain cuboids.
 * The shallow raised tips are a silhouette approximation, not a mould drawing.
 */
function gongArm(b:HeritageBuilder,width:number,p:Point,angle:number,start:number){
  const g=b.geo(`guanque-gong-${width}`,()=>{
    const s=new THREE.Shape();s.moveTo(-width/2,.11);
    s.quadraticCurveTo(-width*.29,.10,-width*.17,-.035);s.lineTo(width*.17,-.035);
    s.quadraticCurveTo(width*.29,.10,width/2,.11);s.lineTo(width/2,-.04);
    s.quadraticCurveTo(width*.29,-.055,width*.20,-.18);s.lineTo(-width*.20,-.18);
    s.quadraticCurveTo(-width*.29,-.055,-width/2,-.04);s.closePath();
    const g=new THREE.ExtrudeGeometry(s,{depth:.22,bevelEnabled:false,steps:1});g.translate(0,0,-.11);return g;
  });
  b.add(g,'paint',start,{p,r:[0,angle,0],shade:.94});
}

function brackets(b:HeritageBuilder,y:number,rx:number,start:number,rz:number) {
  for(let s=0;s<4;s++){
    const a=s*Math.PI/2,r=s%2?rz:rx,depth=s%2?rx:rz;
    for(let i=-6;i<=6;i++){
      const x=i*r/6.1;
      for(let k=0;k<3;k++){
        gongArm(b,.56+k*.24,turn(x,y+k*.18+.05,depth+k*.15,a),a,start+k*.005);
        b.box([.16,.16,.62+k*.18],turn(x,y+k*.18+.07,depth+k*.15,a),'wood',start+k*.005,{r:[0,a,0]});
        for(const sign of [-1,1])b.box([.12,.20,.18],turn(x+sign*(.20+k*.10),y+k*.18+.12,depth+k*.15,a),'bronze',start+.02,{r:[0,a,0]});
      }
    }
    for(const off of [0,.34]){
      b.box([r*2+.5,.22,.35],turn(0,y+.52+off,depth+.43,a),'jade',start+.026,{r:[0,a,0]});
      b.box([r*2+.45,.035,.035],turn(0,y+.55+off,depth+.62,a),'bronze',start+.028,{r:[0,a,0]});
    }
  }
}

function hall(b:HeritageBuilder,level:typeof TOWER.halls[number],index:number) {
  const {floor,height,radius:rx,depth:rz,start,baysX,baysZ}=level;
  b.box([rx*2+.4,.28,rz*2+.4],[0,floor-.12,0],'stone',start,{duration:.025});
  for(let side=0;side<4;side++){
    const a=side*Math.PI/2,bays=side%2?baysZ:baysX,r=side%2?rz:rx,depth=side%2?rx:rz;
    for(let j=0;j<=bays;j++){
      const x=-r+j*2*r/bays;
      b.cylinder(.23,.29,.24,turn(x,floor+.12,depth,a),'stone',start+.025);
      b.cylinder(.15,.20,height-.22,turn(x,floor+height/2+.1,depth,a),'wood',start+.05+j*.002,{duration:.025,lift:2});
      b.box([.46,.22,.46],turn(x,floor+height-.04,depth,a),'jade',start+.08);
    }
    for(const h of [height-.38,height-.12])b.box([r*2,.19,.28],turn(0,floor+h,depth,a),'paint',start+.09,{r:[0,a,0]});
    for(let j=0;j<bays;j++){
      const x=-r+(j+.5)*2*r/bays,bay=2*r/bays-.34;
      // Raised inverted-V/curved door-head carpentry, not scalloped drapery.
      b.tube([turn(x-bay*.42,floor+height-.50,depth+.17,a),turn(x-bay*.18,floor+height-.43,depth+.17,a),turn(x,floor+height-.22,depth+.17,a),turn(x+bay*.18,floor+height-.43,depth+.17,a),turn(x+bay*.42,floor+height-.50,depth+.17,a)],.042,'stone',start+.14,{},10);
    }
  }
  // Lower hall is visibly split by the corridor eave; its upper register is
  // a narrow clerestory, not one six-metre-tall row of doors.
  if(index===0){
    addFacade(b,{floor,height:3.52,rx,rz,baysX,baysZ,start,mode:'doors'});
    // Only a low, shaded structural register is exposed above the outer
    // corridor roof. It is not a repeated full window storey.
    b.box([rx*1.97,1.4,rz*1.97],[0,floor+4.6,0],'recess',start+.14);
    for(let side=0;side<4;side++){
      const a=side*Math.PI/2,r=side%2?rz:rx,d=side%2?rx:rz;
      for(const y of [floor+4.25,floor+5.25])b.box([2*r,.20,.20],turn(0,y,d,a),'paint',start+.15,{r:[0,a,0]});
      for(let j=-6;j<=6;j++)b.box([.12,1.10,.17],turn(j*r/6.5,floor+4.76,d,a),'wood',start+.145,{r:[0,a,0]});
    }
    b.box([2*rx,.26,2*rz],[0,floor+3.9,0],'wood',start+.135);
  }else addFacade(b,{floor,height,rx,rz,baysX,baysZ,start,mode:index===2?'open-gallery':'windows'});
  for(const x of [-rx*.55,rx*.55])for(const z of [-rz*.55,rz*.55])b.cylinder(.18,.22,height,[x,floor+height/2,z],'wood',start+.05,{lift:2});
  for(const z of [-rz*.55,rz*.55])b.box([2*rx,.27,.25],[0,floor+height-.15,z],'wood',start+.082);
  b.box([rx*2,.25,rz*2],[0,floor+height+.05,0],'wood',start+.145);
}

/** Continuous 副阶周匝: 32 perimeter columns, plus projecting bay groups.
 * Bays along the long/short sides are 9/7; corner columns are shared.
 */
function lowerCorridor(b:HeritageBuilder){
  const {rx,rz,height,roofY}=TOWER.corridor,floor=6.6;
  for(let side=0;side<4;side++){
    const a=side*Math.PI/2,bays=side%2?7:9,r=side%2?rz:rx,d=side%2?rx:rz;
    for(let j=0;j<bays;j++){
      const x=-r+j*2*r/bays;
      b.cylinder(.21,.26,.24,turn(x,floor+.12,d,a),'stone',.202);
      b.cylinder(.12,.17,height,turn(x,floor+height/2,d,a),'wood',.222+j*.001,{lift:1.8});
    }
    b.box([2*r+.25,.24,.3],turn(0,floor+height,d,a),'jade',.248,{r:[0,a,0]});
    for(let j=0;j<bays;j++){
      const x=-r+(j+.5)*2*r/bays;
      b.tube([turn(x-r/bays*.78,floor+height-.34,d+.14,a),turn(x-r/bays*.25,floor+height-.25,d+.14,a),turn(x,floor+height-.03,d+.14,a),turn(x+r/bays*.25,floor+height-.25,d+.14,a),turn(x+r/bays*.78,floor+height-.34,d+.14,a)],.04,'stone',.253,{},10);
    }
  }
  brackets(b,roofY-.8,rx,.252,rz);
  ringRoof(b,{outerX:rx+1.7,outerZ:rz+1.55,innerX:7.56,innerZ:5.16,eaveY:roofY,innerY:12.0,start:.27,projections:[{side:0,halfWidth:5.9,outset:.85,rise:1.35,joinDepth:3.0},{side:2,halfWidth:5.9,outset:.85,rise:1.35,joinDepth:3.0},{side:1,halfWidth:3.65,outset:.75,rise:1.35,joinDepth:3.0},{side:3,halfWidth:3.65,outset:.75,rise:1.35,joinDepth:3.0}]});
  for(let side=0;side<4;side++){
    const a=side*Math.PI/2,d=side%2?rx:rz,bays=side%2?3:5,half=bays*1.08;
    for(let j=0;j<=bays;j++){
      const x=-half+j*2*half/bays;
      b.cylinder(.12,.17,height-.04,turn(x,floor+height/2,d+1.15,a),'wood',.229+j*.002);
      b.cylinder(.22,.26,.22,turn(x,floor+.11,d+1.15,a),'stone',.21);
    }
    b.box([half*2+.3,.25,.35],turn(0,floor+height,d+1.15,a),'jade',.252,{r:[0,a,0]});
    // The projecting roof is integrated in ringRoof's common surface above.
  }
}

export function courtyard(b:HeritageBuilder) {
  b.box([42,.40,51],[0,-.5,7],'stone',-1,{lift:0,shade:.87});
  for(let x=-12;x<=12;x++)for(let z=-11;z<=21;z++)b.box([1.47,.08,1.47],[x*1.50,-.25,z*1.50],'stone',-1,{lift:0,shade:.91+noise(x*71+z)*.10});
}

export function buildArchitecture(b:HeritageBuilder) {
  // Photo-informed terrace: tall podium + two forward landings, three stair flights.
  const terraceBlock=(w:number,d:number,cz:number,h:number,start:number)=>{
    b.box([w,h,d],[0,h/2-.15,cz],'stone',start,{duration:.022,lift:1.0,shade:.78});
    b.box([w+.25,.22,d+.25],[0,h-.08,cz],'stone',start+.013,{shade:1.08});
    b.box([w+.12,.16,d+.12],[0,.0,cz],'stone',start+.005,{shade:.9});
    for(let side=0;side<4;side++){
      const a=side*Math.PI/2,r=side%2?d/2:w/2,depth=side%2?w/2:d/2;
      for(let row=0;row<Math.floor(h/.34);row++)for(let i=0;i<Math.floor(r*2/.84);i++){
        const x=-r+.42+i*.84+(row%2)*.12,p=turn(x,.13+row*.34,depth+.03,a);p[2]+=cz;
        b.box([.815,.315,.08],p,'stone',start+.002+row*.001,{r:[0,a,0],shade:.57+noise(i+row*7)*.12});
      }
    }
  };
  // The reference has a tall lower approach + a shorter upper approach,
  // then a low plinth step, not three equal-height cascading stair flights.
  const lowerTerrace=4.216,mainTerrace=5.952;
  terraceBlock(34,24.2,-1.5,mainTerrace,.006);
  terraceBlock(26.6,9.0,15.1,lowerTerrace,.018);
  // Low building plinth sits on the main high platform.
  b.box([25.7,6.6-mainTerrace,18.3],[0,(6.6+mainTerrace)/2,0],'stone',.08,{shade:1.05});
  b.box([26.0,.15,18.5],[0,6.56,0],'stone',.09,{shade:1.08});
  const flight=(base:number,rise:number,front:number,run:number,width:number,start:number,cx=0,steps=16,parapet=true)=>{
    for(let i=0;i<steps;i++){
      const top=base+(i+1)*rise/steps;
      b.box([width,top,run/steps+.02],[cx,top/2,front-(i+.5)*run/steps],'stone',start+i*.001,{lift:.4,shade:.98});
    }
    if(parapet)for(const sign of [-1,1]){
      const x=cx+sign*(width/2+.13),angle=Math.atan2(rise,run),length=Math.hypot(run,rise);
      b.box([.30,.54,length+.3],[x,base+rise/2+.30,front-run/2],'stone',start+.022,{r:[angle,0,0],shade:1.12});
      b.box([.36,.10,length+.4],[x,base+rise/2+.61,front-run/2],'stone',start+.023,{r:[angle,0,0],shade:1.16});
    }
  };
  flight(0,lowerTerrace,28.2,8.6,11.5,.045,0,27);
  flight(lowerTerrace,mainTerrace-lowerTerrace,14.9,4.2,10.8,.080,0,13);
  flight(mainTerrace,6.6-mainTerrace,10.5,1.35,11.2,.108,0,11,false);
  flight(0,mainTerrace,21.5,10.8,3.1,.073,-15.4,35);
  flight(0,mainTerrace,21.5,10.8,3.1,.073,15.4,35);
  rails(b,mainTerrace,16.6,.121,'stone',true,11.7,-1.5);
  // Fore-terrace parapets frame the long lower approach in the reference.
  for(const sign of [-1,1]){
    b.box([6.8,.43,.25],[sign*9.9,lowerTerrace+.22,19.5],'stone',.10);
    for(let i=0;i<11;i++)b.box([.12,.59,.16],[sign*(6.3+i*.7),lowerTerrace+.5,19.5],'stone',.104);
    b.box([7.2,.10,.24],[sign*9.75,lowerTerrace+.80,19.5],'stone',.108);
  }
  lowerCorridor(b);
  for(const [index,level] of TOWER.halls.entries()){
    const depth=level.depth;
    hall(b,level,index);
    const next=TOWER.halls[index+1];
    brackets(b,level.roofY-.8,level.radius,level.start+.153,depth);
    if(next){
      // An annular waist eave connects to a broad bracketed gallery above.
      // Its entire visible width carries slope; no hidden central palace roof.
      const innerX=next.galleryX-.55,innerZ=next.galleryZ-.55;
      ringRoof(b,{outerX:level.roofRadius,outerZ:level.roofDepth,innerX,innerZ,
        eaveY:level.roofY,innerY:level.roofY+level.roofHeight,start:level.start+.18});
      const baseY=level.roofY+level.roofHeight,friezeTop=next.floor-.30;
      b.box([2*innerX,friezeTop-baseY,2*innerZ],[0,(baseY+friezeTop)/2,0],'recess',level.start+.17,{shade:.78});
    }else hipRoof(b,level.roofY,level.roofRadius,level.roofDepth,level.roofHeight,level.start+.18,[0,0,0],0,true,
      [0,1,2,3].map(side=>({side:side as 0|1|2|3,halfWidth:3.65,outset:.4,rise:1.18,joinDepth:2.2})));
    if(index>0){
      const gx=level.galleryX,gz=level.galleryZ;
      b.box([2*gx,.25,2*gz],[0,level.floor-.12,0],'stone',level.start);
      b.box([2*gx+.06,.18,2*gz+.06],[0,level.floor-.36,0],'paint',level.start+.006);
      rails(b,level.floor,gx,level.start+.035,'stone',false,gz);
      brackets(b,level.floor-1.44,gx-.42,level.start+.012,gz-.42);
      for(let side=0;side<4;side++){
        const angle=side*Math.PI/2,span=side%2?gz:gx;
        const outer=(side%2?gx:gz)-.28,inner=(side%2?level.radius:depth)*.83;
        for(let n=-6;n<=6;n++){
          b.box([.23,.23,outer-inner+.42],turn(n*span/6.2,level.floor-.78,(inner+outer)/2,angle),'wood',level.start+.012,{r:[0,angle,0]});
          // Shaped bracket head and cream trim break the former broad green stripe.
          b.tube([turn(n*span/6.2-.24,level.floor-.60,outer,angle),turn(n*span/6.2,level.floor-.73,outer+.05,angle),turn(n*span/6.2+.24,level.floor-.60,outer,angle)],.05,'stone',level.start+.022,{},6);
        }
        b.box([span*2-.3,.22,.18],turn(0,level.floor-.64,outer,angle),'paint',level.start+.023,{r:[0,angle,0]});
      }
    }
  }
  // Four upper projecting galleries. Front/back are three bays, with columns
  // and the projecting eave sharing one extent rather than floating canopies.
  const top=TOWER.halls[2];
  for(let side=0;side<4;side++){
    const a=side*Math.PI/2,d=side%2?top.radius:top.depth,half=3.24;
    const outer=(side%2?top.roofRadius:top.roofDepth)+.12;
    for(const x of [-half,-half/3,half/3,half]){
      b.cylinder(.115,.155,top.height+.04,turn(x,top.floor+top.height/2,outer,a),'wood',.732,{lift:1.1});
      b.cylinder(.22,.25,.18,turn(x,top.floor+.09,outer,a),'stone',.718);
    }
    b.box([half*2+.3,.25,.35],turn(0,top.floor+top.height+.08,outer,a),'paint',.78,{r:[0,a,0]});
    // Actual eaves are carried by a deep painted bracket crown, including the
    // projecting gallery. Previously these outer columns ended at one flat bar.
    for(let n=-3;n<=3;n++)for(let k=0;k<3;k++){
      const x=n*half/3.2,y=top.floor+top.height+.12+k*.16;
      gongArm(b,.46+k*.20,turn(x,y+.04,outer+k*.06,a),a,.786+k*.002);
      b.box([.12,.12,.43+k*.12],turn(x,y+.06,outer+k*.05,a),'wood',.789+k*.002,{r:[0,a,0]});
      for(const sign of [-1,1])b.box([.09,.10,.14],turn(x+sign*(.16+k*.075),y+.10,outer+k*.05,a),'stone',.792+k*.002,{r:[0,a,0],shade:.75});
    }
    // Roof projection is part of the shared top-roof surface, not a second whole roof.
  }
}

/** Only labels identifiable in a located front-elevation photograph are used.
 * Horizontal 文萃李唐 reads right-to-left; top-floor 鸛雀樓 reads top-to-bottom.
 * Other elevations / couplet inscriptions are deliberately untranscribed.
 */
export const PLAQUES = [
  {id:'entrance-front',text:'文萃李唐',direction:'rtl',width:2.8,height:.91,position:[0,9.71,8.96] as Point,at:.37},
  {id:'top-front',text:'鸛雀樓',direction:'vertical',width:.77,height:2.06,position:[0,24.42,5.47] as Point,at:.92},
] as const;

export function addPlaques(scene:THREE.Scene) {
  const objects:{group:THREE.Group;at:number}[]=[],resources:{dispose():void}[]=[];
  // West entrance couplet recorded by Xi'an Evening News, 2006-10-01:
  // https://news.sohu.com/20061001/n245627258.shtml . Right = upper line.
  const entranceCouplets=[-1,1].map(sign=>({id:`entrance-couplet-${sign}`,text:sign>0?'凌空白日三千丈':'拔地黃河第一樓',direction:'vertical',width:.26,height:2.48,position:[sign*1.08,8.05,8.87] as Point,at:.37}));
  for(const spec of [...PLAQUES,...entranceCouplets]){
    const vertical=spec.direction==='vertical',long=spec.text.length>3&&vertical,canvas=document.createElement('canvas');
    canvas.width=long?256:vertical?384:1024;canvas.height=long?2048:vertical?1024:384;
    const ctx=canvas.getContext('2d')!,w=canvas.width,h=canvas.height;
    ctx.fillStyle='#29226b';ctx.fillRect(0,0,w,h);
    ctx.strokeStyle='#b8984e';ctx.lineWidth=13;ctx.strokeRect(12,12,w-24,h-24);
    ctx.lineWidth=3;ctx.strokeRect(33,33,w-66,h-66);
    // Simplified carved border, separate from the calligraphic face.
    for(let x=50;x<w-30;x+=36)for(const y of [23,h-23]){
      ctx.beginPath();ctx.ellipse(x,y,10,5,0,0,Math.PI*2);ctx.stroke();
    }
    ctx.fillStyle='#d9bd76';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.font=`${long?204:vertical?248:235}px "Kaiti SC", "STKaiti", "KaiTi", "Songti SC", serif`;
    const chars=Array.from(spec.text);
    if(vertical)chars.forEach((c,i)=>ctx.fillText(c,w/2,long?180+i*(h-360)/(chars.length-1):177+i*327));
    else chars.reverse().forEach((c,i)=>ctx.fillText(c,150+i*241,h*.53));
    const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;
    const face=new THREE.MeshStandardMaterial({map:texture,roughness:.85});
    const edge=new THREE.MeshStandardMaterial({color:'#927e4c',roughness:.8});
    const boardGeometry=new THREE.BoxGeometry(spec.width,spec.height,.13);
    const faceGeometry=new THREE.PlaneGeometry(spec.width*.98,spec.height*.98);
    const group=new THREE.Group(),board=new THREE.Mesh(boardGeometry,edge),lettering=new THREE.Mesh(faceGeometry,face);
    lettering.position.z=.071;group.add(board,lettering);group.position.set(...spec.position);
    group.name=`plaque-${spec.id}`;scene.add(group);objects.push({group,at:spec.at});
    resources.push(texture,face,edge,boardGeometry,faceGeometry);
  }
  return {
    update(progress:number){objects.forEach(({group,at})=>{group.visible=progress>=at;});},
    dispose(){objects.forEach(({group})=>group.removeFromParent());resources.forEach(r=>r.dispose());},
  };
}
