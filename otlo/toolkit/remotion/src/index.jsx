// Otlo Remotion project (tested 28 Nov 2026: renders 1080x1920 H.264 with the session's Chromium).
// Use for STRUCTURED EDITS of real footage: partner/business features, event highlights, trailers cut from
// clips a partner supplies, multi-clip timelines with lower thirds. Otlo's animated Reels stay on build.py.
// Render: cd otlo/toolkit/remotion && npm install && npx remotion render src/index.jsx Feature out.mp4 \
//   --browser-executable=$(ls -d /opt/pw-browsers/chromium-*/chrome-linux64/chrome | head -1) --codec=h264 --crf=16 \
//   --props='{"clips":[{"src":"https://.../a.mp4","from":0,"dur":90,"title":"…","sub":"…"}]}'
import {staticFile, registerRoot, Composition, AbsoluteFill, Sequence, OffthreadVideo, Img, useCurrentFrame, interpolate, spring, useVideoConfig} from 'remotion';
import React from 'react';
const Lower = ({title, sub}) => { const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 14}});
  return <div style={{position: 'absolute', left: 80, top: 300, transform: `translateX(${(1 - s) * -900}px)`}}>
    <div style={{background: '#E8B84A', color: '#0B0D14', font: '800 64px Fira Sans, sans-serif', padding: '10px 26px', display: 'inline-block'}}>{title}</div>
    <div style={{marginTop: 10, color: '#FFF8EC', font: '600 40px Fira Sans, sans-serif', textShadow: '0 2px 10px #000'}}>{sub}</div></div>; };
const Clip = ({c}) => { const f = useCurrentFrame(); const src = /^https?:/.test(c.src) ? c.src : staticFile(c.src); const z = interpolate(f, [0, c.dur], [1, 1.08]);
  return <AbsoluteFill style={{background: '#0B0D14', overflow: 'hidden'}}>
    {/\.(mp4|mov|webm)$/i.test(c.src) ? <OffthreadVideo src={src} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${z})`}}/>
      : <Img src={src} style={{width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${z})`}}/>}
    {c.title ? <Lower title={c.title} sub={c.sub}/> : null}</AbsoluteFill>; };
const Feature = ({clips}) => { let at = 0;
  return <AbsoluteFill>{clips.map((c, i) => { const s = at; at += c.dur; return <Sequence key={i} from={s} durationInFrames={c.dur}><Clip c={c}/></Sequence>; })}</AbsoluteFill>; };
const Root = () => <Composition id="Feature" component={Feature} fps={30} width={1080} height={1920}
  durationInFrames={300} defaultProps={{clips: [{src: 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Rani_ki_vav_-_Patan_-_Gujarat_-_Wall_Decorations.jpg/1280px-Rani_ki_vav_-_Patan_-_Gujarat_-_Wall_Decorations.jpg', dur: 300, title: 'Otlo Spotlight', sub: 'Feature template'}]}}
  calculateMetadata={({props}) => ({durationInFrames: props.clips.reduce((a, c) => a + c.dur, 0)})}/>;
registerRoot(Root);
