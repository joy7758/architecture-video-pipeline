/** Guanque Tower: a photo-informed, artistic exterior, not a measured survey.
 * Units are scene units. Four eave bands + three principal halls on a high terrace.
 * Every component receives deterministic assembly timing through HeritageBuilder.
 */
import * as THREE from 'three';
import { HeritageBuilder, type Point } from './builder';
import type { SurfaceName } from './materials';

export const TOWER = {
  terrace: { width: 34, depth: 29.2, height: 6.6 },
  halls: [
    { floor: 6.6, height: 5.0, radius: 8.2, roofY: 12.35, roofRadius: 10.6, start: .15 },
    { floor: 14.6, height: 4.7, radius: 7.7, roofY: 20.05, roofRadius: 9.05, start: .40 },
    { floor: 22.2, height: 4.45, radius: 6.25, roofY: 27.4, roofRadius: 7.85, start: .67 },
  ],
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
    b.tube(points,.14,'bronze',start+.082,{},24);
    const end=place([sx*w,y+.7,sz*d]);
    b.tube([end,place([sx*(w+.18),y+1.04,sz*(d+.14)]),place([sx*(w+.04),y+1.19,sz*(d+.05)])],.085,'bronze',start+.084,{},9);
  }
  b.tube([place([-ridge-.2,y+h+.18,0]),place([0,y+h+.26,0]),place([ridge+.2,y+h+.18,0])],.20,'bronze',start+.08,{},20);
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
      const points:Point[]=[[sx*ridge,y+h+.18,0],[sx*(ridge+.4),y+h+.7,0],[sx*(ridge+.35),y+h+1.4,0],[sx*(ridge-.03),y+h+1.6,0],[sx*(ridge-.32),y+h+1.23,0]];
      b.tube(points.map(place),.19,'bronze',start+.091,{duration:.012},20);
      b.sphere(place([sx*(ridge+.18),y+h+.83,0]),[.35,.6,.18],'bronze',start+.09);
    }
    b.cylinder(.06,.23,.65,place([0,y+h+.62,0]),'bronze',start+.096,{duration:.01});
    b.sphere(place([0,y+h+1,0]),[.13,.17,.13],'bronze',start+.098,{duration:.01});
  }
}

function rails(b:HeritageBuilder,y:number,rx:number,start:number,material:SurfaceName='wood',entrance=false,rz=rx,centerZ=0) {
  for(let s=0;s<4;s++){
    const a=s*Math.PI/2,n=20,r=s%2?rz:rx,depth=s%2?rx:rz;
    const point=(x:number,y:number,z:number):Point=>{const p=turn(x,y,z,a);p[2]+=centerZ;return p;};
    for(let i=0;i<=n;i++){
      const x=-r+i*2*r/n;
      if(entrance && s===0 && Math.abs(x)<3.3)continue;
      b.box([.16,.95,.16],point(x,y+.48,depth),material,start+i*.0006,{r:[0,a,0]});
      b.sphere(point(x,y+1.02,depth),[.13,.12,.13],material,start+.016);
      if(i<n && !(entrance && s===0 && Math.abs(x+r/n)<3.5)){
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

function hall(b:HeritageBuilder,floor:number,height:number,rx:number,start:number,rz:number) {
  b.box([rx*2+.4,.28,rz*2+.4],[0,floor-.12,0],'stone',start,{duration:.025});
  for(let side=0;side<4;side++){
    const a=side*Math.PI/2,bays=side%2?5:7,r=side%2?rz:rx,depth=side%2?rx:rz;
    for(let j=0;j<=bays;j++){
      const x=-r+j*2*r/bays;
      b.cylinder(.24,.32,.30,turn(x,floor+.15,depth,a),'stone',start+.025);
      b.cylinder(.18,.24,height-.25,turn(x,floor+height/2+.15,depth,a),'wood',start+.05+j*.002,{duration:.025,lift:2.5});
      b.box([.55,.22,.55],turn(x,floor+height-.04,depth,a),'bronze',start+.08);
    }
    // Recessed hall wall, with real gaps between solid door/window frames.
    for(let j=0;j<bays;j++){
      const x=-r+(j+.5)*2*r/bays,bay=2*r/bays-.36,z=depth-.85;
      if(j===Math.floor(bays/2)){
        b.box([bay,.35,.23],turn(x,floor+height-.40,z,a),'wood',start+.105,{r:[0,a,0]});
      }else{
        for(let row=0;row<5;row++)b.box([bay,.18,.26],turn(x,floor+.13+row*.18,z,a),'brick',start+.09+row*.0016,{r:[0,a,0]});
        b.box([bay,height-1.7,.11],turn(x,floor+(height-.1)/2,z-.04,a),'recess',start+.12,{r:[0,a,0]});
        for(let k=0;k<7;k++)b.box([.038,height-1.7,.055],turn(x-bay*.43+k*bay*.86/6,floor+(height-.1)/2,z+.05,a),'bronze',start+.126,{r:[0,a,0]});
        for(const h of [1.2,1.6,height-1.0])b.box([bay,.065,.07],turn(x,floor+h,z+.055,a),'wood',start+.13,{r:[0,a,0]});
      }
      for(const sign of [-1,1])b.box([.15,height-.4,.3],turn(x+sign*bay/2,floor+height/2,z,a),'wood',start+.102,{r:[0,a,0]});
      b.box([bay,.28,.30],turn(x,floor+height-.3,depth,a),'jade',start+.135,{r:[0,a,0]});
      b.tube([turn(x-bay*.4,floor+height-.18,depth+.17,a),turn(x,floor+height-.36,depth+.17,a),turn(x+bay*.4,floor+height-.18,depth+.17,a)],.035,'bronze',start+.14,{},6);
    }
  }
  // Interior beams and columns supply support in every intermediate pose.
  for(const x of [-rx*.55,rx*.55])for(const z of [-rz*.55,rz*.55])b.cylinder(.2,.24,height,[x,floor+height/2,z],'wood',start+.05,{lift:2});
  for(const z of [-rz*.55,rz*.55])b.box([2*rx,.27,.25],[0,floor+height-.15,z],'wood',start+.082);
  b.box([rx*2,.25,rz*2],[0,floor+height+.05,0],'wood',start+.145);
}

export function courtyard(b:HeritageBuilder) {
  b.box([40,.40,47],[0,-.5,6],'stone',-1,{lift:0,shade:.87});
  for(let x=-12;x<=12;x++)for(let z=-11;z<=19;z++)b.box([1.47,.08,1.47],[x*1.50,-.25,z*1.50],'stone',-1,{lift:0,shade:.91+noise(x*71+z)*.10});
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
  terraceBlock(32,22,-3,6.6,.006);
  terraceBlock(22,7,12.5,4.4,.018);
  terraceBlock(26,7,19.5,2.2,.03);
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
  flight(0,27.1,4.1,10,.051);
  flight(2.2,20.1,4.1,9,.079);
  flight(4.4,12.1,4.1,8,.105);
  // Lateral stairways reach the main terrace beside the central landings.
  flight(2.2,16.1,8.1,3,.08,-13.4,22);
  flight(2.2,16.1,8.1,3,.08,13.4,22);
  rails(b,6.6,15.6,.121,'stone',true,10.6,-3);
  for(const [index,level] of TOWER.halls.entries()){
    const depth=level.radius*(index===2?16.8/28.8:25.8/37.8);
    hall(b,level.floor,level.height,level.radius,level.start,depth);
    // Continuous inner core supports the next deck through the roof volume.
    const next=TOWER.halls[index+1];
    if(next){
      const low=level.floor+level.height,high=next.floor;
      b.box([next.radius*1.4,high-low,next.radius*.87],[0,(low+high)/2,0],'brick',level.start+.16,{duration:.02,lift:.6});
    }
    brackets(b,level.roofY-.8,level.radius,level.start+.153,depth);
    hipRoof(b,level.roofY,level.roofRadius,depth+1.9,1.85,level.start+.18,[0,0,0],0,level.start>.6);
    if(level.start>.2){
      // Shallow waist eaves directly beneath each balustraded gallery.
      hipRoof(b,level.floor-.6,level.radius+.85,depth+.85,.40,level.start+.003);
      rails(b,level.floor,level.radius+.35,level.start+.035,'stone',false,depth+.35);
    }
  }
  // Top-level three-bay projecting galleries, supported directly on the deck.
  for(let side=0;side<4;side++){
    const a=side*Math.PI/2,depth=side%2?6.25:6.25*16.8/28.8;
    b.box([4.8,.24,2.4],turn(0,22.13,depth+.75,a),'stone',.713,{r:[0,a,0]});
    for(const x of [-2.1,-.7,.7,2.1]){
      b.cylinder(.14,.18,3.35,turn(x,23.9,depth+1.65,a),'wood',.754,{duration:.02,lift:1.2});
      b.box([1.38,.1,.12],turn(x,23.05,depth+1.68,a),'wood',.77,{r:[0,a,0]});
    }
    b.box([4.7,.3,.4],turn(0,25.65,depth+1.65,a),'jade',.795,{r:[0,a,0]});
    hipRoof(b,25.93,2.9,2.0,1.02,.80,turn(0,0,depth+.30,a),a);
  }
  // Four projecting entrance porches (抱厦): visible central gables and columns.
  for(let side=0;side<4;side++){
    const a=side*Math.PI/2,porchDepth=side%2?8.2:5.6,center=turn(0,0,porchDepth,a);
    for(const x of [-2.65,2.65])for(const z of [porchDepth+.2,porchDepth+2.5]){
      b.cylinder(.19,.24,3.35,turn(x,8.3,z,a),'wood',.23,{duration:.025,lift:1.5});
      b.cylinder(.3,.32,.18,turn(x,6.67,z,a),'stone',.205);
    }
    b.box([5.9,.3,2.9],turn(0,10.02,porchDepth+1.2,a),'jade',.265,{r:[0,a,0]});
    hipRoof(b,10.25,3.65,3.0,1.4,.278,center,a);
  }
}

/** Canvas lettering is applied only to a solid architectural plaque. */
export function addPlaques(scene:THREE.Scene) {
  const canvas=document.createElement('canvas');canvas.width=768;canvas.height=256;
  const ctx=canvas.getContext('2d')!;ctx.fillStyle='#16384a';ctx.fillRect(0,0,768,256);
  ctx.strokeStyle='#c5a76e';ctx.lineWidth=10;ctx.strokeRect(14,14,740,228);ctx.lineWidth=2;ctx.strokeRect(30,30,708,196);
  ctx.fillStyle='#eee0aa';ctx.font='bold 152px "Songti SC", "Noto Serif SC", serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('鹳雀楼',384,137);
  const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;
  const material=new THREE.MeshStandardMaterial({map:texture,roughness:.75});
  const geometry=new THREE.BoxGeometry(3.1,1.05,.16),meshes:THREE.Mesh[]=[];
  for(let s=0;s<4;s++){
    const a=s*Math.PI/2,m=new THREE.Mesh(geometry,[new THREE.MeshStandardMaterial({color:'#745731'}),material,material,material,material,material]);
    m.position.set(...turn(0,9.46,(s%2?8.2:5.6)+2.64,a));m.rotation.y=a;scene.add(m);meshes.push(m);
  }
  return {update(progress:number){meshes.forEach(m=>{m.visible=progress>=.378;});},dispose(){meshes.forEach(m=>{(m.material as THREE.Material[])[0].dispose();m.removeFromParent();});geometry.dispose();material.dispose();texture.dispose();}};
}
