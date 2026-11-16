/* =================== SENTENCE: the heading writes itself; each choice flies up into it =================== */
function makeSent(cfg){
  let path = [], busy = false; const S = $(cfg.sec), H = $(cfg.h), B = $(cfg.b), STEPS = $(cfg.st);
  const words = p => { const w = []; if(p.length > 0) w.push(P[p[0]].n); if(p.length > 1) w.push(P[p[0]].u[p[1]].n); if(p.length > 2) w.push(P[p[0]].t[p[2]].t); return w; };
  /* while searching, the heading says so ("Searching for “islam” in Religion, …") and offers a way back */
  function head(hideLast){ H.innerHTML = ''; const w = words(path), raw = $('find').value.trim(), searching = !!QRY;
    if(searching){ H.append('Searching for “' + raw + '”'); if(w.length) H.append(' in'); }
    else { H.append('@@LEAD@@'); if(!w.length){ H.append('…'); return null; } }
    let last = null; w.forEach((txt, i) => { H.append(' '); const b = el('button', 'w', txt); b.onclick = () => back(i); H.appendChild(b); H.append(i === w.length - 1 ? (searching ? '' : '@@END@@') : ','); last = b; });
    if(searching){ const g = el('button', 'goback', '← go back'); g.onclick = () => { SND.tick(.8); setQ(''); }; H.append(g); }
    if(hideLast && last) last.style.opacity = 0; return last; }
  /* which layer you're choosing in: steps over the heading; the ones you've passed lead back */
  function steps(){ const st = STEPS; st.innerHTML = ''; CFG.steps.forEach((n, i) => { if(i) st.append(el('i', null, '›'));
      if(i < path.length){ const b = el('button', 'done', n); b.title = 'Back to choosing a ' + n; b.onclick = () => back(i); st.append(b); }
      else st.append(el('span', i === path.length ? 'on' : '', n)); }); if(S.classList.contains('on')) ph('search…'); }
  const mark = (txt) => { const f = document.createDocumentFragment(); const i = QRY ? nrm(txt).indexOf(QRY) : -1;
    if(i < 0){ f.append(txt); return f; } f.append(txt.slice(0, i), el('mark', null, txt.slice(i, i + QRY.length)), txt.slice(i + QRY.length)); return f; };
  /* under each choice, the topics inside it that your search reaches */
  /* the list of what matched sits in a small card that appears when you hover the choice */
  function where(si, tis){ const d = el('span', 'hits'); tis.forEach(ti => { const r = el('span', 'hl'); r.append(mark(P[si].t[ti].t)); d.append(r); }); return d; }
  function body(){ B.innerHTML = ''; steps(); const list = el('div', 'choices'); let rows = [];
    const q = QRY && totalHits() ? QRY : '';
    if(path.length === 0) rows = P.map((s,i) => ({t: s.n, c: plural(s.u.length, W[1]), p: [i], h: q ? sHits(i) : null, si: i, ic: ico(0, i)}));
    else if(path.length === 1) rows = P[path[0]].u.map((u,i) => ({t: u.n, c: plural(u.t.length, W[2]), p: [path[0], i], h: q ? gHits(path[0], i) : null, si: path[0], ic: ico(1, path[0], i)}));
    else if(path.length === 2) rows = P[path[0]].u[path[1]].t.map(ti => ({t: P[path[0]].t[ti].t, c: plural(cnt(P[path[0]].t[ti]), W[3]), p: [path[0], path[1], ti], h: q ? (tHit(path[0], ti) ? [ti] : []) : null, si: path[0], ti}));
    else return facts();
    const total = rows.length;
    /* searching culls every layer to the places that mention it */
    if(q) rows = rows.filter(r => r.h && r.h.length); else if(QRY) rows = [];
    B.appendChild(el('div', 'lay', q ? rows.length + ' of ' + plural(total, LAYER[path.length]) + (rows.length === 1 ? ' mentions “' : ' mention “') + $('find').value.trim() + '”' : QRY ? 'nothing mentions “' + $('find').value.trim() + '”' : plural(total, LAYER[path.length]) + (path.length ? ' in ' + words(path).slice(-1)[0] : '')));
    rows.forEach((r, n) => { const x = el('button', 'ch'); x.style.setProperty('--n', n); if(r.ic){ x.append(r.ic); x.classList.add('hasic'); } const t = el('span', 't'); t.append(mark(r.t)); x.append(t);
      if(q && r.h && r.h.length && path.length < 2) x.append(el('span', 'c more-c', plural(r.h.length, W[2]) + (r.h.length === 1 ? ' mentions it' : ' mention it')), where(r.si, r.h));
      else if(q && path.length === 2){ const ks = P[r.si].t[r.ti].k.filter(fHit), k = ks.length; x.append(el('span', 'c' + (k ? ' more-c' : ''), k ? plural(k, W[3]) + (k === 1 ? ' mentions it' : ' mention it') : 'its title mentions it'));
        if(k){ const d = el('span', 'hits'); ks.forEach(f => { const r = el('span', 'hl'); r.append(mark(f.f)); d.append(r); }); x.append(d); } }
      else x.append(el('span', 'c', r.c));
      x.onclick = () => choose(x, r.p); list.appendChild(x); if(!reduced && !QRY && n < 18) setTimeout(() => SND.tick(.9 + n*.025), 60 + n*30); });
    B.appendChild(list); }
  function facts(){ const t = P[path[0]].t[path[2]], q = QRY && totalHits() ? QRY : '', ks = shownFacts(t), only = q && ks.length < t.k.length;
    const f = el('div', 'facts'), word = $('find').value.trim();
    B.appendChild(el('div', 'lay', only ? ks.length + ' of ' + plural(t.k.length, W[3]) + (ks.length === 1 ? ' mentions “' : ' mention “') + word + '”' : q && !t.k.some(fHit) ? 'its title mentions “' + word + '”; none of its facts do' : plural(cnt(t), W[3])));
    ks.forEach((k, n) => { const x = factEl(k, n); x.style.setProperty('--d', '0s'); if(q) markIn(x); f.appendChild(x); });
    const ld = leadEl(t); if(ld) B.appendChild(ld); B.appendChild(f); if(!reduced && !QRY) ks.forEach((k,i) => setTimeout(() => SND.tick(1.05 + i*.05), 110 + i*90)); }
  function markIn(x){ x.querySelectorAll('.say .tx,.q').forEach(s => { if(s.closest('.more')) return; const txt = s.textContent; s.textContent = ''; s.append(mark(txt)); }); }
  function filter(q){ QRY = q; head(false); body(); if(!reduced && q) SND.tick(1.6); fhint(''); }
  function enter(){ const first = B.querySelector('.ch'); if(first) first.click(); }
  function choose(x, p){ if(busy) return; busy = true; SND.tick(1.4);
    const src = x.querySelector('.t'), rc = src.getBoundingClientRect(), fs = parseFloat(getComputedStyle(src).fontSize);
    /* everything else drops away, rippling out from the one you picked */
    const all = [...B.querySelectorAll('.ch,.lay')], me = all.indexOf(x);
    all.forEach((o, i) => { if(o === x) return; o.animate([{opacity: getComputedStyle(o).opacity, transform: 'none'}, {opacity: 0, transform: 'translateY(10px)'}], {duration: 240, delay: Math.min(170, Math.abs(i - me)*11), easing: 'ease-in', fill: 'forwards'}); });
    x.querySelectorAll('.c,.hits,.ic').forEach(e => e.style.opacity = 0);
    const fly = el('div', 'fly', src.textContent); Object.assign(fly.style, {left: rc.left + 'px', top: rc.top + 'px', fontSize: fs + 'px'}); document.body.appendChild(fly); src.style.visibility = 'hidden';
    S.scrollTo({top: 0, behavior: reduced ? 'auto' : 'smooth'});
    setTimeout(() => { path = p; const tw = head(true), tr = tw.getBoundingClientRect(), tfs = parseFloat(getComputedStyle(tw).fontSize), now = fly.getBoundingClientRect();
      const k = tfs / fs, dx = tr.left - now.left, dy = tr.top - now.top;
      const a = fly.animate([{transform: 'none'}, {transform: `translate(${dx*.55}px,${dy*.55 - 26}px) scale(${1 + (k - 1)*.6})`, offset: .55}, {transform: `translate(${dx}px,${dy}px) scale(${k})`}],
        {duration: reduced ? 1 : 520, easing: 'cubic-bezier(.5,0,.2,1)', fill: 'forwards'});
      a.onfinish = () => { tw.style.opacity = ''; tw.classList.add('land'); fly.remove(); SND.tick(.75); body(); busy = false; }; }, reduced ? 0 : 190); }
  function back(i){ if(busy) return; SND.tick(.8); path = path.slice(0, i); head(false); body(); S.scrollTop = 0; }
  addEventListener('keydown', e => { if(S.classList.contains('on') && e.key === 'Escape' && e.target.tagName !== 'INPUT' && path.length) back(path.length - 1); });
  /* branch mode: fine stems run from the last word of the heading down a trunk, along a rail, and down each column's gutter to its choices, so no line ever crosses a word */
  const NSs = 'http://www.w3.org/2000/svg';
  function stems(anim){ if(!cfg.branch) return; const wrap = S.querySelector('.wrap'); let svg = wrap.querySelector('svg.stems');
    if(!svg){ svg = document.createElementNS(NSs, 'svg'); svg.setAttribute('class', 'stems'); wrap.prepend(svg); } svg.innerHTML = '';
    const items = [...B.querySelectorAll('.choices > .ch, .facts > .fact')]; if(!items.length) return;
    const W = wrap.getBoundingClientRect(), rel = r => ({l: r.left - W.left, r: r.right - W.left, t: r.top - W.top, b: r.bottom - W.top});
    const ws = H.querySelectorAll('.w'), an = ws.length ? rel(ws[ws.length - 1].getBoundingClientRect()) : (() => { const rg = document.createRange(); rg.selectNodeContents(H); const r = rel(rg.getBoundingClientRect()); return {l: r.r - 24, r: r.r - 24, t: r.t, b: r.b}; })();
    const ax = Math.min(an.l + 14, (an.l + an.r)/2), ay = an.b + 4;
    const cols = new Map(); items.forEach(it => { const r = rel(it.getBoundingClientRect()), tr = rel((it.querySelector('.t') || it.querySelector('.q') || it).getBoundingClientRect()), x = Math.round(r.l); if(!cols.has(x)) cols.set(x, []); cols.get(x).push({t: tr.t, b: tr.t + Math.min(tr.b - tr.t, 30)}); });
    const firstTop = Math.min(...items.map(it => rel(it.getBoundingClientRect()).t)), rail = firstTop - 16, R = 7;
    const xs = [...cols.keys()].map(x => x - 12), lo = Math.min(ax, ...xs), hi = Math.max(ax, ...xs);
    let d = `M${ax} ${ay} V${rail - R}`;
    const add = (p, w) => { const e = document.createElementNS(NSs, 'path'); e.setAttribute('d', p); e.style.strokeWidth = w; svg.appendChild(e); return e; };
    const paths = [add(d + ` V${rail}`, 1.2)];
    if(hi > lo) paths.push(add(`M${lo} ${rail} H${hi}`, 1));
    cols.forEach((rs, x) => { const gx = x - 12, last = Math.max(...rs.map(r => (r.t + Math.min(r.b, r.t + 30))/2));
      let p = `M${gx} ${rail} V${last - R}`; paths.push(add(p + ` Q${gx} ${last} ${gx + R} ${last} H${x - 3}`, .9));
      rs.forEach(r => { const y = (r.t + Math.min(r.b, r.t + 30))/2; paths.push(add(`M${gx} ${y - R} Q${gx} ${y} ${gx + R} ${y} H${x - 3}`, .8)); }); });
    svg.style.height = wrap.scrollHeight + 'px';
    if(anim && !reduced) paths.forEach((p, i) => { const L = p.getTotalLength(); p.style.strokeDasharray = L + ' ' + (L + 4); p.style.strokeDashoffset = L + 2; p.getBoundingClientRect();
      p.style.transition = `stroke-dashoffset ${Math.min(.5, .15 + L/1400)}s ease-out ${i ? .12 + i*.012 : 0}s`; p.style.strokeDashoffset = 0; }); }
  if(cfg.branch){ const ro = new ResizeObserver(() => { if(S.classList.contains('on')) stems(false); }); ro.observe(S); }
  const _body = body; body = function(){ if(typeof HIST === 'function') HIST(); _body(); if(cfg.branch) requestAnimationFrame(() => stems(true)); };
  return {depth(){ return path.length; }, up(){ if(path.length) back(path.length - 1); }, start(){ path = []; head(false); body(); }, open(p){ path = p.slice(); head(false); body(); S.scrollTop = 0; }, filter, enter, shown(){ steps(); if(cfg.branch) requestAnimationFrame(() => stems(false)); }};
}
const T = makeSent({sec: 'sent', h: 'sh', b: 'sb', st: 'steps'});
