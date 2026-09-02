# Exp 60: a ligacao fim->inicio atravessa a QUEBRA DE LINHA? (a linha e uma unidade mais dura que a palavra?)
import re, random
from exp49 import parse
from exp56 import MI
random.seed(1)
voy=parse('ZL3b-n.txt')
within=[]; across=[]; across2=[]
for lines in voy:
    for i,line in enumerate(lines):
        for a,b in zip(line,line[1:]): within.append((a[-1],b[0]))
        if i+1<len(lines) and line and lines[i+1]:
            across.append((line[-1][-1], lines[i+1][0][0]))
        if i+2<len(lines) and line and lines[i+2]:
            across2.append((line[-1][-1], lines[i+2][0][0]))
def shuf(pairs):
    b=[y for _,y in pairs]; random.shuffle(b); return list(zip([x for x,_ in pairs],b))
print(f"pares dentro da linha:      n={len(within):6d}  MI={MI(within):.3f}   (embaralhado {MI(shuf(within)):.3f})")
print(f"pares atraves da quebra:    n={len(across):6d}  MI={MI(across):.3f}   (embaralhado {MI(shuf(across)):.3f})")
print(f"fim da linha -> inicio da linha i+2: n={len(across2):6d}  MI={MI(across2):.3f}")
# controle de tamanho: MI dentro da linha com a mesma amostra n
sub=random.sample(within,len(across))
print(f"dentro da linha, mesma amostra n={len(across)}: MI={MI(sub):.3f}")
