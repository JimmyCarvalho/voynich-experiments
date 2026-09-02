# Exp 65: comprimento de memoria do processo: H(proximo glifo | k anteriores), estimado em metade e avaliado na outra metade (sem overfitting)
import re, math, random
from collections import Counter, defaultdict
from exp64 import voy_lines, to_lines, xw, nai_lines
random.seed(2)
def streams(lines): return [' '.join(ws) for ws in lines]   # espaco como simbolo (o proprio texto tem)
def cond_entropy(train,test,k,alpha=0.05):
    ctx=defaultdict(Counter); V=set()
    for s in train:
        s='^'*k+s+'$'
        for i in range(k,len(s)):
            ctx[s[i-k:i]][s[i]]+=1; V.add(s[i])
    V=len(V)+1; lp=0; n=0
    # backoff simples: se contexto nao visto, usa k-1 ... (recursivo via tabelas menores)
    tabs=[ctx]
    for kk in range(k-1,-1,-1):
        t=defaultdict(Counter)
        for s in train:
            s='^'*kk+s+'$'
            for i in range(kk,len(s)): t[s[i-kk:i]][s[i]]+=1
        tabs.append(t)
    for s in test:
        s='^'*k+s+'$'
        for i in range(k,len(s)):
            p=None
            for j,t in enumerate(tabs):
                kk=k-j; c=t.get(s[i-kk:i]) if kk>0 else t.get('')
                if c and sum(c.values())>=3:
                    p=(c[s[i]]+alpha)/(sum(c.values())+alpha*V); break
            if p is None: p=1/V
            lp-=math.log2(p); n+=1
    return lp/n
N=34119
corp={'Voynich':streams(voy_lines()),
      'latim':streams(to_lines(re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()[:N])),
      'portugues':streams(to_lines(xw('Portuguese.xml')[:N])),
      'alemao':streams(to_lines(xw('German.xml')[:N])),
      'Naibbe (latim cifrado)':streams(nai_lines())}
print(f"{'corpus':24s} "+' '.join(f'{"k="+str(k):>7s}' for k in range(0,7))+"   ganho k=2->k=6")
for name,S in corp.items():
    random.shuffle(S); half=len(S)//2; tr,te=S[:half],S[half:]
    hs=[cond_entropy(tr,te,k) for k in range(0,7)]
    print(f"{name:24s} "+' '.join(f'{h:7.3f}' for h in hs)+f"   {hs[2]-hs[6]:+.3f} bits")
