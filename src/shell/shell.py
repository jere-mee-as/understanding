"""The "So you're sure about…" shell, shared. build(...) writes one self-contained page.
P = [{n, i?, u:[{n, i?, t:[topic indices]}], t:[{t, p?, k:[{q?, f, m?, ml?, c?}]}]}]
i: a sigil character, or '@key' for a picture in pfps. q: dim line above an item. m: text that unfolds under it (labelled ml). c: what the copy mark copies (default f)."""
import json, os
H = os.path.dirname(os.path.abspath(__file__))
def r(f): return open(os.path.join(H, f), encoding='utf-8').read()
def js(x): return json.dumps(x, ensure_ascii=False).replace('</', '<\\/')
def build(P, out, *, title, lead, key, words, steps, plurals=None, pfps=None, foot='', theme='ink', end='?', sub='', more='Need more?', morenote=''):
    cfg = {'w': words, 'steps': steps, 'pl': plurals or {}}
    s = r('template.html').replace('@@SENTCSS@@', r('sentence.css')).replace('@@SENTJS@@', r('sent.js')).replace('@@TREEJS@@', r('tree.js'))
    s = s.replace('@@TITLE@@', title).replace('@@LEAD@@', lead).replace('@@KEY@@', key).replace('@@DEFTHEME@@', theme).replace('@@FOOT@@', foot).replace('@@END@@', end).replace('@@SUB@@', sub).replace('@@MORE@@', more).replace('@@MORENOTE@@', morenote)
    s = s.replace('@@JERE@@', r('jere.txt').strip()).replace('@@CFG@@', js(cfg)).replace('@@PFPS@@', js(pfps or {})).replace('@@DATA@@', js(P))
    assert '@@' not in s, s[s.index('@@'):s.index('@@') + 30]
    open(out, 'w', encoding='utf-8').write(s); return len(s)
