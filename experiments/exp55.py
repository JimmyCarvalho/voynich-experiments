# Exp 55: a cifra Naibbe (Greshko 2025) passa nos MEUS testes?
import re, math, random, statistics
from collections import Counter, defaultdict
from exp51 import voy_words, H2, H1
from exp49 import ed1
random.seed(2)

def lines_of(path):
    L=[]
    for l in open(path):
        ws=[re.sub(r'[^a-z]','',w) for w in l.split()]
        ws=[w for w in ws if w]
        if ws: L.append(ws)
    return L

voy=voy_words()
nai_lines=lines_of('naibbe/encrypted/lat_output_ciphertext.txt')
nai=[w for l in nai_lines for w in l]
print(f"Voynich: {len(voy)} palavras | Naibbe(latim): {len(nai)} palavras")
# amostra do mesmo tamanho
nai_s=nai[:len(voy)]

def repeats(ws,n):
    return sum(1 for k,c in Counter(tuple(ws[i:i+n]) for i in range(len(ws)-n+1)).items() if c>1)
lat=re.sub(r'[^a-z\s]','',open('latin_words.txt').read().lower()).split()[:len(voy)]

print(f"\n{'metrica':34s} {'Voynich':>10s} {'Naibbe':>10s} {'latim cru':>10s}")
def row(name,f):
    print(f"{name:34s} {f(voy):>10} {f(nai_s):>10} {f(lat):>10}")
row('H2 (entropia condicional)',lambda w: f"{H2(w):.3f}")
row('H1',lambda w: f"{H1(w):.3f}")
row('tamanho medio da palavra',lambda w: f"{sum(map(len,w))/len(w):.2f}")
row('TTR (tipos/palavras)',lambda w: f"{len(set(w))/len(w):.3f}")
row('tipos',lambda w: f"{len(set(w))}")
row('desvio/media do tamanho',lambda w: f"{statistics.pstdev(list(map(len,w)))/(sum(map(len,w))/len(w)):.3f}")
row('top-20 palavras (% do texto)',lambda w: f"{sum(c for _,c in Counter(w).most_common(20))/len(w)*100:.1f}%")
row('bigramas repetidos',lambda w: f"{repeats(w,2)}")
row('trigramas repetidos',lambda w: f"{repeats(w,3)}")
row('4-gramas repetidos',lambda w: f"{repeats(w,4)}")
row('5-gramas repetidos',lambda w: f"{repeats(w,5)}")
row('palavra = a anterior',lambda w: f"{sum(1 for a,b in zip(w,w[1:]) if a==b)}")
row('vizinhos a 1 letra (%)',lambda w: f"{sum(1 for a,b in zip(w,w[1:]) if ed1(a,b))/len(w)*100:.1f}%")
