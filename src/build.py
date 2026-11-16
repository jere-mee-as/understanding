"""Builds ../index.html from data/*.json inside the shared shell (src/shell/).  Run: python3 src/build.py
group → discipline → its big fights → the camps. The first topic in each discipline is the lay of the land:
the overview, then one line per fight saying where it's landing."""
import glob, json, os, sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(here, 'shell')); import shell

def tx(c): return ''.join(ch + ('︎' if 0x2190 <= ord(ch) <= 0x2bff else '') for ch in c)   # keep symbols in text form

# same groups, disciplines and sigils as the ten best papers
GROUPS = [
  ('Humanities', '❦', [('History', '⧗'), ('Philosophy', '∴'), ('Religious studies', '✺'), ('Arts & music', '♫'), ('Literature', '¶')]),
  ('Social sciences', '⚖', [('Economics', '¤'), ('Political science', '⚑'), ('Psychology', 'Ψ'), ('Sociology', '⁂'),
                            ('Anthropology', '☥'), ('Linguistics', 'ʃ'), ('Communication', '≋'), ('Education', '✎'), ('Geography', '⊕'), ('Law', '§')]),
  ('Natural sciences', '☉', [('Physics', '⚛'), ('Astronomy', '✶'), ('Chemistry', '⌬'), ('Biology', '❀'),
                             ('Neuroscience', '∿'), ('Earth sciences', '◒')]),
  ('Formal sciences', '∑', [('Mathematics', 'π'), ('Statistics', 'σ'), ('Computer science', 'λ'), ('Systems & information', '⇄')]),
  ('Applied sciences', '⚒', [('Medicine & health', '⚕'), ('Engineering', '⚙'), ('Architecture & planning', '⌂'),
                             ('Environment', '❧'), ('Business', '↗')]),
]
MARK = {'winning': '●  where it’s landing', 'partly right': '◐  partly right', 'losing': '−  losing', 'open': '◌  still open'}

ALIAS = {'environment (conservation biology)': 'Environment', 'medicine & health': 'Medicine & health', 'political science': 'Political science', 'religious studies': 'Religious studies'}
D = {}
for f in sorted(glob.glob(os.path.join(here, 'data', '*.json'))):
    d = json.load(open(f, encoding='utf-8')); D[ALIAS.get(d['discipline'].lower(), d['discipline'])] = d

def camp(c):
    st = c['status'].strip().lower()
    q = MARK.get(st, st) + ('  ·  the simple story' if c.get('pop') else '')
    m = c['explain'].strip() + '\n\nWho: ' + c['who'].strip() + '\nBest work: ' + c['best'].strip() + '\nThe evidence: ' + c['evidence'].strip()
    return {'q': q, 'f': c['name'].strip() + '. ' + c['line'].strip(), 'm': m, 'ml': 'Who, and the evidence', 'c': c['line'].strip()}

P, missing, nf, nc = [], [], 0, 0
for gname, gsig, discs in GROUPS:
    g = {'n': gname, 'i': tx(gsig), 'u': [], 't': []}
    for dname, dsig in discs:
        d = D.pop(dname, None)
        if d is None: missing.append(dname); continue
        idx = [len(g['t'])]
        g['t'].append({'t': 'The lay of the land', 'p': d['overview'],
                       'k': [{'q': b['title'], 'f': b['verdict'], 'c': b['title'] + ' ' + b['verdict']} for b in d['debates']]})
        for b in d['debates']:
            idx.append(len(g['t'])); nf += 1; nc += len(b['camps'])
            g['t'].append({'t': b['title'].rstrip('?').rstrip(), 'p': b['lead'] + '\n\nWhere it’s landing: ' + b['verdict'], 'k': [camp(c) for c in b['camps']]})
        g['u'].append({'n': dname, 'i': tx(dsig), 't': idx})
    if g['u']: P.append(g)

if missing: print('missing:', ', '.join(missing))
if D: print('unplaced:', ', '.join(D))
shell.build(P, os.path.join(here, '..', 'index.html'),
    title='So you want to understand…', lead='So you want to understand', key='wu',
    words=['group', 'discipline', 'fight', 'camp'], steps=['group', 'discipline', 'fight', 'camps'],
    sub='<p class="sub">Every field has a simple story it tells the public and a messier one it tells itself. Here are the big fights inside each discipline: who stands where, what they got right, and which way the evidence is leaning.</p>',
    foot='<a class="foot" href="https://jere-mee-as.github.io/tenbestpapers/">The ten best papers →</a>', theme='ink')
print(f'{sum(len(g["u"]) for g in P)} disciplines · {nf} fights · {nc} camps')
