import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { RoomEnvironment } from "three/examples/jsm/environments/RoomEnvironment.js";
import { createHeritageMaterials } from "./heritage/materials";
import { HeritageBuilder } from "./heritage/builder";
import { buildArchitecture, courtyard, addPlaques } from "./heritage/guanque";
import { EXPORT_MODE, validateExportFrame, type ArchitectureExport } from "./export-contract";

/** One discoverable view catalogue supplies both the controls and camera keys. */
export const DETAIL_VIEWS = [
  {id:'overview',label:'全景'},
  {id:'front',label:'正面'},
  {id:'entrance',label:'门脸与匾额'},
  {id:'roof',label:'飞檐细赏'},
] as const;
export type DetailView = typeof DETAIL_VIEWS[number]['id'];
type Props={progress:number;view?:DetailView;cameraRequest?:number;onReady?:()=>void};

export default function PagodaThreeScene({progress,view="overview",cameraRequest=0,onReady}:Props){
  const requestRef=useRef(cameraRequest);
  useEffect(()=>{requestRef.current=cameraRequest;},[cameraRequest]);
  const mountRef=useRef<HTMLDivElement>(null);
  const progressRef=useRef(progress),viewRef=useRef(view),readyRef=useRef(onReady);
  useEffect(()=>{progressRef.current=progress;},[progress]);
  useEffect(()=>{viewRef.current=view;},[view]);
  useEffect(()=>{readyRef.current=onReady;},[onReady]);
  useEffect(()=>{
    const mount=mountRef.current;if(!mount)return;
    const scene=new THREE.Scene();
    const camera=new THREE.PerspectiveCamera(34,1,.1,180);
    camera.position.set(48,35,81);
    const renderer=new THREE.WebGLRenderer({antialias:true,alpha:true,powerPreference:"high-performance",preserveDrawingBuffer:EXPORT_MODE});
    renderer.setPixelRatio(EXPORT_MODE?1:Math.min(devicePixelRatio,window.innerWidth<700?1.5:2));
    renderer.setClearColor(0xf4f1e9,0);
    renderer.outputColorSpace=THREE.SRGBColorSpace;
    renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.13;
    renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFShadowMap;
    // Camera movement does not change a directional light's shadow map.
    renderer.shadowMap.autoUpdate=false;
    mount.appendChild(renderer.domElement);
    const room=new RoomEnvironment(),pmrem=new THREE.PMREMGenerator(renderer);
    const environment=pmrem.fromScene(room,.025);scene.environment=environment.texture;scene.environmentIntensity=.32;
    room.dispose();pmrem.dispose();
    scene.add(new THREE.HemisphereLight(0xfaf7ef,0x706a5c,.72));
    const key=new THREE.DirectionalLight(0xfff2e2,2.4);key.position.set(-22,38,30);key.castShadow=true;
    key.shadow.mapSize.set(2048,2048);key.shadow.camera.left=-28;key.shadow.camera.right=28;
    key.shadow.camera.top=25;key.shadow.camera.bottom=-20;key.shadow.camera.near=.5;key.shadow.camera.far=100;
    key.target.position.set(0,12,0);key.shadow.normalBias=.025;key.shadow.bias=-.00015;key.shadow.radius=3;
    scene.add(key,key.target);
    const fill=new THREE.DirectionalLight(0xe5eced,.55);fill.position.set(25,18,-10);scene.add(fill);
    const rim=new THREE.DirectionalLight(0xfff4de,.7);rim.position.set(-12,30,-24);scene.add(rim);
    const controls=new OrbitControls(camera,renderer.domElement);
    controls.target.set(0,12.5,4.5);controls.enableDamping=true;controls.dampingFactor=.075;
    if(EXPORT_MODE){controls.enabled=false;controls.enableDamping=false;}
    controls.enablePan=true;controls.minDistance=12;controls.maxDistance=110;
    controls.minPolarAngle=.35;controls.maxPolarAngle=Math.PI*.51;
    const materialKit=createHeritageMaterials(renderer),builder=new HeritageBuilder(materialKit.materials);
    courtyard(builder);buildArchitecture(builder);builder.finish(scene);
    const plaques=addPlaques(scene);
    const reducedMotion=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const presets:Record<DetailView,{position:THREE.Vector3;target:THREE.Vector3}>={
      overview:{position:new THREE.Vector3(48,35,81),target:new THREE.Vector3(0,12.5,4.5)},
      roof:{position:new THREE.Vector3(21,33,32),target:new THREE.Vector3(0,25.4,0)},
      front:{position:new THREE.Vector3(0,24,90),target:new THREE.Vector3(0,12.5,4.5)},
      entrance:{position:new THREE.Vector3(7,11.5,29),target:new THREE.Vector3(0,9.7,7.5)},
    };
    let lastRequest=-1;
    let lastView:DetailView="overview",transition=false,raf=0,lastNow=performance.now(),frames=0,elapsed=0;
    let needsFrame=true,lastProgress=-2,lastShadowProgress=-2,lastShadowTime=-Infinity;
    let renderedFrames=0,shadowUpdates=0;
    let renderExport:(()=>void)|undefined;
    const interrupt=()=>{transition=false;};controls.addEventListener("start",interrupt);
    const resize=()=>{
      const w=Math.max(1,mount.clientWidth),h=Math.max(1,mount.clientHeight);
      renderer.setSize(w,h,false);camera.aspect=w/h;
      camera.fov=EXPORT_MODE?48:window.innerWidth<650?48:camera.aspect<.7?48:34;camera.updateProjectionMatrix();
      needsFrame=true;
      renderExport?.();
    };
    const ro=new ResizeObserver(resize);ro.observe(mount);resize();
    builder.progress.value=progressRef.current;plaques.update(progressRef.current);
    renderer.compile(scene,camera);
    const render=(now:number)=>{
      const frameSeconds=(now-lastNow)/1000;
      const dt=Math.min(frameSeconds,.1);lastNow=now;
      builder.progress.value=progressRef.current;plaques.update(progressRef.current);
      if(lastView!==viewRef.current || lastRequest!==requestRef.current){lastView=viewRef.current;lastRequest=requestRef.current;transition=true;}
      if(transition){
        const preset=presets[lastView],amount=reducedMotion?1:1-Math.exp(-dt*5);
        camera.position.lerp(preset.position,amount);controls.target.lerp(preset.target,amount);
        if(camera.position.distanceTo(preset.position)<.02)transition=false;
      }
      const cameraChanged=controls.update();
      const progressChanged=lastProgress!==progressRef.current;
      // Limit construction shadow work to 30 Hz. Final/rewound poses flush
      // immediately, and a paused intermediate pose flushes on the next tick.
      const shadowChanged=lastShadowProgress!==progressRef.current &&
        (now-lastShadowTime>=1000/30 || progressRef.current===0 || progressRef.current===1);
      if(!document.hidden && (needsFrame || cameraChanged || transition || progressChanged || shadowChanged)){
        if(shadowChanged){
          renderer.shadowMap.needsUpdate=true;
          lastShadowProgress=progressRef.current;lastShadowTime=now;shadowUpdates++;
        }
        renderer.render(scene,camera);renderedFrames++;
        needsFrame=false;lastProgress=progressRef.current;
      }
      frames++;elapsed+=frameSeconds;
      if(elapsed>.6){
        mount.dataset.renderStats=JSON.stringify({calls:renderer.info.render.calls,triangles:renderer.info.render.triangles,geometries:renderer.info.memory.geometries,textures:renderer.info.memory.textures,pieces:builder.pieces,fps:Math.round(frames/elapsed),renderFps:Math.round(renderedFrames/elapsed),shadowUpdatesPerSecond:Math.round(shadowUpdates/elapsed),idle:renderedFrames===0,dpr:renderer.getPixelRatio(),shadowLights:1,postPasses:0});
        frames=0;elapsed=0;renderedFrames=0;shadowUpdates=0;
      }
      raf=requestAnimationFrame(render);
    };
    let exportApi:ArchitectureExport|undefined;
    if(EXPORT_MODE){
      // Export owns time and camera completely: no rAF, damping, autoplay or
      // shadow throttling. Re-seeking the same input redraws the same scene.
      renderExport=()=>{
        builder.progress.value=progressRef.current;plaques.update(progressRef.current);
        camera.lookAt(controls.target);camera.updateMatrixWorld(true);
        renderer.shadowMap.needsUpdate=true;
        renderer.render(scene,camera);
        renderer.getContext().finish();
      };
      exportApi={version:"architecture-export.v1",adapterId:"guanque",ready:false,setFrame(frame){
        validateExportFrame(frame);
        progressRef.current=frame.progress;
        camera.position.set(...frame.position);controls.target.set(...frame.target);
        renderExport!();
        return {progress:frame.progress,width:renderer.domElement.width,height:renderer.domElement.height,calls:renderer.info.render.calls,triangles:renderer.info.render.triangles};
      }};
      renderExport();exportApi.ready=true;window.__ARCHITECTURE_EXPORT__=exportApi;
    }else raf=requestAnimationFrame(render);
    readyRef.current?.();
    return()=>{
      if(exportApi){exportApi.ready=false;if(window.__ARCHITECTURE_EXPORT__===exportApi)delete window.__ARCHITECTURE_EXPORT__;}
      cancelAnimationFrame(raf);ro.disconnect();controls.removeEventListener("start",interrupt);controls.dispose();
      plaques.dispose();builder.dispose();materialKit.dispose();environment.dispose();
      key.shadow.map?.dispose();renderer.dispose();renderer.domElement.remove();
    };
  },[]);
  const viewLabel=DETAIL_VIEWS.find(item=>item.id===view)!.label;
  return <div ref={mountRef} className="three-scene" aria-label={`可旋转的三维鹳雀楼搭建动画：${viewLabel}`} />;
}
