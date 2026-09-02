import numpy as np, cv2, sys, json
from scipy.signal import find_peaks
def line_bands(gray, x0, x1, y0, y1, pitch_min=20):
    reg=gray[y0:y1, x0:x1]
    th=cv2.threshold(cv2.GaussianBlur(reg,(3,3),0),0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    rows=(th>0).sum(axis=1).astype(float)
    sm=np.convolve(rows,np.ones(7)/7,mode='same')
    peaks,_=find_peaks(sm,distance=pitch_min,prominence=sm.max()*0.15)
    bands=[]
    for i,p in enumerate(peaks):
        lo=(peaks[i-1]+p)//2 if i>0 else max(0,p-14)
        hi=(p+peaks[i+1])//2 if i+1<len(peaks) else min(len(rows)-1,p+14)
        bands.append((y0+lo,y0+hi,y0+p))
    return th,bands
def gaps_in_line(th_line, min_ink=1):
    cols=(th_line>0).sum(axis=0)
    ink=cols>=min_ink
    # ignora margens
    xs=np.where(ink)[0]
    if len(xs)==0: return [],[]
    a,b=xs[0],xs[-1]
    runs=[]; blobs=[]; cur=a; inb=True; start=a
    x=a
    gapsl=[]
    while x<=b:
        if not ink[x]:
            g0=x
            while x<=b and not ink[x]: x+=1
            gapsl.append((g0,x-g0))   # (posicao, largura)
        else: x+=1
    return gapsl,(a,b)
if __name__=='__main__':
    page=sys.argv[1]; x0,x1,y0,y1=map(int,sys.argv[2:6])
    gray=cv2.imread(page,cv2.IMREAD_GRAYSCALE)
    th,bands=line_bands(gray,x0,x1,y0,y1)
    print(len(bands),'linhas, picos em',[b[2] for b in bands])
    out=[]
    for (lo,hi,p) in bands:
        # nucleo da linha: +-11 px em torno do pico (evita hastes das linhas vizinhas)
        core=th[max(0,p-y0-11):p-y0+11, :]
        g,(a,b)=gaps_in_line(core)
        out.append(dict(peak=int(p),ext=(int(a+x0),int(b+x0)),gaps=[(int(x+x0),int(w)) for x,w in g]))
    json.dump(out,open(page+'.gaps.json','w'))
    for o in out:
        ws=[w for _,w in o['gaps']]
        print(f"y={o['peak']:4d} largura={o['ext'][1]-o['ext'][0]:4d}px  vaos={len(ws):3d}  larguras ordenadas: {sorted(ws,reverse=True)[:14]}")
