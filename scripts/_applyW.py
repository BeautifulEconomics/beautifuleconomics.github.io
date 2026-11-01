import base64, gzip, json, os, re, random, subprocess, hashlib, collections, yaml
blob = open('scripts/_dW.txt').read().strip()
assert hashlib.sha256(blob.encode()).hexdigest() == 'a1bef0775aa1d9b35f0707f82f022d801baf4547421a6bf8bef54f65829a735c', 'sha'
groups = json.loads(gzip.decompress(base64.b64decode(blob)).decode())['groups']
added = sum(len(v) for v in groups.values())
print('new entries received:', added)

path = '_data/thoughts.yml'
raw = open(path).read()
head = raw.split('\n\n- text:')[0] + '\n\n'
live = yaml.safe_load(raw)
print('already live:', len(live))

old_text = {e['text'].strip().lower() for e in live}
seen = set()
for g, lst in groups.items():
    for t, who, what, src in lst:
        k = t.strip().lower()
        assert k not in old_text, 'overlaps live file: ' + t[:50]
        assert k not in seen, 'duplicate in new batch: ' + t[:50]
        seen.add(k)
        assert t and who and what and src and re.search(r'\d', src), 'incomplete: ' + t[:40]
print('no overlap, no duplicates, every entry sourced')

pools = {g: [tuple(e) for e in lst] for g, lst in groups.items()}
pools['live'] = [(e['text'], e['who'], e['what'], e['source']) for e in live]
total = sum(len(v) for v in pools.values())
rng = random.Random(9021)
for v in pools.values(): rng.shuffle(v)
remaining = {k: len(v) for k, v in pools.items()}
order, prev = [], None
for i in range(total):
    cands = [k for k in pools if remaining[k] > 0 and k != prev]
    assert cands, 'stuck at %d' % i
    top = max(remaining[k] for k in cands)
    pick = rng.choice([k for k in cands if remaining[k] == top])
    e = pools[pick][remaining[pick] - 1]; remaining[pick] -= 1
    order.append((pick, e)); prev = pick
if order[0][0] == order[-1][0]:
    n = len(order)
    for i in range(1, n - 1):
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
assert len(d) == total == 354, (len(d), total)
assert len({e['text'].lower() for e in d}) == total, 'duplicate after merge'
assert all(e.get('source') for e in d)
print('FINAL:', len(d), 'thoughts |', len({e['who'] for e in d}), 'thinkers')

os.remove('scripts/_dW.txt'); os.remove('scripts/_applyW.py')
for f in os.listdir('.github/workflows'):
    if f.startswith('deploy-r34'): os.remove('.github/workflows/'+f)
subprocess.run(['git','add','-A'], check=True)
subprocess.run(['git','-c','user.name=github-actions[bot]','-c','user.email=41898282+github-actions[bot]@users.noreply.github.com','commit','-m','200 more thoughts, mostly from outside economics'], check=True)
subprocess.run(['git','push'], check=True)
print('pushed')
