"""Atualiza citações (Google Scholar, perfil público, uma leitura) em publications.yml e productions.yml.
Uso: python3 _tools/scholar.py. Confira a lista impressa antes de publicar. most_cited.yml e o total do perfil são atualizados à mão."""
import re,json,unicodedata,difflib
import html,os,datetime,urllib.request
u='https://scholar.google.com.br/citations?user=DpkPDqEAAAAJ&hl=pt-BR&pagesize=100'
s=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read().decode('utf-8');R=[]
for r in re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>',s,re.S):
    t=html.unescape(re.sub('<[^>]+>','',re.search(r'gsc_a_at"[^>]*>(.*?)</a>',r,re.S)[1]))
    c=re.search(r'gsc_a_ac[^>]*>(\d*)<',r);y=re.search(r'gsc_a_h[^>]*>(\d*)<',r)
    g=[html.unescape(re.sub('<[^>]+>','',x)) for x in re.findall(r'class="gs_gray">(.*?)</div>',r,re.S)]
    R.append(dict(t=t,c=int(c[1] or 0) if c else 0,y=int(y[1] or 0) if y else 0,v=g[1] if len(g)>1 else ''))
F=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','_data','')
def norm(x):return ' '.join(re.findall(r'[a-z0-9]+',unicodedata.normalize('NFKD',x).encode('ascii','ignore').decode().lower()))
def sim(a,b):
    a,b=norm(a),norm(b);n=difflib.SequenceMatcher(None,a,b).ratio()
    return max(n,.95) if min(len(a),len(b))>40 and (a.startswith(b) or b.startswith(a)) else n
def load(f):
    z=re.split(r'(?m)^(?=- (?:title|group):)',open(F+f).read());return z
P=load('publications.yml');Q=load('productions.yml')
def fld(b,k):
    m=re.search(rf'(?m)^(?:- |  ){k}: (.*)$',b);return json.loads(m[1]) if m and m[1].startswith('"') else (m[1] if m else None)
used=set();A={}
def run(blocks,tag,pen):
    prs=[]
    for k,b in enumerate(blocks):
        if not b.startswith('- '):continue
        for j,r in enumerate(R):
            q=sim(fld(b,'title'),r['t'])
            if q>=.86:
                vs=difflib.SequenceMatcher(None,norm(fld(b,'venue') or ''),norm(re.sub(r'\d','',r['v']))).ratio()
                dy=abs(int(fld(b,'year'))-r['y']) if r['y'] else 1
                prs.append((q+.5*vs-.06*dy,k,j,q,vs,dy))
    for sc,k,j,q,vs,dy in sorted(prs,reverse=True):
        if j in used or (tag,k) in A: continue
        if tag=='Q' and (vs<.35 or dy>1) : continue
        if dy>2: continue
        used.add(j);A[(tag,k)]=(j,q,vs,dy)
run(P,'P',0);run(Q,'Q',0)

assert len(R)>50, 'perfil não lido'
# versões traduzidas ou com título diferente: (início no site, início no Scholar)
MAN={'P':[('Integridade Científica na Era','Scientific Integrity in the Digital Age'),('Concrete vs. abstract','Concrete vs. abstract'),('Chocolates e Outras','Chocolates and'),('Deviances from planned purchases','Desvios das compras planejadas: implica')],
 'Q':[('Diretrizes para o uso','Diretrizes para o uso'),('Perspectiva evolutiva','Perspectiva Evolutiva'),('O Valor do Cliente','O Valor do Cliente')]}
for tag,bl in (('P',P),('Q',Q)):
    for a,c in MAN[tag]:
        k=next((k for k,b in enumerate(bl) if b.startswith('- ') and fld(b,'title').startswith(a)),None)
        j=next((j for j,r in enumerate(R) if r['t'].startswith(c) and j not in used),None)
        if k is not None and j is not None and (tag,k) not in A: used.add(j);A[(tag,k)]=(j,0,0,0)
hoje=datetime.date.today().isoformat()
for tag,bl,f in (('P',P,'publications.yml'),('Q',Q,'productions.yml')):
    for k,b in enumerate(bl):
        if not b.startswith('- '): continue
        b=re.sub(r'(?m)^  citations(_date)?: .*\n','',b.rstrip('\n')+'\n')
        if (tag,k) in A: b+=f"  citations: {R[A[(tag,k)][0]]['c']}\n  citations_date: {hoje}\n"
        bl[k]=b
    open(F+f,'w').write(''.join(bl))
print('total no perfil:',re.findall(r'gsc_rsb_std">(\d+)',s)[0],'| casados:',len(A))
for j,r in enumerate(R):
    if j not in used and r['c']>=5: print('sem correspondência:',r['c'],r['y'],r['t'][:80])
