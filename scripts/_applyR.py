import base64, gzip, json, os, subprocess, hashlib
blob = open('scripts/_dR.txt').read().strip()
assert hashlib.sha256(blob.encode()).hexdigest() == '07204d3b2eb4d33bae71338c585e82ec06c2d7a3c98e8fb02513c8b78d6d5874'
d = json.loads(gzip.decompress(base64.b64decode(blob)).decode())
for p, o, n in d['sub']:
    s = open(p).read(); assert s.count(o) == 1, 'sub %d in %s' % (s.count(o), p)
    open(p,'w').write(s.replace(o, n)); print('patched', p)
for f in ['assets/library/consumer_equilibrium_made_simple_beautiful_economics.pdf','assets/library/prisoners_dilemma_payoff_matrix_beautiful_economics.pdf']:
    assert os.path.exists(f), 'missing '+f
print('both pdfs present')
os.remove('scripts/_dR.txt'); os.remove('scripts/_applyR.py')
for f in os.listdir('.github/workflows'):
    if f.startswith('deploy-r29'): os.remove('.github/workflows/'+f)
subprocess.run(['git','add','-A'], check=True)
subprocess.run(['git','-c','user.name=github-actions[bot]','-c','user.email=41898282+github-actions[bot]@users.noreply.github.com','commit','-m','Drop the PDF size line and fix the game theory file path'], check=True)
subprocess.run(['git','push'], check=True)
print('pushed')
