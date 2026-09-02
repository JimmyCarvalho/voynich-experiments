import numpy as np, cv2, sys, json
from gaps import line_bands, gaps_in_line
def measure(page, x0,x1,y0,y1, core=11):
    gray=cv2.imread(page,cv2.IMREAD_GRAYSCALE)
    th,bands=line_bands(gray,x0,x1,y0,y1)
    res=[]
    for (lo,hi,p) in bands:
        c=th[max(0,p-y0-core):p-y0+core,:]
        g,(a,b)=gaps_in_line(c)
        res.append(dict(peak=int(p),ext=(int(a+x0),int(b+x0)),gaps=[(int(x+x0),int(w)) for x,w in g],
                        xheight=None))
    return res
if __name__=='__main__':
    page=sys.argv[1]; x0,x1,y0,y1=map(int,sys.argv[2:6]); tag=sys.argv[6]
    res=measure(page,x0,x1,y0,y1)
    json.dump(res,open(f'{tag}.gaps.json','w'))
    allg=[w for o in res for _,w in o['gaps'] if w<30]
    print(f"{tag}: {len(res)} linhas, {len(allg)} vaos (<30px)")
    h=np.bincount(allg,minlength=30)
    for w in range(1,30):
        print(f"  {w:2d}px {'#'*int(h[w]/2)} {h[w]}")
