# (a) a MI atraves do espaco e comparavel a MI DENTRO da palavra?
import re, math
from collections import Counter
from exp56 import corp, MI, cross_pairs
def within_pairs(ws): return [(w[i],w[i+1]) for w in ws for i in range(len(w)-1)]
print(f"{'corpus':34s} {'MI dentro da palavra':>20s} {'MI atraves do espaco':>20s} {'razao':>6s}")
for name in ['Voynich (EVA)','Voynich (glifos compostos)','latim','portugues','alemao','hebraico','turco','Naibbe (latim cifrado)']:
    ws=[w for w in corp[name] if w]
    wi=MI(within_pairs(ws)); cr=MI(cross_pairs(ws))
    print(f"{name:34s} {wi:20.3f} {cr:20.3f} {cr/wi:6.2f}")
