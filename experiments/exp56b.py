# Exp 56b: a MI atraves da fronteira sobrevive se os 8% de espacos INCERTOS forem tratados como nao-espacos?
import re, math, random
from collections import Counter
from exp56 import MI, cross_pairs, end_start_rate, space_predictability
random.seed(3)
def voy_variant(mode):
    out=[]
    for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
        m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',raw.strip())
        if not m: continue
        t=re.sub(r'<[^>]*>','',m.group(5)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t)
        if mode=='juntar': t=t.replace(',','')      # espaco incerto = sem espaco
        elif mode=='separar': t=t.replace(',','.')  # espaco incerto = espaco (padrao usado ate agora)
        elif mode=='descartar':                      # so fronteiras certas: quebra a linha nos incertos e ignora esses pares
            t=t.replace(',','|')
        out.extend(list(re.sub(r'[^a-z]','',w)) for w in re.split(r'[.|]',t) if re.sub(r'[^a-z]','',w))
    return out
print(f"{'tratamento dos espacos incertos':34s} {'palavras':>8s} {'MI d=1':>7s} {'MI d=2':>7s} {'fim->ini':>8s} {'previs.':>7s}")
for mode in ['separar','juntar']:
    ws=voy_variant(mode); mi1=MI(cross_pairs(ws,1)); mi2=MI(cross_pairs(ws,2)); r,_,_=end_start_rate(ws); _,_,pr=space_predictability(ws)
    print(f"{mode:34s} {len(ws):8d} {mi1:7.3f} {mi2:7.3f} {r*100:7.1f}% {pr*100:6.1f}%")
# so pares onde o espaco e CERTO (ponto): recomputa MI usando apenas fronteiras marcadas com '.'
pairs=[]; pairs2=[]
for raw in open('ZL3b-n.txt',encoding='utf-8',errors='ignore'):
    m=re.match(r'^<(f[^.>]+)\.([^,>]+),([@+=&])(P[a-z0-9]*)>\s*(.*)',raw.strip())
    if not m: continue
    t=re.sub(r'<[^>]*>','',m.group(5)); t=re.sub(r'\[([^:\]]*):[^\]]*\]',r'\1',t); t=re.sub(r'\{[^}]*\}','',t)
    toks=re.split(r'([.,])',t); toks=[x for x in toks if x!='']
    # sequencia palavra,sep,palavra,sep...
    items=[]
    for x in toks:
        if x in '.,': items.append(x)
        else:
            w=re.sub(r'[^a-z]','',x)
            if w: items.append(w)
    for i in range(len(items)-2):
        if items[i] not in '.,' and items[i+1]=='.' and items[i+2] not in '.,':
            pairs.append((items[i][-1],items[i+2][0]))
print(f"{'so fronteiras CERTAS (n='+str(len(pairs))+')':34s} {'':8s} {MI(pairs):7.3f}")
sh=[b for _,b in pairs]; random.shuffle(sh)
print(f"{'  mesmas fronteiras, embaralhadas':34s} {'':8s} {MI(list(zip([a for a,_ in pairs],sh))):7.3f}")
