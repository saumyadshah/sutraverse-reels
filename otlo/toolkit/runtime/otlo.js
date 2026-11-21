// Otlo runtime: generic scene/element animation + retiming to the voice-over.
// Scenes: <div class="scene" data-s="0" data-e="5">; elements: class="a" data-in="<sec>" [data-pop|data-rise="px"].
// Optional per-reel hook: window.extra = function(t){...}  (t is in the scene's ORIGINAL time).
(function(){
  document.querySelectorAll('.band').forEach(b=>{});
  const ease=x=>1-Math.pow(1-Math.min(1,Math.max(0,x)),3);
  const back=x=>{x=Math.min(1,Math.max(0,x));const c=1.70158;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
  const scenes=[...document.querySelectorAll('.scene')];
  window.ORIG=scenes.map(s=>[+s.dataset.s,+s.dataset.e]);
  window.render=function(t){
    for(const sc of scenes){const s=+sc.dataset.s,e=+sc.dataset.e;
      const vis=t>=s-0.01&&t<e;sc.style.display=vis?'flex':'none';if(!vis)continue;
      const out=Math.min(1,Math.max(0,(e-t)/0.35));
      sc.style.opacity=out;sc.style.transform=`translateY(${(1-out)*-30}px)`;
      for(const el of sc.querySelectorAll('.a')){const i=+el.dataset.in;const p=(t-i)/0.5;
        el.style.opacity=ease(p);
        if(el.dataset.pop){el.style.transform=`scale(${0.85+0.15*back(p)})`;el.style.transformOrigin=el.dataset.origin||'left center'}
        else if(el.dataset.rise){el.style.transform=`translateY(${(1-ease((t-i)/0.9))*(+el.dataset.rise)}px)`}
        else el.style.transform=`translateY(${(1-ease(p))*46}px)`;}
    }
    if(window.extra) window.extra(t);
  };
  window.renderTimed=function(t,starts,ends){let i=starts.length-1;for(let k=0;k<starts.length;k++){if(t>=starts[k]&&t<ends[k]){i=k;break}}
    const [os,oe]=window.ORIG[i];const local=t-starts[i];const nl=ends[i]-starts[i];const ol=oe-os;
    let tp; if(local<nl-0.35){tp=os+Math.min(local,ol-0.36)}else{tp=oe-(nl-local)}
    window.render(Math.min(tp,oe-0.001));};
  window.addEventListener('load',()=>window.render(0));
})();
