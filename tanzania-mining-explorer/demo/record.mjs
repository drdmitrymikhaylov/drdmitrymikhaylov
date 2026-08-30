import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';

const TL   = JSON.parse(readFileSync(new URL('./timeline.json', import.meta.url)));
const CAPS = JSON.parse(readFileSync(new URL('./captions.json', import.meta.url)));
const SEG  = Object.fromEntries(TL.segments.map(s=>[s.name,s]));

const b = await chromium.launch();
const ctx = await b.newContext({ viewport:{width:1920,height:1080}, deviceScaleFactor:1 });
const p = await ctx.newPage();
p.on('pageerror',e=>console.log('PAGEERROR',e.message));

/* Demo chrome — brand cards, caption bar, cursor — present from first paint */
await p.addInitScript({content:`
document.addEventListener('DOMContentLoaded',()=>{
  const css=document.createElement('style');
  css.textContent=\`
  #demo-root{position:fixed;inset:0;z-index:500;pointer-events:none;font-family:"Archivo","Helvetica Neue",Arial,sans-serif}
  .brandcard{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;
    background:radial-gradient(1200px 700px at 30% 20%, #0B3A5C 0%, #062A45 55%, #041D31 100%);
    opacity:1;transition:opacity .7s ease;z-index:600}
  .brandcard.gone{opacity:0}
  .bc-mark{display:flex;align-items:center;gap:14px;margin-bottom:34px}
  .bc-bars{display:flex;gap:4px;align-items:flex-end}
  .bc-bars i{width:9px;background:#19B5D5;border-radius:1px;display:block}
  .bc-word{font-size:26px;font-weight:700;letter-spacing:.34em;color:#F2F7FA}
  .bc-word small{display:block;font-size:11px;font-weight:500;letter-spacing:.42em;color:#8FB8CC;margin-top:6px}
  .bc-rule{width:64px;height:2px;background:#19B5D5;margin:6px 0 30px}
  .bc-title{font-size:56px;font-weight:700;letter-spacing:-.015em;color:#FFFFFF;text-align:center}
  .bc-sub{font-size:19px;font-weight:400;color:#A9C6D6;margin-top:14px;letter-spacing:.02em}
  .bc-note{position:absolute;bottom:36px;font-size:12px;letter-spacing:.18em;color:#5E88A0;text-transform:uppercase}
  #capbar{position:absolute;left:50%;bottom:34px;transform:translateX(-50%);max-width:1100px;
    display:flex;align-items:center;gap:14px;padding:13px 22px;border-radius:6px;
    background:rgba(4,17,27,.88);border:1px solid rgba(25,181,213,.35);
    box-shadow:0 10px 34px rgba(0,0,0,.55);opacity:0;transition:opacity .25s ease;z-index:560}
  #capbar.on{opacity:1}
  #capbar .tag{flex:none;font-size:9.5px;font-weight:700;letter-spacing:.22em;color:#19B5D5;
    border:1px solid rgba(25,181,213,.5);border-radius:3px;padding:3px 7px;white-space:nowrap}
  #capbar .txt{font-size:21px;font-weight:500;color:#F4F8FA;line-height:1.35;text-align:center}
  #democur{position:absolute;left:0;top:0;z-index:640;transition:transform .55s cubic-bezier(.25,.6,.25,1);will-change:transform}
  #democur svg{filter:drop-shadow(0 2px 5px rgba(0,0,0,.6))}
  .ripple{position:absolute;width:14px;height:14px;border-radius:50%;border:2.5px solid #19B5D5;z-index:630;
    animation:rip .55s ease-out forwards;pointer-events:none}
  @keyframes rip{from{transform:translate(-50%,-50%) scale(.5);opacity:.95}to{transform:translate(-50%,-50%) scale(3.4);opacity:0}}\`;
  document.head.appendChild(css);

  const root=document.createElement('div'); root.id='demo-root';
  const bars=(h)=>'<span class="bc-bars">'+h.map(v=>'<i style="height:'+v+'px"></i>').join('')+'</span>';
  root.innerHTML=\`
    <div class="brandcard" id="card-in">
      <div class="bc-mark">\${bars([16,26,38,30,20])}<span class="bc-word">AD PORTS GROUP<small>RESEARCH &amp; INNOVATION</small></span></div>
      <div class="bc-rule"></div>
      <div class="bc-title">Ngao Exploration Console</div>
      <div class="bc-sub">Mineral targeting for Tanzania · hyperspectral remote sensing · tenure intelligence</div>
      <div class="bc-note">Technology demonstrator — synthetic tenure &amp; assay data</div>
    </div>
    <div class="brandcard" id="card-out" style="opacity:0">
      <div class="bc-mark">\${bars([16,26,38,30,20])}<span class="bc-word">AD PORTS GROUP<small>RESEARCH &amp; INNOVATION</small></span></div>
      <div class="bc-rule"></div>
      <div class="bc-title">Find the licence first.</div>
      <div class="bc-sub">Ngao Exploration Console — a research prototype by Prof. Dr. Dmitry Mikhaylov</div>
    </div>
    <div id="capbar"><span class="tag">AD PORTS · R&amp;I</span><span class="txt"></span></div>
    <div id="democur" style="transform:translate(960px,760px)">
      <svg width="26" height="30" viewBox="0 0 26 30"><path d="M2 2 L2 24 L8.5 18.5 L12.5 27 L16.5 25 L12.5 17 L21 16 Z"
        fill="#FFFFFF" stroke="#062A45" stroke-width="1.6" stroke-linejoin="round"/></svg>
    </div>\`;
  document.body.appendChild(root);

  window.__demo={
    cur(x,y,ms){const c=document.getElementById('democur');c.style.transitionDuration=(ms||550)+'ms';c.style.transform='translate('+x+'px,'+y+'px)';},
    ripple(x,y){const r=document.createElement('div');r.className='ripple';r.style.left=x+'px';r.style.top=y+'px';
      document.getElementById('demo-root').appendChild(r);setTimeout(()=>r.remove(),650);},
    cap(t){const b=document.getElementById('capbar');if(!t){b.classList.remove('on');return;}
      b.querySelector('.txt').textContent=t;b.classList.add('on');},
    card(id,on){document.getElementById(id).classList.toggle('gone',!on);document.getElementById(id).style.opacity=on?'1':'0';},
    fly(lng,lat,zoom,ms){const v=view;if(!v)return;const a={lng:v.lng,lat:v.lat,z:v.zoom},t0=performance.now();
      const step=(t)=>{const u=Math.min(1,(t-t0)/ms),e=u<.5?2*u*u:1-Math.pow(-2*u+2,2)/2;
        v.lng=a.lng+(lng-a.lng)*e;v.lat=a.lat+(lat-a.lat)*e;v.zoom=a.z+(zoom-a.z)*e;render();
        if(u<1)requestAnimationFrame(step);};requestAnimationFrame(step);},
  };
});
`});

await p.goto('file:///home/user/drdmitrymikhaylov/tanzania-mining-explorer/index.html',{waitUntil:'load'});
await p.waitForTimeout(400);
await p.evaluate(()=>{ document.getElementById('toasts').style.display='none'; });
await p.waitForFunction(()=>typeof TARGETS!=='undefined' && !!window.__demo);
await p.evaluate(()=>document.fonts.ready.then(()=>{}));
await p.waitForTimeout(600);

/* ── frame capture: CDP screencast with wall-clock stamps ── */
mkdirSync('frames',{recursive:true});
const cdp = await ctx.newCDPSession(p);
const frames = [];            // {t, file}
let fi = 0;
cdp.on('Page.screencastFrame', ev => {
  const f = `frames/f${String(fi++).padStart(5,'0')}.jpg`;
  writeFileSync(f, Buffer.from(ev.data,'base64'));
  frames.push({t: ev.metadata.timestamp*1000, file: f});
  cdp.send('Page.screencastFrameAck',{sessionId: ev.sessionId}).catch(()=>{});
});
await cdp.send('Page.startScreencast',{format:'jpeg',quality:85,maxWidth:1920,maxHeight:1080,everyNthFrame:1});
await p.waitForTimeout(300);

/* ── helpers ─────────────────────────────────────────────── */
const t0 = Date.now();
const now = ()=> (Date.now()-t0)/1000;
const until = async (t)=>{ const d=t*1000-(Date.now()-t0); if(d>0) await p.waitForTimeout(d); };
const center = async (sel)=>{ const el=p.locator(sel).first(); await el.scrollIntoViewIfNeeded().catch(()=>{});
  const bb=await el.boundingBox(); if(!bb) throw new Error('no bb '+sel); return {x:bb.x+bb.width/2, y:bb.y+bb.height/2}; };
const moveCur = async (x,y,ms=550)=>{ await p.evaluate(([x,y,ms])=>__demo.cur(x-2,y-2,ms),[x,y,ms]); await p.waitForTimeout(ms+60); };
const click = async (sel,ms=550)=>{ const c=await center(sel); await moveCur(c.x,c.y,ms);
  await p.evaluate(([x,y])=>__demo.ripple(x,y),[c.x,c.y]); await p.mouse.click(c.x,c.y); await p.waitForTimeout(120); };
const glide = async (x1,y1,x2,y2,ms)=>{ // map hover sweep: fake cursor + real pointermoves
  await p.evaluate(([x,y,ms])=>__demo.cur(x-2,y-2,ms),[x2,y2,ms]);
  const steps=Math.max(8,Math.round(ms/70));
  for(let i=0;i<=steps;i++){ await p.mouse.move(x1+(x2-x1)*i/steps, y1+(y2-y1)*i/steps); await p.waitForTimeout(ms/steps); } };

/* caption scheduler — fire alongside actions */
(async ()=>{ for(const c of CAPS){ await until(c.t); await p.evaluate(t=>__demo.cap(t),c.text);
  } })();
(async ()=>{ // clear caption in gaps between segments
  const ends = TL.segments.map(s=>{ const cs=CAPS.filter(c=>c.t>=s.start-0.01 && c.t<s.start+s.dur); return cs.length?Math.max(...cs.map(c=>c.end)):s.start+s.dur; });
  for(const e of ends){ await until(e); await p.evaluate(()=>__demo.cap(null)); } })();

/* ── scenario ────────────────────────────────────────────── */
// s1: brand card holds, then reveals the console
await until(4.6);  await p.evaluate(()=>__demo.card('card-in',false));

// s2: choose Rare earth → heat redraw → sweep across the Songwe district
await until(SEG.s2.start+0.6);
await click('#commodities .cmd:nth-child(4)', 650);
await until(SEG.s2.start+3.4);
{ const bb=await p.locator('#mapcanvas').boundingBox();
  await glide(bb.x+bb.width*0.42,bb.y+bb.height*0.62, bb.x+bb.width*0.50,bb.y+bb.height*0.70, 1500);
  await glide(bb.x+bb.width*0.50,bb.y+bb.height*0.70, bb.x+bb.width*0.44,bb.y+bb.height*0.30, 2200); }

// s3: tenure → click a strong producing licence → open its passport
await until(SEG.s3.start-0.2);
await click('.tab[data-mode="tenure"]', 600);
await until(SEG.s3.start+1.6);
{ const rel=await p.evaluate(()=>{ const l=LICENCES.filter(x=>!x.ours&&x.producing&&x.score>=78&&x.cy>-9&&x.cy<-2)[0]
      ||LICENCES.find(x=>!x.ours&&x.producing)||LICENCES.find(x=>!x.ours);
    return {x:PX(l.cx),y:PY(l.cy)}; });
  const bb=await p.locator('#mapcanvas').boundingBox();
  const pt={x:bb.x+rel.x, y:bb.y+rel.y};
  await moveCur(pt.x,pt.y,700);
  await p.evaluate(([x,y])=>__demo.ripple(x,y),[pt.x,pt.y]);
  await p.mouse.click(pt.x,pt.y); }
await until(SEG.s3.start+4.2);
await click('#act-passport2', 600);

// s4: close passport → animated zoom to the block → infra + score visible
await until(SEG.s4.start+0.3);
await click('#modal-x', 450);
await p.evaluate(()=>{ const f=selectedFeature(); if(f) __demo.fly(f.cx,f.cy,8.6,1600); });
await until(SEG.s4.start+3.2);
{ const c=await center('#dossier .sbars'); await moveCur(c.x,c.y-20,700); }

// s5: targeting → top-ranked open block → draft the peg application
await until(SEG.s5.start+0.2);
await p.evaluate(()=>__demo.fly((28.9+40.9)/2,-6.55,5.8,1100));
await click('.tab[data-mode="target"]', 600);
await until(SEG.s5.start+1.9);
await click('#drawer-body tbody tr:nth-child(1)', 650);
await until(SEG.s5.start+4.4);
await click('#act-peg', 650);

// s6: our ground → Nyakafulu → open the drilling report and scroll it
await until(SEG.s6.start-0.3);
await click('#modal-x', 400);
await click('.tab[data-mode="ground"]', 550);
await until(SEG.s6.start+1.5);
await click('#dossier [data-lic="P1"]', 650);
await until(SEG.s6.start+3.4);
await click('#dossier [data-report]', 650);
await until(SEG.s6.start+5.2);
{ const bb=await p.locator('.modal-body').boundingBox();
  await p.mouse.move(bb.x+bb.width/2,bb.y+bb.height/2);
  for(let i=0;i<10;i++){ await p.mouse.wheel(0,130); await p.waitForTimeout(110);} }

// s7: lab queue → the backlog → click the worst overdue batch
await until(SEG.s7.start-0.2);
await click('#modal-x', 400);
await click('.tab[data-mode="lab"]', 550);
await until(SEG.s7.start+2.2);
await click('#drawer-body tbody tr:nth-child(1)', 700);
await until(SEG.s7.start+4.6);
{ const c=await center('#dossier .note'); await moveCur(c.x,c.y,600); }

// s8: outro card
await until(SEG.s8.start-0.25);
await p.evaluate(()=>{ __demo.cap(null); document.getElementById('card-out').style.transition='opacity .7s ease';
  document.getElementById('card-out').style.opacity='1'; });
await until(TL.total);

await cdp.send('Page.stopScreencast').catch(()=>{});
await p.waitForTimeout(200);
const rel = frames.map(f=>({t:(f.t-t0)/1000, file:f.file}));
writeFileSync('frames.json', JSON.stringify({total:TL.total, frames:rel}));
console.log('captured', frames.length, 'frames; scenario seconds', now().toFixed(1));
await ctx.close(); await b.close();
