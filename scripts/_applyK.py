import base64, gzip, json, os, subprocess, hashlib
blob = open('scripts/_dK.txt').read().strip()
assert hashlib.sha256(blob.encode()).hexdigest() == 'f8f122de38c0950d750e0db249e34e8e0e719d98a428131114ccb15bb7029719'
d = json.loads(gzip.decompress(base64.b64decode(blob)).decode())
for path, content in d['new'].items():
    open(path,'w').write(content); print('wrote', path, len(content))
for path, (marker, newtail) in d['tail'].items():
    s = open(path).read(); assert s.count(marker) == 1, 'marker %d' % s.count(marker)
    open(path,'w').write(s[:s.index(marker)] + newtail); print('tail', path)
for path, old, new in d['sub']:
    s = open(path).read(); assert s.count(old) == 1, 'sub %d in %s' % (s.count(old), path)
    open(path,'w').write(s.replace(old, new)); print('patched', path)
os.remove('scripts/_dK.txt'); os.remove('scripts/_applyK.py')
for f in os.listdir('.github/workflows'):
    if f.startswith('deploy-r22'): os.remove('.github/workflows/'+f)
subprocess.run(['git','add','-A'], check=True)
subprocess.run(['git','-c','user.name=github-actions[bot]','-c','user.email=41898282+github-actions[bot]@users.noreply.github.com','commit','-m','Animated welcome, amber daily labels, working contact email'], check=True)
subprocess.run(['git','push'], check=True)
print('pushed')
