import re, math, random, pickle, json
from collections import Counter
random.seed(2026)
models = pickle.load(open('models.pkl','rb'))

# ---------- Voynich ----------
voy = []
for raw in open('ZL3b-n.txt', encoding='utf-8', errors='replace'):
    raw2 = raw.strip()
    m = re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)$', raw2)
    if not m: continue
    text = re.sub(r'<[^>]*>', '', m.group(5))
    text = re.sub(r'\[([^:\]]*):[^\]]*\]', r'\1', text)
    text = re.sub(r'\{[^}]*\}', '', text).replace(',', '.')
    voy.extend(re.sub(r'[^a-z]','',w) for w in text.split('.') if re.sub(r'[^a-z]','',w))

def H2words(ws):
    big=Counter(); uni=Counter()
    for w in ws:
        s='#'+w+'#'
        for i in range(len(s)-1): big[s[i:i+2]]+=1; uni[s[i]]+=1
    tb=sum(big.values())
    return -sum(c/tb*math.log2(c/uni[a[0]]) for a,c in big.items())

out = {}
# ---------- 1. entropy across languages ----------
ent = {'Voynich': round(H2words(voy),2)}
NAMES = {'latim':'Latim','português':'Português','hebraico':'Hebraico','grego':'Grego',
         'alemão':'Alemão','turco':'Turco','árabe':'Árabe'}
for key, label in NAMES.items():
    ws = models[key][3].split()[:len(voy)]
    ent[label] = round(H2words(ws),2)
lat = models['latim'][3].split()[:len(voy)]
ent['Latim sem vogais'] = round(H2words([w for w in (re.sub(r'[aeiou]','',x) for x in lat) if w]),2)
out['entropia_H2'] = ent
print("H2:", ent)

# ---------- 2. attack scoreboard: control vs Voynich, all languages ----------
class Attack:
    def __init__(self, tri, bi):
        self.logp = {t: math.log((c+0.1)/(bi.get(t[:2],0)+0.1*31)) for t,c in tri.items()}
        self.floor = math.log(0.1/(0.1*31))
    def ws_(self, dec, wins):
        lp=self.logp; fl=self.floor
        return sum(lp.get(''.join(dec[w:w+3]), fl) for w in wins)
    def solve(self, cipher, targets, iters=18000, restarts=2):
        syms = sorted(set(cipher)-{' '}); n=len(cipher)
        pos = {s:[i for i,c in enumerate(cipher) if c==s] for s in syms}
        wof = {}
        for s in syms:
            st=set()
            for p in pos[s]:
                for w in (p-2,p-1,p):
                    if 0<=w<=n-3: st.add(w)
            wof[s]=sorted(st)
        best=None
        for r in range(restarts):
            mp={s:random.choice(targets) for s in syms}
            dec=[mp.get(c,' ') if c!=' ' else ' ' for c in cipher]
            for it in range(iters):
                T=0.08*(1-it/iters)*(n-2)*0.01
                if random.random()<0.5:
                    s1=random.choice(syms); old=mp[s1]; nt=random.choice(targets)
                    if nt==old: continue
                    wns=wof[s1]; before=self.ws_(dec,wns)
                    for p in pos[s1]: dec[p]=nt
                    d=self.ws_(dec,wns)-before
                    if d>=0 or random.random()<math.exp(d/max(T,1e-9)): mp[s1]=nt
                    else:
                        for p in pos[s1]: dec[p]=old
                else:
                    s1,s2=random.sample(syms,2)
                    wns=sorted(set(wof[s1])|set(wof[s2])); before=self.ws_(dec,wns)
                    a,b=mp[s1],mp[s2]
                    for p in pos[s1]: dec[p]=b
                    for p in pos[s2]: dec[p]=a
                    d=self.ws_(dec,wns)-before
                    if d>=0 or random.random()<math.exp(d/max(T,1e-9)): mp[s1],mp[s2]=b,a
                    else:
                        for p in pos[s1]: dec[p]=a
                        for p in pos[s2]: dec[p]=b
            sc=self.ws_(dec,range(n-2))
            if best is None or sc>best[0]: best=(sc,dict(mp))
        return best[0]/(n-2), best[1]

vtext = ' '.join(voy)[:3500]
board = {}
for key,label in NAMES.items():
    tri,bi,letters,sample = models[key]
    atk = Attack(tri,bi)
    ref = atk.ws_(list(sample[:20000]), range(20000-2))/(20000-2)
    plain = sample[1000:4500]
    kk = {c:t for c,t in zip(letters, random.sample(letters,len(letters)))}
    ciph = ''.join(kk.get(c,c) if c!=' ' else ' ' for c in plain)
    cs, cmp_ = atk.solve(ciph, letters)
    dec_c = ''.join(cmp_.get(c,c) if c!=' ' else ' ' for c in ciph)
    recov = sum(1 for a,b in zip(dec_c,plain) if a==b)/len(plain)*100
    vs, vmp = atk.solve(vtext, letters)
    board[label] = dict(ref=round(ref,3), controle=round(ref-cs,3), voynich=round(ref-vs,3), recuperacao=round(recov))
    print(label, board[label])
out['placar'] = board
json.dump(out, open('numbers.json','w'), ensure_ascii=False, indent=1)
