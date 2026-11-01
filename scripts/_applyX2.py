import base64, gzip, json, os, re, random, subprocess, hashlib, yaml, collections
blob = open('scripts/_dX.txt').read().strip()
assert hashlib.sha256(blob.encode()).hexdigest() == '175d82a6773237d3f992b4f79f739b8f5012c8ee8ad1f34c2a5bd0eacf815ad7', 'sha'
groups = json.loads(gzip.decompress(base64.b64decode(blob)).decode())['groups']
path = '_data/thoughts.yml'
raw = open(path).read()
head = raw.split('\n\n- text:')[0] + '\n\n'
live = yaml.safe_load(raw)
old = {e['text'].strip().lower() for e in live}
seen = set()
for g, lst in groups.items():
    for t, who, what, src in lst:
        k = t.strip().lower()
        assert k not in old, 'overlap: ' + t[:50]
        assert k not in seen, 'dup: ' + t[:50]
        seen.add(k)
        assert t and who and what and src and re.search(r'\d', src), 'incomplete: ' + t[:40]
print('no overlap, no duplicates, all sourced')
RULES = [
 ('economics',  r'econom'),
 ('science',    r'physic|chemist|astronom|mathematic|logician|biolog|geneticist|naturalist|palaeontolog|etholog|primatolog|bacteriolog|virolog|astrophysic|meteorolog|cybernetic|statistic'),
 ('mind',       r'psycholog|psychiat|psychoanalyst|cognitive|physiolog'),
 ('medicine',   r'physician|surgeon|monk and scientist'),
 ('society',    r'sociolog|political|historian|anthropolog|jurist|theorist|legal|reformer|activist|statesman|emperor|leader|organiser|urbanist|geograph|educator|epidemiolog|media'),
 ('letters',    r'novelist|poet|writer|critic|playwright|essayist|humanist|chronicler|grammarian'),
 ('philosophy', r'philosoph|theologian|teacher|text'),
 ('systems',    r'computer|engineer|management|executive|scholar|scientist|researcher|technologist'),
]
def bucket(what):
    w = what.lower()
    for name, pat in RULES:
        if re.search(pat, w): return name
    return 'other'
allr = [(e['text'], e['who'], e['what'], e['source']) for e in live]
allr += [tuple(e) for lst in groups.values() for e in lst]
pools = collections.defaultdict(list)
for e in allr: pools[bucket(e[2])].append(e)
counts = {k: len(v) for k, v in pools.items()}
total = sum(counts.values())
print('buckets:', sorted(counts.items(), key=lambda x: -x[1]))
assert max(counts.values()) <= (total + 1)//2, 'bucket too large'
rng = random.Random(4471)
for v in pools.values(): rng.shuffle(v)
remaining = dict(counts)
order, prev = [], None
for i in range(total):
    cands = [k for k in pools if remaining[k] > 0 and k != prev]
    assert cands, 'stuck at %d' % i
    top = max(remaining[k] for k in cands)
    pick = rng.choice([k for k in cands if remaining[k] == top])
    e = pools[pick][remaining[pick]-1]; remaining[pick] -= 1
    order.append((pick, e)); prev = pick
if order[0][0] == order[-1][0]:
    n = len(order)
    for i in range(1, n-1):
        if order[i][0] != order[n-1][0] and order[i+1][0] != order[0][0]:
            order = order[:i+1] + order[i+1:][::-1]; break
bad = [i for i in range(total) if order[i][0] == order[(i+1) % total][0]]
assert not bad, bad
print('alternation holds end to end')
def q(s): return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'
lines = []
for _, (t, who, what, src) in order:
    lines += ['- text: ' + q(t), '  who: ' + q(who), '  what: ' + q(what), '  source: ' + q(src)]
text = head + '\n'.join(lines) + '\n'
open(path, 'w').write(text)
d = yaml.safe_load(text)
assert len(d) == total == 505, (len(d), total)
assert len({e['text'].lower() for e in d}) == total
assert all(e.get('source') for e in d)
print('FINAL:', len(d), 'thoughts |', len({e['who'] for e in d}), 'thinkers')
os.remove('scripts/_dX.txt')
for f in ['scripts/_applyX.py', 'scripts/_applyX2.py']:
    if os.path.exists(f): os.remove(f)
for f in os.listdir('.github/workflows'):
    if f.startswith('deploy-r35') or f.startswith('deploy-r36'): os.remove('.github/workflows/'+f)
subprocess.run(['git','add','-A'], check=True)
subprocess.run(['git','-c','user.name=github-actions[bot]','-c','user.email=41898282+github-actions[bot]@users.noreply.github.com','commit','-m','505 thoughts of the day'], check=True)
subprocess.run(['git','push'], check=True)
print('pushed')
