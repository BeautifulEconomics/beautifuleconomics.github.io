import base64, gzip, json, os, subprocess, hashlib

def load(name, sha):
    blob = open('scripts/'+name).read().strip()
    assert hashlib.sha256(blob.encode()).hexdigest() == sha, name+' sha mismatch'
    return json.loads(gzip.decompress(base64.b64decode(blob)).decode())

G = load('_dG.txt', 'f5ebef596f91554afd90071a638af78910f491f923998efd8131bf594c8987b4')
I = load('_dI.txt', 'dd8724536be1e7c721d1cf2b37fb39a5047dee3a148f818d68392dc649e07df6')

for d in (G, I):
    for path, content in d.get('new', {}).items():
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        open(path, 'w').write(content)
        print('wrote', path, len(content))

css_path = 'assets/css/style.css'
css = open(css_path).read()
for anchor, repl in G['css']:
    assert css.count(anchor) == 1, 'anchor count %d' % css.count(anchor)
    css = css.replace(anchor, repl)
css += I['append'][css_path]
open(css_path, 'w').write(css)
print('css', len(css))

for path, old, new in I['sub']:
    s = open(path).read()
    assert s.count(old) == 1, 'sub count %d in %s' % (s.count(old), path)
    open(path, 'w').write(s.replace(old, new))
    print('patched', path)

os.remove('scripts/_dG.txt'); os.remove('scripts/_dI.txt'); os.remove('scripts/_apply.py')
for f in os.listdir('.github/workflows'):
    if f.startswith('deploy-r20'): os.remove('.github/workflows/'+f)
subprocess.run(['git','add','-A'], check=True)
subprocess.run(['git','-c','user.name=github-actions[bot]','-c','user.email=41898282+github-actions[bot]@users.noreply.github.com','commit','-m','Library categories and the homepage opening curtain'], check=True)
subprocess.run(['git','push'], check=True)
print('pushed')
