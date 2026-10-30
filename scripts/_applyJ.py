import base64, gzip, json, os, subprocess, hashlib
blob = open('scripts/_dJ.txt').read().strip()
assert hashlib.sha256(blob.encode()).hexdigest() == '855046e2b24866db1f6dee83df82c204b8d77ff28bd60c9133eda1c1b051d40b'
d = json.loads(gzip.decompress(base64.b64decode(blob)).decode())
for path, content in d['new'].items():
    open(path, 'w').write(content); print('wrote', path, len(content))
for path, (marker, newtail) in d['tail'].items():
    s = open(path).read()
    assert s.count(marker) == 1, 'marker count %d' % s.count(marker)
    s = s[:s.index(marker)] + newtail
    open(path, 'w').write(s); print('tail', path, len(s))
os.remove('scripts/_dJ.txt'); os.remove('scripts/_applyJ.py')
for f in os.listdir('.github/workflows'):
    if f.startswith('deploy-r21'): os.remove('.github/workflows/'+f)
subprocess.run(['git','add','-A'], check=True)
subprocess.run(['git','-c','user.name=github-actions[bot]','-c','user.email=41898282+github-actions[bot]@users.noreply.github.com','commit','-m','Welcome line and six rotating opening drawings'], check=True)
subprocess.run(['git','push'], check=True)
print('pushed')
