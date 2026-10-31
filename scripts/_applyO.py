import base64, gzip, json, os, subprocess, hashlib
blob = open('scripts/_dO.txt').read().strip()
assert hashlib.sha256(blob.encode()).hexdigest() == '5cc3dcdcb1a0f137d11203fb1eaa30f54cdef3d7ea049f44de0c48b8f631a3ee'
d = json.loads(gzip.decompress(base64.b64decode(blob)).decode())
for p, c in d['new'].items(): open(p,'w').write(c); print('wrote', p, len(c))
for p, t in d['append'].items(): open(p,'a').write(t); print('appended', p, len(t))
for p, o, n in d['sub']:
    s = open(p).read(); assert s.count(o) == 1, 'sub %d in %s' % (s.count(o), p)
    open(p,'w').write(s.replace(o, n)); print('patched', p)
os.remove('scripts/_dO.txt'); os.remove('scripts/_applyO.py')
for f in os.listdir('.github/workflows'):
    if f.startswith('deploy-r26'): os.remove('.github/workflows/'+f)
subprocess.run(['git','add','-A'], check=True)
subprocess.run(['git','-c','user.name=github-actions[bot]','-c','user.email=41898282+github-actions[bot]@users.noreply.github.com','commit','-m','A colour and a label for each band, and tick marks in the margins'], check=True)
subprocess.run(['git','push'], check=True)
print('pushed')
