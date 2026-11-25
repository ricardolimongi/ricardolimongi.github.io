"""Gera a arte de fundo das seções (assets/img/cena-*.webp). Uso: python3 arte.py <pasta de saída>
Tema: traço humano (fluxo, amarelo) e malha da máquina (pontos, azul). Requer numpy, scipy e pillow."""
import sys, numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter as G, map_coordinates
W, H = 1920, 1200
out = sys.argv[1]
only = sys.argv[2:]
Y, X = np.mgrid[0:H, 0:W].astype(float)
INK = np.array([10, 15, 30.])

def noise(rng, scale, octaves=4):
    r = np.zeros((H, W))
    for o in range(octaves):
        s = scale / 2**o
        g = rng.standard_normal((int(H/s)+4, int(W/s)+4))
        r += map_coordinates(g, [Y/s+1, X/s+1], order=3) / 2**o
    return r / r.std()

def splat(x, y, w=1.0):
    ok = (x >= 0) & (x < W-1) & (y >= 0) & (y < H-1)
    x, y = x[ok], y[ok]
    w = np.broadcast_to(w, ok.shape)[ok]
    xi, yi = x.astype(int), y.astype(int); fx, fy = x-xi, y-yi
    d = np.zeros(W*H)
    for dx, dy, k in ((0,0,(1-fx)*(1-fy)),(1,0,fx*(1-fy)),(0,1,(1-fx)*fy),(1,1,fx*fy)):
        d += np.bincount((yi+dy)*W+xi+dx, weights=w*k, minlength=W*H)
    return d.reshape(H, W)

def flow(ang, x, y, steps, w=1.0, dt=1.0):
    d = np.zeros((H, W)); n = steps
    for i in range(n):
        xi = np.clip(x, 0, W-1).astype(int); yi = np.clip(y, 0, H-1).astype(int)
        a = ang[yi, xi]; x = x+np.cos(a)*dt; y = y+np.sin(a)*dt
        d += splat(x, y, w*np.sin(np.pi*(i+.5)/n))
    return d

def tone(d, q=99.6, g=.6):
    d = np.log1p(d*3/np.percentile(d[d > 0], 90)) if (d > 0).any() else d
    return np.clip(d/np.percentile(d, q), 0, 1.15)**(1/g*.75)

def compose(layers, name, base=INK, tint=None, glow=.45):
    im = np.zeros((H, W, 3)) + base
    if tint is not None:
        cx, cy, rx, ry, col, k = tint
        im += (np.exp(-(((X-cx*W)/(rx*W))**2+((Y-cy*H)/(ry*H))**2))*k)[..., None]*np.array(col)*.5
    for d, col in layers:
        t = d + G(d, 9)*glow*1.3 + G(d, 45)*glow*1.6
        im += t[..., None]*np.array(col, float)
    im = 255*(1-np.exp(-im/190.))
    im += np.random.default_rng(1).normal(0, 1.1, (H, W, 1))
    Image.fromarray(np.clip(im, 0, 255).astype('uint8')).resize((1600, 1000), Image.LANCZOS).save(f'{out}/cena-{name}.webp', quality=66, method=6)
    print(name)

AM, AZ = (245, 172, 22), (74, 122, 230)

def lines_seed(rng, n, x0, x1, y0=-.1, y1=1.1):
    return rng.uniform(x0*W, x1*W, n), rng.uniform(y0*H, y1*H, n)

def inicio():
    r = np.random.default_rng(7)
    a = noise(r, 620, 2)*.75 - .35
    x, y = lines_seed(r, 5200, .05, .95)
    k = np.exp(-((x/W-.70)/.26)**2)*r.gamma(1.2, 1, x.size)
    warm = tone(flow(a, x, y, 620, k), 99.8)
    mask = 1/(1+np.exp(-(X/W-.60+.10*noise(r, 420, 2)*.6)/.06))
    warm *= np.clip(mask+.10, 0, 1)
    # malha de pontos deformada pelo mesmo campo
    gy, gx = np.mgrid[-20:H+20:15, -20:W+20:15].astype(float)
    gx, gy = gx.ravel(), gy.ravel()
    yi, xi = np.clip(gy,0,H-1).astype(int), np.clip(gx,0,W-1).astype(int)
    f = noise(r, 520, 2)[yi, xi]
    p = np.clip(1.0-mask[yi, xi]*.95, 0, 1)*np.clip(f*.5+.6, .08, 2)
    dots = G(splat(gx+f*7, gy+np.roll(f, 9)*7, p), 1.25)*9
    compose([(dots, AZ), (warm*.6, AM)], 'inicio', tint=(.72, .55, .34, .6, (90, 70, 14), .9))

def relevo():
    r = np.random.default_rng(21)
    n = noise(r, 620, 5); n = G(n, 3)
    c = np.abs(((n*5.5) % 1)-.5); gy, gx = np.gradient(n*5.5); m = np.hypot(gx, gy)+1e-6
    l = np.clip(1.2-(.5-c)/m/1.0, 0, 1)
    c2 = np.abs(((n*1.1) % 1)-.5); l2 = np.clip(1.6-(.5-c2)/(m/5)/1.0, 0, 1)
    f = np.clip((X/W-.2)/.7, .12, 1)
    compose([(l*.42*f, (52, 150, 150)), (l2*.55*f, AM)], 'sobre', np.array([6, 20, 26.]), (.85, .3, .5, .6, (10, 62, 66), 1), .3)

def rede():
    r = np.random.default_rng(5)
    cen = np.array([[.86,.25],[.70,.66],[.95,.74],[.5,.2],[.3,.82]]); P=[]; gid=[]
    for i,(cx,cy) in enumerate(cen):
        n=[95,85,70,45,35][i]; P.append(np.c_[r.normal(cx,.07,n)*W, r.normal(cy,.10,n)*H]); gid += [i]*n
    P=np.vstack(P); gid=np.array(gid); xs=[];ys=[];ws=[];xs2=[];ys2=[];ws2=[]
    for i in range(len(P)):
        d=np.hypot(*(P-P[i]).T); nb=list(np.argsort(d)[1:5])
        if r.random()<.22: nb.append(r.integers(len(P)))
        for j in nb:
            L=np.hypot(*(P[j]-P[i])); t=np.linspace(0,1,int(L*1.6)+2)
            mid=(P[i]+P[j])/2+np.array([-(P[j]-P[i])[1],(P[j]-P[i])[0]])*.16
            q=((1-t)**2)[:,None]*P[i]+(2*t*(1-t))[:,None]*mid+(t**2)[:,None]*P[j]
            (xs if gid[i]==gid[j] else xs2).append(q[:,0]); (ys if gid[i]==gid[j] else ys2).append(q[:,1])
            (ws if gid[i]==gid[j] else ws2).append(np.full(t.size,.30 if gid[i]==gid[j] else .5))
    e=splat(np.concatenate(xs),np.concatenate(ys),np.concatenate(ws)); e2=splat(np.concatenate(xs2),np.concatenate(ys2),np.concatenate(ws2))
    nod=np.zeros((H,W)); 
    for s in (2.0,3.4,5.5):
        k=r.random(len(P))<{2.0:1,3.4:.35,5.5:.08}[s]; nod+=G(splat(P[k,0],P[k,1]),s)*s*s*6
    compose([(G(e,.6)*1.1,(86,110,235)),(G(e2,.7)*.5,AM),(np.clip(nod,0,1.4),(190,205,255))],'pesquisa',np.array([9,13,40.]),(.85,.5,.4,.6,(30,36,110),.9),.35)

def ondas():
    r=np.random.default_rng(3); nx,ny=noise(r,700,2)*26,noise(r,700,2)*26
    d1=np.hypot(X-.52*W+nx,Y-.42*H+ny); d2=np.hypot(X-1.02*W,Y-.62*H)
    a=np.sin(d1/7.5); b=np.sin(d2/7.5)
    l1=np.clip((a-.62)/.38,0,1)*np.exp(-d1/620); l2=np.clip((b-.62)/.38,0,1)*np.exp(-d2/820)
    compose([(l1*.5,AM),(l2*.6,(110,84,220)),(l1*l2*2.4,(255,225,170))],'hilab',np.array([18,11,34.]),(.8,.5,.4,.6,(56,28,96),.9),.15)

def registro():
    r=np.random.default_rng(11); s=24; f=noise(r,420,3)
    gy,gx=np.mgrid[12:H:s,12:W:s]; v=f[gy,gx]+ (gx/W-.5)*3.0+r.normal(0,.45,gx.shape)
    im=np.zeros((H,W)); hi=np.zeros((H,W))
    for y,x,k in zip(gy.ravel(),gx.ravel(),v.ravel()):
        if k>.0:
            h=int(min(k,2.4)*3.6)+1; (hi if r.random()<.06 else im)[max(y-2,0):y+3,max(x-h,0):x+h]=min(.25+k*.22,.85)
    compose([(im*.8,(46,130,120)),(hi*1.1,AM)],'materiais',np.array([7,24,26.]),(.9,.6,.4,.7,(10,60,52),.9),.3)

def ondulacao():
    r=np.random.default_rng(9); d=np.zeros((H,W)); d2=np.zeros((H,W)); x=np.linspace(0,W,5200)
    for i in range(90):
        t=i/90; amp=150*np.exp(-((x/W-.74)/.30)**2)+12
        y=H*.52+amp*(np.sin(x/190+t*5)*np.cos(x/410-t*2.2))*(.25+1.6*t)+(t-.5)*620*np.sin(x/700+.5)
        (d if i%9 else d2)[:]+=splat(x,y,.03+.42*np.exp(-((x/W-.8)/.38)**2))
    compose([(np.clip(G(d,.6)*1.3,0,1.2),(220,78,70)),(np.clip(G(d2,.7)*1.6,0,1.2),AM)],'videos',np.array([30,10,18.]),(.8,.5,.4,.5,(96,22,34),.8),.4)

def ressonancia():
    th=np.arctan2(Y-1.05*H,X-.80*W); d=np.hypot(X-.80*W,Y-1.05*H); r=np.random.default_rng(2)
    n=noise(r,500,3); rr=d/26+np.sin(th*9+n)*.35*np.clip(d/900,0,1); l=np.clip((np.cos(2*np.pi*rr)-.80)/.2,0,1)
    brk=np.clip(noise(r,130,2)*.6+.7,0,1.2); f=np.exp(-d/1000)
    pick=(np.floor(rr+.5).astype(int)%7==0)
    compose([(l*brk*f*~pick*1.0,(88,120,220)),(l*f*pick*1.1,AM)],'palestras',np.array([10,16,36.]),(.8,1,.5,.8,(36,50,110),.9),.3)

def arcos():
    r=np.random.default_rng(14); xs=[];ys=[];ws=[];k=[]
    base=.84*H; nod=np.sort(r.beta(2.2,1.2,46))*W*.98
    for _ in range(260):
        a,b=r.choice(nod,2,replace=False); R=abs(b-a)/2; c=(a+b)/2; t=np.linspace(0,np.pi,int(R*3)+8)
        xs.append(c+R*np.cos(t)); ys.append(base-R*.95*np.sin(t)); ws.append(np.full(t.size,.32*np.exp(-R/520)+.05)); k.append(np.full(t.size,r.random()<.12))
    x,y,w,k=map(np.concatenate,(xs,ys,ws,k)); k=k.astype(bool)
    p=G(splat(nod,np.full(nod.size,base)),3.2)*90
    compose([(G(splat(x[~k],y[~k],w[~k]),.6)*1.2,(205,120,60)),(G(splat(x[k],y[k],w[k]),.6)*1.5,AM),(np.clip(p,0,1.3),(255,232,190))],'publicacoes',np.array([26,16,12.]),(.78,.8,.4,.6,(84,44,14),.8),.35)

def agenda():
    r=np.random.default_rng(17); d=np.zeros((H,W)); pts=[]; x=np.linspace(0,W,4200); u=x/W
    for i in range(54):
        a=(i/53-.5); y=H*(.55+a*(1.25-1.05*np.exp(-((u-.8)/.22)**2)))+70*np.sin(u*4+a*2)*(1-u*.6)
        d+=splat(x,y,.06+.4*u**2)
        for k in r.integers(1400,4100,3): pts.append((x[k],y[k]))
    P=np.array(pts); s=r.random(len(P))
    n=G(splat(P[:,0],P[:,1]),2.2)*34; big=G(splat(P[s<.2,0],P[s<.2,1]),5)*170
    compose([(np.clip(G(d,.6)*.9,0,1),(176,70,170)),(np.clip(n,0,1.2),(240,170,225)),(np.clip(big,0,1.3),AM)],'eventos',np.array([26,9,30.]),(.82,.55,.3,.6,(96,26,92),.9),.3)

def contato():
    r=np.random.default_rng(31); n=noise(r,640,2)
    a=np.arctan2(.5*H-Y,.86*W-X)+n*.42
    x,y=lines_seed(r,4200,-.05,1.05); w=tone(flow(a,x,y,300,r.gamma(1,1,x.size)),99.9)
    compose([(w*.5,(70,112,215)),(w*np.exp(-np.hypot(X-.86*W,(Y-.5*H))/260)*1.1,AM)],'contato',tint=(.86,.5,.25,.4,(90,70,14),.7))

for f in (inicio, relevo, rede, ondas, registro, ondulacao, ressonancia, arcos, agenda, contato):
    if not only or f.__name__ in only: f()
