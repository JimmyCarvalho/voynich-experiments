# Exp 80b, passo A: aprender a segmentacao (unigramas / prefixo+sufixo) SEM a chave, e checar no controle
import re, math, random, sys
from collections import Counter, defaultdict
def learn_segmentation(words_counter, n_uni=170, iters=12, maxaff=6):
    # unigramas = tipos mais frequentes
    types=sorted(words_counter.items(), key=lambda x:-x[1])
    U=set(w for w,_ in types[:n_uni])
    rest=[(w,c) for w,c in types if w not in U and len(w)>=2]
    # inicializacao: contagens de prefixos/sufixos possiveis (ponderadas)
    f=Counter(); g=Counter()
    for w,c in rest:
        for k in range(1,min(maxaff,len(w)-1)+1):
            f[w[:k]]+=c/ (len(w)-1); g[w[k:]]+=c/(len(w)-1)
    split={}
    for _ in range(iters):
        nf=Counter(); ng=Counter()
        for w,c in rest:
            best=None
            for k in range(1,min(maxaff,len(w)-1)+1):
                p,s=w[:k],w[k:]
                if len(s)>maxaff: continue
                sc=math.log(f[p]+1e-9)+math.log(g[s]+1e-9)
                if best is None or sc>best[0]: best=(sc,p,s)
            if best: split[w]=(best[1],best[2]); nf[best[1]]+=c; ng[best[2]]+=c
        f,g=nf,ng
    return U,split,f,g
if __name__=='__main__':
    L1=[l.split() for l in open('naibbe/encrypted/lat_output_ciphertext.txt')]
    L2=[l.split() for l in open('naibbe/respaced_plaintext/lat_pre_encryption_respaced_plaintext.txt')]
    pairs=[(a,b) for a,b in zip(L1,L2) if a and b and len(a)==len(b)]
    cnt=Counter(w for a,_ in pairs for w in a)
    # verdade: tabelas
    import csv
    tab={}
    for row in csv.DictReader(open('naibbe/references/naibbe_tables.csv',encoding='utf-8-sig')): tab[row['code']]=row['glyphs']
    true_uni={v for k,v in tab.items() if k.startswith('unigram')}
    true_pre={v for k,v in tab.items() if k.startswith('prefix')}; true_suf={v for k,v in tab.items() if k.startswith('suffix')}
    print(f"tabelas verdadeiras: {len(true_uni)} unigramas, {len(true_pre)} prefixos ({len(set(true_pre))} distintos), {len(true_suf)} sufixos ({len(set(true_suf))} distintos)")
    for n_uni in [120,156,170,200]:
        U,split,f,g=learn_segmentation(cnt,n_uni=n_uni)
        u_ok=sum(1 for w in U if w in true_uni)
        # acuracia da divisao: palavra bigrama verdadeira = prefixo+sufixo verdadeiros; checa se a divisao aprendida bate
        ok=tot=0
        for w,(p,s) in split.items():
            if w in true_uni: continue
            # divisao verdadeira: existe (p',s') com p' em prefixos e s' em sufixos e p'+s'==w
            cands=[(p2,w[len(p2):]) for p2 in true_pre if w.startswith(p2) and w[len(p2):] in true_suf]
            if not cands: continue
            tot+=cnt[w]; ok+= cnt[w] if (p,s) in cands else 0
        topP=set(x for x,_ in f.most_common(len(set(true_pre)))); topS=set(x for x,_ in g.most_common(len(set(true_suf))))
        print(f"n_uni={n_uni}: unigramas certos {u_ok}/{n_uni}; divisao certa em {ok/tot*100:.1f}% dos tokens bigrama; prefixos verdadeiros recuperados {len(topP&true_pre)}/{len(set(true_pre))}; sufixos {len(topS&true_suf)}/{len(set(true_suf))}")
