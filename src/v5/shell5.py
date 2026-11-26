"""Sites for arguing — shared engine v4.
Layout: header (family switcher · sentence that writes itself · search) / index · rows · detail.
Site JS provides on SITE: BLOB(u), ROW(u,Q), DETAIL(u,Q) [if panel], SAY(item,u) -> sentence html,
optional HEAD(item), COLS(item), GROUP(u,item), COPY(u), FEATURE() (home block), COUNT(u) (bool, counts in index)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
JERE = open(os.environ.get('JEREFILE', os.path.join(HERE,'jere.txt'))).read().strip()
OUT = os.environ.get('OUTDIR','/home/claude/preview/v5')
FAMILY = [  # id, name, note
    ('philosophyarguing', 'So you’re arguing about…', 'Philosophy, argued three ways'),
    ('sosureabout', 'So you’re sure about…', 'Uncomfortable facts, sourced'),
    ('crazystudies', 'DiD yOu KnOw…', 'Crazy studies, judged'),
    ('understanding', 'So you want to understand…', 'Each field’s big fights'),
    ('tenbestpapers', 'The ten best papers for…', 'Every field, caught up'),
    ('metaphors', 'Metaphors for…', 'The pictures in how we talk'),
    ('normdictionary', 'Norm Dictionary', 'What people say vs. allow'),
]

BASE_CSS = r'''
:root{--s1:4px;--s2:8px;--s3:12px;--s4:16px;--s6:24px;--s8:32px;--mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;--left:260px;--right:420px;--top:64px;--label:var(--text)}
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{background:var(--bg);color:var(--fg);font:400 14.5px/1.45 var(--text);display:grid;grid-template:var(--top) 1fr / var(--left) minmax(0,1fr) var(--right);overflow:hidden}
body.nopanel{grid-template-columns:var(--left) minmax(0,1fr)}body.nopanel aside{display:none}
body.home aside{display:none}body.home{grid-template-columns:var(--left) minmax(0,1fr)}
button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer;text-align:inherit}
a{color:inherit;text-decoration-color:var(--line);text-underline-offset:3px}
mark{background:var(--hl);color:inherit;border-radius:2px}
.m{font-family:var(--mono);font-size:11px;letter-spacing:.01em;color:var(--dim);font-variant-numeric:tabular-nums}
/* header */
header{grid-column:1/-1;display:flex;align-items:center;gap:var(--s4);padding:0 var(--s4);border-bottom:1px solid var(--line);background:var(--bar,var(--bg));color:var(--barfg,var(--fg));min-width:0;position:relative;z-index:20}
.fam{flex:none;display:flex;align-items:center;gap:6px;font:500 12px var(--text);color:var(--bardim,var(--dim));padding:6px 8px;border:1px solid var(--barline,var(--line));border-radius:var(--r,0)}
.fam:hover,.fam[aria-expanded=true]{color:var(--barfg,var(--fg))}
.fam svg{width:10px;height:10px}
#say{margin:0;font:var(--dispw,400) 24px/1.15 var(--display);letter-spacing:var(--displs,0);color:var(--title,var(--barfg,var(--fg)));white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0;flex:1}
#say b{font-weight:inherit;color:var(--sayacc,var(--acc))}
#say .lead{opacity:1}
#q{width:280px;flex:none;height:34px;border:1px solid var(--barline,var(--line));background:var(--field,transparent);color:var(--barfg,var(--fg));font:13.5px var(--text);padding:0 var(--s3) 0 30px;border-radius:var(--r,0);outline:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' fill='none' stroke='%23888' stroke-width='2'%3E%3Ccircle cx='6' cy='6' r='4.5'/%3E%3Cpath d='m9.5 9.5 3.5 3.5'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:10px 50%}
#q:focus{border-color:var(--acc)}#q::placeholder{color:var(--bardim,var(--dim))}
#idxb{display:none}.nclose{display:none}
.menu{position:absolute;top:calc(var(--top) - 6px);left:var(--s4);z-index:40;background:var(--panel,var(--bg));color:var(--fg);border:1px solid var(--line);box-shadow:0 10px 30px rgba(0,0,0,.18);padding:var(--s2) 0;min-width:340px;display:none}
.menu.on{display:block}
.menu .mt{padding:var(--s1) var(--s4) var(--s2);font:600 12px var(--text);color:var(--dim)}
.menu a{display:grid;grid-template-columns:1fr auto;gap:var(--s3);padding:6px var(--s4);text-decoration:none;font-size:14px}
.menu a:hover{background:var(--hov)}.menu a[aria-current=true]{box-shadow:inset 3px 0 0 var(--acc);font-weight:600}
.menu a span:last-child{color:var(--dim);font-size:12.5px}
/* index */
nav{overflow-y:auto;border-right:1px solid var(--line);padding:var(--s2) 0 var(--s8);scrollbar-width:thin;background:var(--navbg,transparent)}
.home-it{display:flex;gap:var(--s2);width:100%;padding:6px var(--s4);font-weight:600;font-size:14px}
.home-it:hover{background:var(--hov)}.home-it[aria-current=true]{background:var(--sel);box-shadow:inset 3px 0 0 var(--acc)}
.g{border-top:1px solid var(--line2,var(--line))}
.gh{display:flex;gap:var(--s2);align-items:baseline;width:100%;padding:8px var(--s4);font:600 13px/1.3 var(--label);color:var(--gfg,var(--fg))}
.gh .ic{width:16px;flex:none;text-align:center;color:var(--acc)}
.gh .m{margin-left:auto}
.gh .cv{width:10px;flex:none;color:var(--dim);font-size:10px;transition:transform .15s}
.g.open .gh .cv{transform:rotate(90deg)}
.gb{display:none;padding-bottom:var(--s2)}.g.open .gb{display:block}
.it{display:flex;gap:var(--s2);align-items:baseline;width:100%;padding:3px var(--s4) 3px 40px;font-size:14px;line-height:1.35}
.it .ic{width:16px;margin-left:-24px;flex:none;text-align:center;color:var(--dim);font-size:12.5px}
.it .nm{min-width:0}
.it .m{margin-left:auto;padding-left:var(--s2)}
.it:hover,.gh:hover{background:var(--hov)}
.it[aria-current=true]{background:var(--sel);color:var(--selfg,var(--fg));box-shadow:inset 3px 0 0 var(--acc)}
/* middle */
main{overflow-y:auto;min-width:0;scrollbar-width:thin}
.mh{padding:var(--s4) var(--s6) var(--s3);border-bottom:1px solid var(--line)}
.crumb{display:flex;gap:var(--s2);flex-wrap:wrap;align-items:baseline}
.crumb .c{font:600 12.5px var(--label);color:var(--dim)}
.mh .lead{margin:var(--s2) 0 0;max-width:72ch;color:var(--fg2,var(--fg));font-size:14px}
.cols{position:sticky;top:0;z-index:3;background:var(--bg);border-bottom:1px solid var(--line);padding:var(--s2) var(--s6)}
.sub{position:sticky;top:var(--subtop,0);z-index:2;background:var(--bg);padding:var(--s3) var(--s6) 6px;font:600 13.5px var(--label);border-bottom:1px solid var(--line)}
.row{display:block;width:100%;padding:10px var(--s6);border-bottom:1px solid var(--line2,var(--line));position:relative}
.row.pick{cursor:pointer}.row.pick:hover{background:var(--hov)}
.row[aria-selected=true]{background:var(--sel);box-shadow:inset 3px 0 0 var(--acc)}
.row .p1{display:block;font-size:15px;line-height:1.35}
.row .p2{display:block;color:var(--fg2,var(--dim));font-size:13.5px;line-height:1.45;margin-top:2px}
.row .meta{display:flex;gap:var(--s2);flex-wrap:wrap;align-items:baseline;margin-top:6px}
.none{padding:var(--s6);color:var(--dim)}
.more-res{padding:var(--s3) var(--s6)}
.t{display:inline-block;font:600 11.5px/1 var(--label);padding:4px 6px 3px;border:1px solid currentColor;border-radius:var(--r,0);white-space:nowrap}
.t.f{border-color:transparent;background:var(--c,var(--fg));color:var(--onc,#fff)}
/* home */
.hw{padding:var(--s6) var(--s6) 80px;max-width:1180px}
.hw .intro{font-size:16px;line-height:1.55;max-width:66ch;margin:0 0 var(--s4)}
.hw .how{display:flex;gap:var(--s4);flex-wrap:wrap;color:var(--dim);font-size:13px;margin:0 0 var(--s6)}
.hw .how b{font-weight:600;color:var(--fg)}
.hw h3{font:600 13px var(--label);color:var(--dim);margin:var(--s6) 0 var(--s2);padding-bottom:6px;border-bottom:1px solid var(--line)}
.hg{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:var(--s4) var(--s6)}
.hg .hgr h4{margin:0 0 4px;font:600 15px var(--label);display:flex;gap:var(--s2);align-items:baseline}
.hg .hgr h4 .ic{color:var(--acc)}.hg .hgr h4 .m{margin-left:auto}
.hg .hgr button{display:block;font-size:13.5px;line-height:1.5;color:var(--fg2,var(--fg))}.hg .hgr button:hover{color:var(--acc);text-decoration:underline}
.feat{display:grid;gap:0}
.fr{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:var(--s4);padding:8px 0;border-bottom:1px solid var(--line2,var(--line));text-align:left;width:100%}
.fr:hover{background:var(--hov)}
.fr .src{color:var(--dim);font-size:12.5px}
/* detail */
aside{overflow-y:auto;border-left:1px solid var(--line);background:var(--panel,var(--bg));scrollbar-width:thin}
.d{padding:var(--s4) var(--s6) 80px;max-width:68ch}
.d h3{margin:var(--s2) 0 var(--s3);font:600 19px/1.3 var(--text)}
.d .lab{display:flex;align-items:center;gap:var(--s2);margin:var(--s4) 0 6px;font:600 12.5px var(--label);color:var(--dim)}
.d .lab::after{content:"";flex:1;border-top:1px solid var(--line)}
.d p{margin:0 0 var(--s2)}
.d .src{font-size:13px;color:var(--dim)}
.empty{padding:var(--s6);color:var(--dim);font-size:13.5px}
.cp{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;vertical-align:-5px;margin-left:var(--s1);opacity:0;color:var(--dim);border-radius:3px}
.cp svg{width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
:hover>.cp,:hover>*>.cp,[aria-selected=true] .cp,.d .cp{opacity:.7}.cp:hover,.cp:focus-visible{opacity:1!important;color:var(--fg)}.cp.ok{opacity:1;color:var(--acc)}.cp.ok svg{display:none}.cp.ok::after{content:"✓";font-size:13px}
@media (hover:none){.cp{opacity:.5}}
.kh{font:11px var(--mono);color:var(--dim)}.kh kbd{font:inherit;border:1px solid var(--line);padding:0 4px;border-radius:3px}
.credit{position:fixed;right:var(--s3);bottom:var(--s3);z-index:20;display:flex;align-items:center;gap:6px;font:12px var(--text);color:var(--dim);background:var(--panel,var(--bg));padding:3px 9px 3px 3px;border:1px solid var(--line);border-radius:999px}
.credit img{width:18px;height:18px;border-radius:50%;object-fit:cover}.credit b{font-weight:600;color:var(--fg)}
.back{display:none}
:focus-visible{outline:2px solid var(--acc);outline-offset:-2px}
@media (max-width:1180px){:root{--right:360px;--left:230px}#q{width:200px}}
@media (max-width:860px){
 :root{--top:auto}
 body,body.home,body.nopanel{display:block;overflow:auto;height:auto}
 header{position:sticky;top:0;flex-wrap:wrap;padding:var(--s2) var(--s4);gap:var(--s2)}
 #say{order:2;flex-basis:100%;white-space:normal;font-size:19px!important;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
 .nclose{display:block;width:100%;padding:var(--s3) var(--s4);font:600 13px var(--text);color:var(--dim);border-bottom:1px solid var(--line);margin-top:calc(-1*var(--s4))}
 #q{order:3;flex:1;width:auto}
 #idxb{display:block;order:1;margin-left:auto;font:600 12px var(--text);padding:6px 10px;border:1px solid var(--barline,var(--line));color:var(--barfg,var(--fg))}
 nav{position:fixed;inset:0;z-index:35;background:var(--bg);transform:translateX(-100%);transition:transform .2s;padding-top:var(--s4)}
 body.idx nav{transform:none}
 .mh,.row,.sub,.cols,.hw{padding-left:var(--s4);padding-right:var(--s4)}
 aside{position:fixed;inset:0;z-index:30;transform:translateX(100%);transition:transform .2s;border:0}
 body.det aside{transform:none;display:block}
 .back{display:block;width:100%;padding:var(--s3) var(--s4);border-bottom:1px solid var(--line);font:600 13px var(--text);color:var(--dim);position:sticky;top:0;background:var(--panel,var(--bg))}
 .d{padding:var(--s4) var(--s4) 80px}
 .menu{left:var(--s2);right:var(--s2);min-width:0}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}

/* ---- minimalism brush ---- */
.fam{border:0;padding:6px 4px;font-size:0;gap:0}.fam::before{content:"";width:16px;height:12px;background:linear-gradient(currentColor 0 0) 0 0/100% 1.5px no-repeat,linear-gradient(currentColor 0 0) 0 50%/100% 1.5px no-repeat,linear-gradient(currentColor 0 0) 0 100%/100% 1.5px no-repeat}.fam svg{display:none}
#q{border-width:0 0 1px;background-color:transparent!important;border-radius:0;width:220px}
#q:focus{width:300px}
.it .m,.gh .m{opacity:0;transition:opacity .15s}.it:hover .m,.it[aria-current=true] .m,.gh:hover .m,nav:focus-within .m{opacity:1}
.d .lab::after{display:none}.d .lab{margin-top:20px}
.credit{display:none}
.vtabs{display:flex;gap:18px;flex:none;font-size:15px}.vtabs a{color:var(--bardim,var(--dim));text-decoration:none;padding:4px 0;border-bottom:1.5px solid transparent}.vtabs a:hover{color:var(--barfg,var(--fg))}.vtabs a[aria-current]{color:var(--barfg,var(--fg));border-color:var(--acc)}
@media (max-width:860px){.vtabs{order:4;flex-basis:100%}}
.navlink{display:block;padding:6px 16px;font-size:13px;color:var(--dim);text-decoration:none}.navlink:first-of-type{margin-top:16px;border-top:1px solid var(--line2,var(--line));padding-top:14px}.navlink:hover{color:var(--acc)}
.navfoot{padding:24px 16px 8px;font-size:12px;color:var(--dim);display:flex;align-items:center;gap:6px}.navfoot img{width:16px;height:16px;border-radius:50%}
.hw .intro{font-size:17px;max-width:58ch;margin-bottom:24px}
.mh{border-bottom:0;padding-bottom:4px}
.sub{border-bottom:0;padding-top:20px}
.row{border-bottom-color:transparent;border-top:1px solid var(--line2,var(--line))}
.sub+.row{border-top-color:transparent}
.tip{position:absolute;z-index:5;left:var(--s6);top:100%;margin-top:-4px;background:var(--panel,var(--bg));border:1px solid var(--line);padding:6px 10px;font-size:13px;box-shadow:0 6px 18px rgba(0,0,0,.12);display:none;white-space:nowrap}
.row:hover .tip{display:block}
.row:not([aria-selected=true]) .onsel{display:none!important}
'''

ENGINE = r'''
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const fold=s=>String(s||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[’‘]/g,"'").replace(/[“”]/g,'"');
function hl(t,q){const s=String(t??'');if(!q)return esc(s);const f=fold(s),i=f.indexOf(q);if(i<0)return esc(s);return esc(s.slice(0,i))+'<mark>'+esc(s.slice(i,i+q.length))+'</mark>'+esc(s.slice(i+q.length))}
const CPI='<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="2.5"/><path d="M5 15H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1"/></svg>';
const cpb=t=>`<span class="cp" role="button" tabindex="0" data-c="${esc(t)}" title="Copy (c)" aria-label="Copy">${CPI}</span>`;
const lab=t=>`<div class="lab">${t}</div>`;
const S=SITE,PANEL=S.PANEL!==false;const NAVFOOT=(S.LINKS||[]).map(l=>`<a class="navlink" href="${l[1]}">${esc(l[0])}</a>`).join('')+`<div class="navfoot"><img alt="" src="${document.querySelector('.credit img').src}">made by Jere</div>`;if(!PANEL)document.body.classList.add('nopanel');
const ITEMS={};S.tree.forEach((g,gi)=>{g.gi=gi;g.items.forEach(it=>{it.g=g;ITEMS[it.id]=it})});
S.units.forEach((u,i)=>{u.ix=i;u._f=fold(u.blob||S.BLOB(u));delete u.blob});
const BY={};S.units.forEach(u=>(u.its||[u.it]).forEach(id=>(BY[id]=BY[id]||[]).push(u)));
const CNT=u=>S.COUNT?S.COUNT(u):true;
let cur=null,sel=null,Q='',vis=[];const OPEN=new Set();
function count(it){return (BY[it.id]||[]).filter(u=>CNT(u)&&(!Q||u._f.includes(Q))).length}
function say(){$('#say').innerHTML=S.SAY(Q?null:cur,Q?null:sel,Q?$('#q').value.trim():'');document.title=$('#say').textContent}
function tree(){const home=`<button class="nclose" onclick="document.body.classList.remove('idx')">✕ Close index</button><button class="home-it" data-home aria-current="${!cur&&!Q}">Overview</button>`;
 $('nav').innerHTML=home+S.tree.map(g=>{const n=g.items.reduce((a,it)=>a+count(it),0);if(Q&&!n)return'';
 const open=Q||OPEN.has(g.gi);
 return `<div class="g${open?' open':''}"><button class="gh" data-g="${g.gi}" aria-expanded="${!!open}"><span class="cv">▶</span>${g.i?`<span class="ic">${esc(g.i)}</span>`:''}<span>${esc(g.n)}</span><span class="m">${n}</span></button><div class="gb">${g.items.map(it=>{const c=count(it);if(Q&&!c)return'';return `<button class="it" data-id="${it.id}" aria-current="${!Q&&cur===it}"><span class="ic"${it.c?` style="color:${it.c}"`:''}>${esc(it.i||'')}</span><span class="nm">${hl(it.n,Q)}</span><span class="m">${c}</span></button>`}).join('')}</div></div>`}).join('')+NAVFOOT}
function middle(){const m=$('main');let html='';document.body.classList.toggle('home',!cur&&!Q);
 if(Q){vis=S.units.filter(u=>u._f.includes(Q));const shown=vis.slice(0,400);
  html=`<div class="mh"><span class="m">${vis.length} ${vis.length===1?S.noun[0]:S.noun[1]}</span></div>`+(S.COLS?S.COLS(null):'')+rows(shown,true)+(vis.length>400?`<div class="more-res m">Showing 400. Narrow the search.</div>`:'')}
 else if(!cur){vis=[];html=home()}
 else{vis=BY[cur.id]||[];html=(S.HEAD?`<div class="mh">${S.HEAD(cur)}</div>`:'')+(S.COLS?S.COLS(cur):'')+rows(vis,false)}
 m.innerHTML=html;m.scrollTop=0;const c=m.querySelector('.cols');if(c)m.style.setProperty('--subtop',c.offsetHeight+'px')}
function home(){return `<div class="hw"><p class="intro">${S.INTRO}</p>${S.FEATURE?S.FEATURE():''}
 ${S.GRID?`<h3>Everything, by ${esc(S.by||'section')}</h3>`:''}<div class="hg">${!S.GRID?'':S.tree.filter(g=>!g.nohome).map(g=>`<div class="hgr"><h4>${g.i?`<span class="ic">${esc(g.i)}</span>`:''}<span>${esc(g.n)}</span><span class="m">${g.items.reduce((a,it)=>a+count(it),0)}</span></h4>${g.items.map(it=>`<button data-id="${it.id}">${esc(it.n)}</button>`).join('')}</div>`).join('')||''}</div></div>`}
function rows(list,search){let last=null,out='';const pick=PANEL||S.PICK?' pick':'';
 list.forEach(u=>{const gk=search?(ITEMS[u.it].n+(u.g?' · '+u.g:'')):(S.GROUP?S.GROUP(u,cur):u.g);
 if(gk&&gk!==last){out+=`<div class="sub">${esc(gk)}</div>`;last=gk}
 out+=`<div class="row${pick}" data-u="${u.ix}" aria-selected="${sel===u}">${S.ROW(u,Q)}</div>`});
 return out||'<div class="none">Nothing here.</div>'}
function detail(){if(!PANEL)return;const a=$('aside');if(!sel){a.innerHTML=`<div class="empty">${S.EMPTY||'Pick a row to see it in full.'}</div>`;return}
 a.innerHTML=`<button class="back" onclick="document.body.classList.remove('det')">← Back</button><div class="d">${S.DETAIL(sel,Q)}</div>`;a.scrollTop=0}
function hash(){try{history.replaceState(null,'',cur?'#'+cur.id+(sel?'~'+sel.ix:''):location.pathname)}catch(e){}}
function pickItem(it){cur=it;sel=null;Q='';$('#q').value='';if(it)OPEN.add(it.g.gi);document.body.classList.remove('idx');tree();middle();if(it&&PANEL&&vis[0])sel=vis[0];markSel();detail();say();hash();
 const c=document.querySelector('.it[aria-current=true]');if(c)c.scrollIntoView({block:'nearest'})}
function markSel(){document.querySelectorAll('.row').forEach(r=>r.setAttribute('aria-selected',S.units[+r.dataset.u]===sel))}
function pickRow(u,scroll,open){sel=u;markSel();detail();say();hash();if(open&&PANEL&&innerWidth<=860)document.body.classList.add('det');
 if(scroll){const r=document.querySelector(`.row[data-u="${u.ix}"]`);if(r)r.scrollIntoView({block:'nearest'})}}
function copyText(t,el){const ok=()=>{if(el){el.classList.add('ok');setTimeout(()=>el.classList.remove('ok'),1100)}};try{navigator.clipboard.writeText(t).then(ok,()=>{fb(t);ok()})}catch(_){fb(t);ok()}}
function fb(t){const a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();try{document.execCommand('copy')}catch(e){}a.remove()}
document.addEventListener('click',e=>{
 const c=e.target.closest('.cp');if(c){e.stopPropagation();copyText(c.dataset.c,c);return}
 if(e.target.closest('.fam')){const mn=$('.menu');const on=!mn.classList.contains('on');mn.classList.toggle('on',on);$('.fam').setAttribute('aria-expanded',on);return}
 if(!e.target.closest('.menu'))$('.menu').classList.remove('on'),$('.fam').setAttribute('aria-expanded',false);
 if(e.target.closest('#idxb')){document.body.classList.toggle('idx');return}
 if(e.target.closest('[data-home]')){pickItem(null);return}
 const gh=e.target.closest('.gh');if(gh){const gi=+gh.dataset.g;OPEN.has(gi)?OPEN.delete(gi):OPEN.add(gi);tree();return}
 const it=e.target.closest('[data-id]');if(it){pickItem(ITEMS[it.dataset.id]);return}
 const j=e.target.closest('[data-jump]');if(j){const u=S.units[+j.dataset.jump];pickItem(ITEMS[u.it]);pickRow(u,true,true);return}
 const r=e.target.closest('.row.pick');if(r&&!e.target.closest('a,summary,details')){pickRow(S.units[+r.dataset.u],false,true)}});
let tm;$('#q').addEventListener('input',e=>{clearTimeout(tm);tm=setTimeout(()=>{Q=fold(e.target.value.trim());tree();middle();
 if(Q){if(PANEL&&vis[0]&&!vis.includes(sel)){sel=vis[0]}document.body.classList.toggle('home',false)}markSel();detail();say()},90)});
document.addEventListener('keydown',e=>{const q=$('#q');const inQ=document.activeElement===q;
 if(e.key==='/'&&!inQ){e.preventDefault();q.focus();q.select();return}
 if(e.key==='Escape'){$('.menu').classList.remove('on');document.body.classList.remove('idx','det');if(q.value){q.value='';q.dispatchEvent(new Event('input'))}q.blur();return}
 if(e.key==='c'&&!inQ&&sel&&!e.metaKey&&!e.ctrlKey){const r=document.querySelector(`.row[data-u="${sel.ix}"] .cp`);copyText(S.COPY?S.COPY(sel):r?r.dataset.c:'',r);return}
 if(['ArrowDown','ArrowUp','j','k'].includes(e.key)&&(!inQ||e.key.startsWith('Arrow'))){const list=Q?vis.slice(0,400):vis;if(!list.length)return;e.preventDefault();
  let i=list.indexOf(sel);i=(e.key==='ArrowDown'||e.key==='j')?Math.min(list.length-1,i+1):Math.max(0,i-1);pickRow(list[i],true,false)}});
if(S.TABS){const n=document.createElement('div');n.className='vtabs';n.setAttribute('aria-label','Views');n.innerHTML=S.TABS.map((t,i)=>`<a href="${t[1]}"${i===0?' aria-current="page"':''}>${esc(t[0])}</a>`).join('');$('#say').after(n)}
(function(){const h=decodeURIComponent(location.hash.slice(1)).split('~');const it=ITEMS[h[0]]||null;cur=it;if(it)OPEN.add(it.g.gi);tree();middle();
 const u=h[1]!=null?S.units[+h[1]]:null;if(u&&it&&(u.its||[u.it]).includes(it.id))sel=u;else if(it&&PANEL&&vis[0])sel=vis[0];markSel();detail();say();
 const c=document.querySelector('.it[aria-current=true]');if(c)c.scrollIntoView({block:'center'});if(sel){const r=document.querySelector(`.row[data-u="${sel.ix}"]`);if(r)r.scrollIntoView({block:'center'})}})();
'''

def page4(name, title, fonts, theme_css, site, site_js, extra_css=''):
    fonts_url = f'https://fonts.googleapis.com/css2?{fonts}&family=IBM+Plex+Mono:wght@400;500&display=swap'
    base = os.environ.get('FAMBASE')
    menu = ''.join(f'<a href="{(base+fid+"/"+os.environ.get("FAMQ","")) if base else fid+".html"}" aria-current="{str(fid==name).lower()}"><span>{fn}</span><span>{fnote}</span></a>' for fid, fn, fnote in FAMILY)
    caret = '<svg viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.6"><path d="m2 3.5 3 3 3-3"/></svg>'
    h = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="{fonts_url}">
<style>{BASE_CSS}{theme_css}{extra_css}</style></head><body>
<header><button class="fam" aria-expanded="false" aria-haspopup="true" aria-label="Sites for arguing" title="Sites for arguing">Sites for arguing {caret}</button><h1 id="say">{title}</h1><button id="idxb">Index</button><input id="q" placeholder="Search" title="/ search · ↑ ↓ move · c copy · esc clear" autocomplete="off" spellcheck="false" aria-label="Search"></header>
<div class="menu" role="menu"><div class="mt">Sites for arguing, by Jere</div>{menu}</div>
<nav aria-label="Index"></nav><main></main><aside aria-label="Details"></aside>
<div class="credit"><img alt="" src="{JERE}">made by <b>Jere</b></div>
<script id="data" type="application/json">{json.dumps(site, ensure_ascii=False).replace("</", "<\\/")}</script>
<script>const SITE=JSON.parse(document.getElementById('data').textContent);
{site_js}
{ENGINE}</script></body></html>'''
    path = os.environ.get('OUTFILE') or f'{OUT}/{name}.html'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(h)
    print('wrote', name, len(h))
