// Otlo runtime v2: scene/element animation, retimed to the voice-over.
// Scenes: <div class="scene" data-s="0" data-e="5">; elements: class="a" data-in="<sec>" [data-pop|data-rise="px"].
// v2 (26 Nov): the hook is on screen from frame one (elements of scene 1 with data-in <= 0.3 start fully visible),
// hard cuts with a quick slide-in instead of fades, a slow push-in on every scene, and scenes shorter than their
// original timing are compressed (so late elements still appear). Optional per-reel hook: window.extra(t).
(function(){
  const clamp=x=>Math.min(1,Math.max(0,x));
  const ease=x=>1-Math.pow(1-clamp(x),3);
  const back=x=>{x=clamp(x);const c=1.70158;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
  const scenes=[...document.querySelectorAll('.scene')];
  window.ORIG=scenes.map(s=>[+s.dataset.s,+s.dataset.e]);
  window.render=function(t){
    scenes.forEach((sc,si)=>{const s=+sc.dataset.s,e=+sc.dataset.e;
      const vis=t>=s-0.01&&t<e;sc.style.display=vis?'flex':'none';if(!vis)return;
      const local=t-s, len=e-s;
      const slide=si===0?0:(1-ease(local/0.22))*120;                 // quick slide-in on the cut
      const zoom=1+0.035*clamp(local/Math.max(len,0.5));             // slow push-in
      sc.style.opacity=1; sc.style.transform=`translateX(${slide}px) scale(${zoom})`; sc.style.transformOrigin='50% 40%';
      for(const el of sc.querySelectorAll('.a')){const i=+el.dataset.in;
        if(si===0&&i<=s+0.3){el.style.opacity=1;el.style.transform=`scale(${1+0.06*(1-ease(local/0.3))})`;el.style.transformOrigin=el.dataset.origin||'left center';continue;}
        const p=(t-i)/0.28; el.style.opacity=ease(p);
        if(el.dataset.pop){el.style.transform=`scale(${0.8+0.2*back(p)})`;el.style.transformOrigin=el.dataset.origin||'left center'}
        else if(el.dataset.rise){el.style.transform=`translateY(${(1-ease((t-i)/0.5))*(+el.dataset.rise)}px)`}
        else el.style.transform=`translateY(${(1-ease(p))*40}px)`;}
    });
    if(window.OTLOFX) window.OTLOFX.update(t);
    if(window.extra) window.extra(t);
  };
  window.renderTimed=function(t,starts,ends){let i=starts.length-1;for(let k=0;k<starts.length;k++){if(t>=starts[k]&&t<ends[k]){i=k;break}}
    const [os,oe]=window.ORIG[i];const local=t-starts[i];const nl=ends[i]-starts[i];const ol=oe-os;
    let tp;
    if(nl<ol){tp=os+local*(ol/nl);}                                  // compress: everything still appears
    else{tp=os+Math.min(local,ol-0.05);}                              // stretch: play, then hold the last state
    window.render(Math.min(tp,oe-0.001));};
  window.addEventListener('load',()=>window.render(0));
})();
