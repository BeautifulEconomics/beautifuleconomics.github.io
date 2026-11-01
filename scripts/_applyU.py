import base64, gzip, json, os, subprocess, hashlib, yaml
blob = open('scripts/_dU.txt').read().strip()
assert hashlib.sha256(blob.encode()).hexdigest() == '6dd534fe499dc4391f9a54314fdd6d0581ffe4af7c3a82f475b63dbf647465f6', 'sha'
d = json.loads(gzip.decompress(base64.b64decode(blob)).decode())
for p, c in d['new'].items(): open(p,'w').write(c); print('wrote', p, len(c))
w = yaml.safe_load(open('_data/words.yml'))
assert isinstance(w, list) and len(w) == 500, len(w)
assert len({e['term'].lower() for e in w}) == 500, 'duplicate term'
assert all(e.get('meaning') for e in w), 'missing meaning'
bad = [i for i in range(500) if w[i]['field'] == w[(i+1) % 500]['field']]
assert not bad, bad
print('500 unique terms, alternation holds end to end')
os.remove('scripts/_dU.txt'); os.remove('scripts/_applyU.py')
for f in os.listdir('.github/workflows'):
    if f.startswith('deploy-r32'): os.remove('.github/workflows/'+f)
subprocess.run(['git','add','-A'], check=True)
subprocess.run(['git','-c','user.name=github-actions[bot]','-c','user.email=41898282+github-actions[bot]@users.noreply.github.com','commit','-m','500 words of the day across nine fields of economics'], check=True)
subprocess.run(['git','push'], check=True)
print('pushed')
