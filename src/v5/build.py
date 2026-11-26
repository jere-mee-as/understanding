import json,sys; import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from shell5 import page4
P=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'understanding.json')))
def vi(q):
    q=q.lower(); return 0 if 'landing' in q else 1 if 'partly' in q else 2 if 'open' in q else 3
tree=[];units=[];LAND={}
for gi,g in enumerate(P):
    G={'n':g['n'],'i':g.get('i',''),'items':[]}
    for ui,u in enumerate(g['u']):
        iid=f'{gi}.{ui}'; G['items'].append({'id':iid,'n':u['n'],'i':u.get('i','')})
        ts=[g['t'][i] for i in u['t']]; land=ts[0]; LAND[iid]=land.get('p','')
        for fi,f in enumerate(ts[1:]):
            a=land['k'][fi] if fi<len(land['k']) else {}
            pos=sorted([{'v':vi(k['q']),'s':1 if 'simple story' in k['q'] else 0,'f':k['f'],'m':k.get('m','')} for k in f['k']],key=lambda p:p['v'])
            units.append({'it':iid,'q':f['t'].rstrip('?')+'?','a':a.get('f',''),'p':f.get('p',''),'pos':pos})
    tree.append(G)
site={'tree':tree,'units':units,'noun':['fight','fights'],'LINKS':[['The ten best papers →','https://jere-mee-as.github.io/tenbestpapers/']],'LAND':LAND,'by':'discipline',
 'INTRO':'Every field’s big fights, and which way the evidence is leaning.'}
theme=r'''
:root{--bg:#22362c;--fg:#efede2;--fg2:#dcdfd3;--dim:#a9bcb0;--line:#3b5246;--line2:#30473b;--acc:#f6e27f;--hov:#2a4035;--sel:#2f4a3c;--hl:rgba(246,226,127,.35);--panel:#1d2f26;--bar:#1d2f26;--field:rgba(0,0,0,.2);
--display:"Cabin Sketch",cursive;--text:"Source Serif 4",Georgia,serif;--label:Kalam,cursive;--dispw:700;--V0:#f6e27f;--V1:#a9d4f5;--V2:#b9c7be;--V3:#f5a9bb;color-scheme:dark}
#say{font-size:26px}
.gh{font-weight:700;font-size:14.5px}.sub,.crumb .c,.d .lab,.hw h3,.hg .hgr h4{font-weight:700;font-size:14px}
.row .p1{font:700 18px/1.25 Kalam,cursive;color:var(--acc)}
.row .p2{font-size:14.5px;color:var(--fg2)}
.vw{display:flex;gap:4px 14px;flex-wrap:wrap;margin-top:6px;font-size:12.5px}
.vw span{color:var(--c)}.vw span::before{content:"● "}.vw span.s{text-decoration:underline;text-decoration-color:#f5a9bb;text-underline-offset:3px}
.d h3{font:700 22px/1.25 Kalam,cursive;color:var(--acc)}
.d .ans{font-size:16px}
.d .ctx{font-size:14px;color:var(--dim)}
.ps{border-top:1px solid var(--line);padding:10px 0}
.ps .f{font-size:15px;margin:4px 0}
.ps .vl{font:700 14px Kalam,cursive;color:var(--c)}
.ps details{font-size:13.5px;color:var(--dim)}.ps summary{cursor:pointer;font:400 13.5px Kalam,cursive;color:#f5a9bb}
.ps details div{white-space:pre-line;margin-top:4px}
.sim{font:400 13px Kalam,cursive;color:#f5a9bb;margin-left:8px}
.lead{color:var(--fg2)!important}.clamp{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;cursor:pointer}.clamp.open{display:block}
.tally{display:flex;gap:20px;flex-wrap:wrap;font-size:14px}.tally b{font:600 20px var(--text);margin-right:6px}
.fr .q{font:700 16px Kalam,cursive;color:var(--acc)}.fr .src{color:var(--dim);font-size:13px;white-space:nowrap}
'''
js=r'''
const VS=['where it’s landing','partly right','still open','losing'],VSS=['landing','partly right','open','losing'];
SITE.BLOB=u=>[u.q,u.a,u.p,...u.pos.map(p=>p.f+' '+p.m)].join(' ');
SITE.SAY=(it,u,q)=>q?`So you want to understand “${esc(q)}”?`:!it?'So you want to understand…':`So you want to understand <b>${esc(it.n)}</b>?`;
const fw=f=>(f.match(/^[^.]*\./)||[f])[0];
SITE.ROW=(u,Q)=>`<span class="p1">${hl(u.q,Q)}</span><span class="p2">${hl(u.a,Q)}</span>`;
SITE.COPY=u=>u.q+' '+u.a;
SITE.HEAD=it=>`<p class="lead clamp" onclick="this.classList.toggle('open')" title="Click to read all">${esc(SITE.LAND[it.id])}</p>`;
SITE.DETAIL=(u,Q)=>`<h3>${hl(u.q,Q)}</h3>${lab('Where it’s landing')}<p class="ans">${hl(u.a,Q)}${cpb(u.q+' '+u.a)}</p>${u.p?`<p class="ctx">${hl(u.p,Q)}</p>`:''}
 ${lab('The positions')}${u.pos.map(p=>`<div class="ps" style="--c:var(--V${p.v})"><span class="vl">${VS[p.v]}</span>${p.s?'<span class="sim">the simple story</span>':''}<p class="f">${hl(p.f,Q)}</p>${p.m?`<details${Q&&fold(p.m).includes(Q)?' open':''}><summary>who, and the best work</summary><div>${hl(p.m,Q)}</div></details>`:''}</div>`).join('')}`;
SITE.FEATURE=()=>{const T=[0,0,0,0];SITE.units.forEach(u=>u.pos.forEach(p=>T[p.v]++));
 const L=SITE.units.filter(u=>u.pos.some(p=>p.s&&p.v===3));
 return `<h3>All ${SITE.units.reduce((a,u)=>a+u.pos.length,0)} positions, by verdict</h3><div class="tally">${VS.map((v,i)=>`<span style="color:var(--V${i})"><b>${T[i]}</b>${v}</span>`).join('')}</div>
 <h3>Where the simple story is losing (${L.length})</h3><div class="feat">${L.slice(0,12).map(u=>`<button class="fr" data-jump="${u.ix}"><span class="q">${esc(u.q)}</span><span class="src">${esc(ITEMS[u.it].n)}</span></button>`).join('')}</div>`};
'''
page4('understanding','So you want to understand…','family=Cabin+Sketch:wght@700&family=Kalam:wght@400;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400',theme,site,js)
