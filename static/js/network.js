// Minimal network-style background animation for the hero canvas
(function(){
  const canvas = document.getElementById('networkCanvas');
  if(!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width;
  const h = canvas.height;
  const nodes = Array.from({length: 40}, () => ({
    x: Math.random()*w,
    y: Math.random()*h,
    vx: (Math.random()-.5)*0.6,
    vy: (Math.random()-.5)*0.6,
  }));

  function step(){
    ctx.clearRect(0,0,w,h);
    // draw connections
    for(let i=0;i<nodes.length;i++){
      for(let j=i+1;j<nodes.length;j++){
        const a = nodes[i], b = nodes[j];
        const dx = a.x-b.x, dy=a.y-b.y; const d = Math.sqrt(dx*dx+dy*dy);
        if(d<120){
          ctx.globalAlpha = 1 - d/120;
          ctx.strokeStyle = '#9ec5ff';
          ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke();
        }
      }
    }
    ctx.globalAlpha = 1;
    // draw nodes
    for(const n of nodes){
      ctx.fillStyle = '#2563eb';
      ctx.beginPath(); ctx.arc(n.x,n.y,2.2,0,Math.PI*2); ctx.fill();
      n.x += n.vx; n.y += n.vy;
      if(n.x<0||n.x>w) n.vx*=-1; if(n.y<0||n.y>h) n.vy*=-1;
    }
    requestAnimationFrame(step);
  }
  step();
})();
