import { Component, useCallback, useEffect, useRef, useState, type ReactNode } from 'react';
import PagodaThreeScene, { DETAIL_VIEWS, type DetailView } from './PagodaThreeScene';
import { DURATION, STAGES, clampProgress, stageAt } from './timeline';
import { EXPORT_MODE } from './export-contract';

class SceneBoundary extends Component<{children:ReactNode},{failed:boolean}> {
  state={failed:false};
  static getDerivedStateFromError(){return {failed:true};}
  render(){return this.state.failed?<div className="scene-loading" role="alert">三维场景未能加载<br/><small>请使用支持 WebGL2 的浏览器，并开启硬件加速。</small></div>:this.props.children;}
}
export default function App(){
  const [progress,setProgress]=useState(0),[playing,setPlaying]=useState(()=>!EXPORT_MODE&&!matchMedia('(prefers-reduced-motion: reduce)').matches);
  const [ready,setReady]=useState(false),[view,setView]=useState<DetailView>('overview');
  const [speed,setSpeed]=useState(1),[cameraRequest,setCameraRequest]=useState(0);
  const progressRef=useRef(0);
  const onReady=useCallback(()=>setReady(true),[]);
  const seek=useCallback((p:number)=>{const next=clampProgress(p);progressRef.current=next;setProgress(next);},[]);
  useEffect(()=>{
    if(!ready||!playing)return;
    let frame=0,last=performance.now();
    const tick=(now:number)=>{
      const dt=document.hidden?0:Math.min((now-last)/1000,.1);last=now;
      const next=clampProgress(progressRef.current+dt*speed/DURATION);seek(next);
      if(next===1)setPlaying(false);else frame=requestAnimationFrame(tick);
    };
    frame=requestAnimationFrame(tick);return()=>cancelAnimationFrame(frame);
  },[ready,playing,speed,seek]);
  const replay=()=>{setView('overview');setCameraRequest(n=>n+1);seek(0);setPlaying(true);};
  const toggle=()=>{if(progress===1){seek(0);setPlaying(true);}else setPlaying(p=>!p);};
  const detail=(v:DetailView)=>{setView(v);setCameraRequest(n=>n+1);seek(1);setPlaying(false);};
  if(EXPORT_MODE)return <main className="film" data-adapter-id="guanque">
    <header className="film-title"><span>山河营造 · 中国名楼</span><h1>鹳雀楼</h1><p>GUANQUE TOWER</p></header>
    <SceneBoundary><PagodaThreeScene progress={0} onReady={onReady}/></SceneBoundary>
    {!ready&&<div className="scene-loading">正在展开三维画卷…</div>}
    <footer className="film-caption"><p className="film-phase">一砖一瓦，重见营造之美</p><span>程序化艺术重现 · 非测绘复原</span></footer>
  </main>;
  return <main className="exhibition" data-progress={progress.toFixed(4)} data-playing={playing} data-view={view}>
    <header className="masthead"><a className="brand" href="#"><span className="seal">营</span><span>山河营造<small>ARCHITECTURE IN MOTION</small></span></a><div className="edition">中国名楼 · 零一<span>山西 · 永济</span></div><button className="replay" disabled={!ready} onClick={replay}>重新营造 <span>↻</span></button></header>
    <section className="gallery">
      <aside className="introduction"><div className="eyebrow"><span/>黄河东岸 · 千古名楼</div><h2>欲穷千里目，<br/>更上一层楼。</h2><p className="poet">唐 · 王之涣《登鹳雀楼》</p><div className="fine-rule"/><p className="intro-copy">从一方础石，到四檐凌空。<br/>循着梁柱与砖瓦，<br/>看一座名楼缓缓生长。</p><div className="architectural-note"><b>三层四檐</b><span>高台 · 回廊 · 飞檐</span></div></aside>
      <div className="tower-stage"><div className="stage-label"><span className={playing?'pulse':''}/>{ready?stageAt(progress):'展卷 · 备料中'}<b>{Math.round(progress*100)}<small>%</small></b></div>
        <SceneBoundary><PagodaThreeScene progress={progress} view={view} cameraRequest={cameraRequest} onReady={onReady}/></SceneBoundary>
        {!ready&&<div className="scene-loading">正在展开三维画卷…</div>}
        <div className="view-controls" role="group" aria-label="观赏视角">{DETAIL_VIEWS.map(({id,label})=><button key={id} disabled={!ready} aria-pressed={view===id} onClick={()=>detail(id)}>{label}</button>)}</div>
        <div className="orbit-hint"><span>⌘</span> 拖动环视 <i/> 滚轮缩放</div>
      </div>
      <aside className="tower-title"><span className="catalogue">GUANQUE TOWER / 001</span><h1>鹳雀楼</h1><div className="red-seal">更上<br/>层楼</div><p>白日依山尽<br/>黄河入海流</p></aside>
    </section>
    <footer className="control-deck"><div className="timeline-heading"><span>营造长卷 <small>CONSTRUCTION SEQUENCE</small></span><span className="method">程序化艺术重现</span></div><div className="playback"><button className="play" disabled={!ready} onClick={toggle} aria-label={playing?'暂停':'播放'}>{playing?'Ⅱ':'▶'}</button><div className="timeline"><div className="track"><span style={{width:`${progress*100}%`}}/>{STAGES.slice(0,-1).map(s=><i key={s.end} style={{left:`${s.end*100}%`}}/>)}</div><input aria-label="施工进度" type="range" min="0" max="1000" disabled={!ready} value={Math.round(progress*1000)} onChange={e=>{setPlaying(false);seek(Number(e.target.value)/1000);}}/><div className="milestones"><span>筑台</span><span>立柱</span><span>登阁</span><span>重檐</span><span>落成</span></div></div><button className="speed" aria-label="切换播放速度" onClick={()=>setSpeed(s=>s===1?2:s===2?.5:1)}>{speed}×</button><time>{(progress*DURATION).toFixed(1)}<span> / {DURATION.toFixed(1)} s</span></time></div><div className="bottomline"><span>一砖一瓦，重见营造之美。</span><span>THREE DIMENSIONS · A THOUSAND YEARS</span></div></footer>
  </main>;
}
