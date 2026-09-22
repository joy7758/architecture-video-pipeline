/** Guanque Tower: a photo-informed, artistic exterior, not a measured survey.
 * Units are scene units. Four eave bands + three principal halls on a high terrace.
 * Every component receives deterministic assembly timing through HeritageBuilder.
 */
import * as THREE from 'three';
import { HeritageBuilder, type Point } from './builder';
import type { SurfaceName } from './materials';
import { addFacade } from './facade';

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
    { floor: 6.6, height: 6.3, radius: 7.56, depth: 5.16, roofY: 13.7, roofRadius: 11.3, roofDepth: 8.2, roofHeight: 1.65, baysX: 7, baysZ: 5, start: .15 },
    { floor: 15.35, height: 3.95, radius: 7.56, depth: 5.16, roofY: 20.10, roofRadius: 10.85, roofDepth: 7.9, roofHeight: 1.65, baysX: 7, baysZ: 5, start: .40 },
    { floor: 22.50, height: 3.65, radius: 5.76, depth: 3.36, roofY: 26.92, roofRadius: 8.25, roofDepth: 5.7, roofHeight: 1.3, baysX: 5, baysZ: 3, start: .67 },
  ],
  corridor: { rx: 9.96, rz: 7.56, height: 3.50, roofY: 10.85 },
} as const;
const turn = (x:number,y:number,z:number,a:number):Point => [x*Math.cos(a)+z*Math.sin(a),y,z*Math.cos(a)-x*Math.sin(a)];
const noise=(n:number)=>{const x=Math.sin(n*31.7+9.2)*43758.5;return x-Math.floor(x);};

function grid(nx:number,ny:number,point:(u:number,v:number)=>Point) {
  const positions:number[]=[],uv:number[]=[],indices:number[]=[];
  for(let j=0;j<=ny;j++)for(let i=0;i<=nx;i++){positions.push(...point(i/nx,j/ny));uv.push(i/nx,j/ny);}
  for(let j=0;j<ny;j++)for(let i=0;i<nx;i++){const a=j*(nx+1)+i;indices.push(a,a+nx+1,a+1,a+1,a+nx+1,a+nx+2);}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(indices);g.computeVertexNormals();return g;
}

/** Hipped roof with a horizontal ridge; both faces and soffit are modeled.
 * Each ceramic segment follows the same roof profile as boards and ridge caps.
 */
function hipRoof(b:HeritageBuilder,y:number,w:number,d:number,h:number,start:number,center:Point=[0,0,0],angle=0,ornaments=false) {
  const ridge=w*(ornaments?.62:.42);
  const place=(p:Point):Point=>{const t=turn(...p,angle);return [t[0]+center[0],t[1]+center[1],t[2]+center[2]];};
  const shape=(side:number,u:number,v:number):Point=>{
    const spread=ornaments?ridge+(w-ridge)*Math.max(0,(v-.45)/.55):ridge+(w-ridge)*v;
    const lift=h*Math.pow(1-v,1.65)+.17*Math.pow(v,6)+.48*Math.pow(Math.abs(u*2-1),9)*Math.pow(v,4);
    if(side<2)return [(u*2-1)*spread,y+lift,(side===0?1:-1)*v*d];
    const sv=ornaments?.45+.55*v:v;
    const sy=h*Math.pow(1-sv,1.65)+.17*Math.pow(sv,6)+.48*Math.pow(Math.abs(u*2-1),9)*Math.pow(sv,4);
    return [(side===2?1:-1)*(ridge+(w-ridge)*v),y+sy,(u*2-1)*d*sv];
  };
  for(let side=0;side<4;side++){
    const surface=(u:number,v:number)=>place(shape(side,u,v));
    for(const offset of [0,-.22]){
      const g=grid(20,10,(u,v)=>{const p=surface(u,v);p[1]+=offset;return p;});
      b.add(g,offset===0?'tile':'wood',start,{duration:.027,lift:.6});g.dispose();
    }
    const edge=grid(30,1,(u,v)=>{const p=surface(u,1);p[1]-=v*.23;return p;});
    b.add(edge,'jade',start+.016,{lift:.4});edge.dispose();
    const cols=Math.round((side<2?w:d)*2/.30),rows=Math.max(4,Math.round((side<2?d:w-ridge)/.46));
    for(let row=0;row<rows;row++)for(let col=0;col<cols;col++){
      const tile=grid(4,1,(u,v)=>{
        const p=surface((col+u*.96)/cols,Math.min(1,(row+v*1.08)/rows));p[1]+=.055+Math.sin(u*Math.PI)*.07;return p;
      });
      b.add(tile,'tile',start+.025+(1-row/rows)*.045+col*.00012,{duration:.014,lift:.5,shade:.85+noise(row*43+col*7+side)*.22});tile.dispose();
    }
    const eave:Point[]=[];
    for(let i=0;i<=40;i++){const p=surface(i/40,1);p[1]-=.13;eave.push(p);}
    b.tube(eave,.105,'jade',start+.075,{},40);
    for(let i=0;i<cols;i++){
      const p=surface((i+.5)/cols,1);p[1]+=.03;
      b.sphere(p,[.075,.065,.075],'jade',start+.071,{shade:.9});
    }
    // Visible rafter ends under the eaves.
    for(let i=1;i<cols;i+=2){
      const p=surface(i/cols,.83),q=surface(i/cols,1);p[1]-=.32;q[1]-=.32;
      b.tube([p,q],.045,'wood',start+.02,{},2);
    }
  }
  for(const sx of [-1,1])for(const sz of [-1,1]){
    const points:Point[]=[];
    for(let j=0;j<=16;j++){
      const v=j/16,sv=ornaments?.45+.55*v:v;points.push(place([sx*(ridge+(w-ridge)*v),y+h*Math.pow(1-sv,1.65)+.65*Math.pow(sv,4)+.1,sz*d*sv]));
    }
    b.tube(points,.14,'tile',start+.082,{},24);
    const end=place([sx*w,y+.7,sz*d]);
    b.tube([end,place([sx*(w+.18),y+1.04,sz*(d+.14)]),place([sx*(w+.04),y+1.19,sz*(d+.05)])],.085,'tile',start+.084,{},9);
  }
  b.tube([place([-ridge-.2,y+h+.18,0]),place([0,y+h+.26,0]),place([ridge+.2,y+h+.18,0])],.20,'tile',start+.08,{},20);
  if(ornaments){
    // Closed triangular gables distinguish the top xieshan roof from a hip roof.
    for(const sign of [-1,1]){
      const cap=grid(14,3,(u,v)=>{
        const z=(u*2-1)*d*.45,base=y+h*Math.pow(.55,1.65);
        return place([sign*ridge,base+(y+h*Math.pow(1-Math.abs(z)/d,1.65)-base)*v,z]);
      });
      b.add(cap,'wood',start+.079);cap.dispose();
      b.tube([place([sign*ridge,y+h*.37,-d*.45]),place([sign*ridge,y+h+.08,0]),place([sign*ridge,y+h*.37,d*.45])],.11,'jade',start+.083,{},20);
    }
    for(const sx of [-1,1]){
      // Broad ceramic chiwen silhouette: replace the former wire-like loop.
      const outline=new THREE.Shape();
      outline.moveTo(-.24,0);outline.bezierCurveTo(.23,-.04,.60,.15,.60,.58);
      outline.bezierCurveTo(.65,.89,.63,1.38,.37,1.58);
      outline.bezierCurveTo(.19,1.73,-.12,1.66,-.18,1.42);
      outline.lineTo(.10,1.36);outline.bezierCurveTo(.35,1.14,.10,.94,-.12,.74);
      outline.bezierCurveTo(-.36,.51,-.47,.32,-.24,0);outline.closePath();
      const ornament=new THREE.ExtrudeGeometry(outline,{depth:.30,bevelEnabled:true,bevelSize:.04,bevelThickness:.04,bevelSegments:2,steps:1});
      ornament.translate(0,0,-.15);ornament.scale(sx,1,1);
      ornament.translate(sx*ridge,y+h+.12,0);
      // place() also supports the orientation of projecting roofs.
      const positions=ornament.getAttribute('position');
      for(let i=0;i<positions.count;i++)positions.setXYZ(i,...place([positions.getX(i),positions.getY(i),positions.getZ(i)]));
      ornament.computeVertexNormals();b.add(ornament,'tile',start+.09,{duration:.012,shade:.89});ornament.dispose();
      b.sphere(place([sx*(ridge+.21),y+h+1.35,.20]),[.07,.07,.055],'jade',start+.093);
    }
    b.cylinder(.06,.23,.65,place([0,y+h+.62,0]),'tile',start+.096,{duration:.01});
    b.sphere(place([0,y+h+1,0]),[.13,.17,.13],'tile',start+.098,{duration:.01});
  }
}

function rails(b:HeritageBuilder,y:number,rx:number,start:number,material:SurfaceName='wood',entrance=false,rz=rx,centerZ=0) {
  for(let s=0;s<4;s++){
    const a=s*Math.PI/2,n=20,r=s%2?rz:rx,depth=s%2?rx:rz;
    const point=(x:number,y:number,z:number):Point=>{const p=turn(x,y,z,a);p[2]+=centerZ;return p;};
    for(let i=0;i<=n;i++){
      const x=-r+i*2*r/n;
      if(entrance && s===0 && Math.abs(x)<5.3)continue;
      b.box([.16,.95,.16],point(x,y+.48,depth),material,start+i*.0006,{r:[0,a,0]});
      b.sphere(point(x,y+1.02,depth),[.13,.12,.13],material,start+.016);
      if(i<n && !(entrance && s===0 && Math.abs(x+r/n)<5.5)){
        for(const h of [.18,.58,.91])b.box([r*2/n,.09,.1],point(x+r/n,y+h,depth),material,start+.012,{r:[0,a,0]});
        b.box([.08,.70,.08],point(x+r/n,y+.49,depth),material,start+.016,{r:[0,a,0]});
      }
    }
  }
}

function brackets(b:HeritageBuilder,y:number,rx:number,start:number,rz:number) {
  for(let s=0;s<4;s++){
    const a=s*Math.PI/2,r=s%2?rz:rx,depth=s%2?rx:rz;
    for(let i=-6;i<=6;i++){
      const x=i*r/6.1;
      for(let k=0;k<3;k++){
        b.box([.48+k*.2,.13,.24],turn(x,y+k*.18,depth+k*.15,a),'jade',start+k*.005,{r:[0,a,0]});
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
    for(const h of [height-.38,height-.12])b.box([r*2,.19,.28],turn(0,floor+h,depth,a),'jade',start+.09,{r:[0,a,0]});
    for(let j=0;j<bays;j++){
      const x=-r+(j+.5)*2*r/bays,bay=2*r/bays-.34;
      // Pale ornament belongs to the lintel, not a hanging fabric curtain.
      b.tube([turn(x-bay*.42,floor+height-.5,depth+.17,a),turn(x,floor+height-.69,depth+.17,a),turn(x+bay*.42,floor+height-.5,depth+.17,a)],.04,'stone',start+.14,{},8);
    }
  }
  // Lower hall is visibly split by the corridor eave; its upper register is
  // a narrow clerestory, not one six-metre-tall row of doors.
  if(index===0){
    addFacade(b,{floor,height:3.52,rx,rz,baysX,baysZ,start,mode:'doors'});
    addFacade(b,{floor:floor+4.12,height:height-4.12,rx,rz,baysX,baysZ,start:start+.025,mode:'windows'});
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
      b.tube([turn(x-r/bays*.78,floor+height-.2,d+.14,a),turn(x,floor+height-.38,d+.14,a),turn(x+r/bays*.78,floor+height-.2,d+.14,a)],.04,'stone',.253,{},6);
    }
  }
  brackets(b,roofY-.8,rx,.252,rz);
  hipRoof(b,roofY,rx+1.8,rz+1.65,1.40,.27);
  for(let side=0;side<4;side++){
    const a=side*Math.PI/2,d=side%2?rx:rz,bays=side%2?3:5,half=bays*1.08;
    for(let j=0;j<=bays;j++){
      const x=-half+j*2*half/bays;
      b.cylinder(.12,.17,height-.04,turn(x,floor+height/2,d+1.15,a),'wood',.229+j*.002);
      b.cylinder(.22,.26,.22,turn(x,floor+.11,d+1.15,a),'stone',.21);
    }
    b.box([half*2+.3,.25,.35],turn(0,floor+height,d+1.15,a),'jade',.252,{r:[0,a,0]});
    hipRoof(b,roofY-.10,half+.72,2.6,1.38,.279,turn(0,0,d-.8,a),a);
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
  terraceBlock(TOWER.terrace.width,TOWER.terrace.depth,-4,6.6,.006);
  terraceBlock(23,7,15.1,4.4,.018);
  terraceBlock(27,7,22.1,2.2,.03);
  const flight=(base:number,front:number,run:number,width:number,start:number,cx=0,steps=11)=>{
    for(let i=0;i<steps;i++){
      const top=base+(i+1)*.2;
      b.box([width,top,run/steps+.02],[cx,top/2,front-i*run/steps],'stone',start+i*.0017,{lift:.4,shade:.96});
    }
    for(const sign of [-1,1]){
      const x=cx+sign*(width/2+.12);
      b.tube([[x,base+.8,front+.12],[x,base+steps*.2+.7,front-run+.3]],.10,'stone',start+.021,{},2);
      for(let i=0;i<6;i++){
        const z=front-i*run/5,y=base+i*steps*.2/5;
        b.box([.18,.8,.18],[x,y+.4,z],'stone',start+.025);
        b.sphere([x,y+.9,z],[.13,.12,.13],'stone',start+.027);
      }
    }
  };
  flight(0,29.7,4.1,10,.051);
  flight(2.2,22.7,4.1,10,.079);
  flight(4.4,14.7,4.1,10,.105);
  // Lateral stairways reach the main terrace beside the central landings.
  flight(2.2,18.7,8.1,3,.08,-14.5,22);
  flight(2.2,18.7,8.1,3,.08,14.5,22);
  rails(b,6.6,16.6,.121,'stone',true,14.2,-4);
  lowerCorridor(b);
  for(const [index,level] of TOWER.halls.entries()){
    const depth=level.depth;
    hall(b,level,index);
    const next=TOWER.halls[index+1];
    if(next){
      const low=level.floor+level.height,high=next.floor;
      b.box([next.radius*1.85,high-low,next.depth*1.85],[0,(low+high)/2,0],'recess',level.start+.15,{duration:.02,lift:.6});
    }
    brackets(b,level.roofY-.8,level.radius,level.start+.153,depth);
    hipRoof(b,level.roofY,level.roofRadius,level.roofDepth,level.roofHeight,level.start+.18,[0,0,0],0,index===2);
    if(index>0){
      const gx=level.radius+(index===2?1.5:1.15),gz=depth+1.15;
      // Photo evidence: a thick projecting deck + brackets, not a second
      // independent tiled roof between each principal eave and its balustrade.
      b.box([2*gx,.35,2*gz],[0,level.floor-.18,0],'stone',level.start);
      b.box([2*gx+.18,.11,2*gz+.18],[0,level.floor-.4,0],'jade',level.start+.007);
      rails(b,level.floor,gx,level.start+.035,'stone',false,gz);
      brackets(b,level.floor-1.18,gx-.48,level.start+.013,gz-.48);
      // Radial tails connect the projecting brackets back into the inner core.
      for(let side=0;side<4;side++){
        const angle=side*Math.PI/2,span=side%2?gz:gx;
        const outer=(side%2?gx:gz)-.40,inner=(side%2?level.radius:depth)*.82;
        for(let n=-5;n<=5;n++)b.box([.19,.24,outer-inner+.42],
          turn(n*span/5.6,level.floor-.62,(inner+outer)/2,angle),'wood',level.start+.012,{r:[0,angle,0]});
      }
    }
  }
  // Four upper projecting galleries. Front/back are three bays, with columns
  // and the projecting eave sharing one extent rather than floating canopies.
  const top=TOWER.halls[2];
  for(let side=0;side<4;side++){
    const a=side*Math.PI/2,d=side%2?top.radius:top.depth,half=3.24;
    const outer=d+1.10;
    for(const x of [-half,-half/3,half/3,half]){
      b.cylinder(.115,.155,top.height+.04,turn(x,top.floor+top.height/2,outer,a),'wood',.732,{lift:1.1});
      b.cylinder(.22,.25,.18,turn(x,top.floor+.09,outer,a),'stone',.718);
    }
    b.box([half*2+.3,.23,.35],turn(0,top.floor+top.height+.10,outer,a),'jade',.78,{r:[0,a,0]});
    hipRoof(b,top.roofY-.39,half+.6,2.0,1.26,.817,turn(0,0,d-.1,a),a);
  }
}

/** Only labels identifiable in a located front-elevation photograph are used.
 * Horizontal 文萃李唐 reads right-to-left; top-floor 鸛雀樓 reads top-to-bottom.
 * Other elevations / couplet inscriptions are deliberately untranscribed.
 */
export const PLAQUES = [
  {id:'entrance-front',text:'文萃李唐',direction:'rtl',width:2.8,height:.91,position:[0,9.71,8.96] as Point,at:.37},
  {id:'top-front',text:'鸛雀樓',direction:'vertical',width:.77,height:2.06,position:[0,25.10,4.66] as Point,at:.92},
] as const;

export function addPlaques(scene:THREE.Scene) {
  const objects:{group:THREE.Group;at:number}[]=[],resources:{dispose():void}[]=[];
  // Locations and blue/gold boards are visible; their precise inscriptions are
  // pending same-elevation verification. Empty text is intentional, not invented.
  const untranscribedCouplets=[-1,1].map(sign=>({id:`entrance-couplet-${sign}`,text:'',direction:'vertical',width:.26,height:2.48,position:[sign*1.08,8.05,8.87] as Point,at:.37}));
  for(const spec of [...PLAQUES,...untranscribedCouplets]){
    const vertical=spec.direction==='vertical',canvas=document.createElement('canvas');
    canvas.width=vertical?384:1024;canvas.height=vertical?1024:384;
    const ctx=canvas.getContext('2d')!,w=canvas.width,h=canvas.height;
    ctx.fillStyle='#29226b';ctx.fillRect(0,0,w,h);
    ctx.strokeStyle='#b8984e';ctx.lineWidth=13;ctx.strokeRect(12,12,w-24,h-24);
    ctx.lineWidth=3;ctx.strokeRect(33,33,w-66,h-66);
    // Simplified carved border, separate from the calligraphic face.
    for(let x=50;x<w-30;x+=36)for(const y of [23,h-23]){
      ctx.beginPath();ctx.ellipse(x,y,10,5,0,0,Math.PI*2);ctx.stroke();
    }
    ctx.fillStyle='#d9bd76';ctx.textAlign='center';ctx.textBaseline='middle';
    ctx.font=`${vertical?248:235}px "Kaiti SC", "STKaiti", "KaiTi", "Songti SC", serif`;
    const chars=Array.from(spec.text);
    if(vertical)chars.forEach((c,i)=>ctx.fillText(c,w/2,177+i*327));
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
