"""Atualiza DOI (ORCID, OpenAlex, Crossref) e citações (OpenAlex) em _data/publications.yml.
Uso: python3 _tools/publicacoes.py   (não apaga DOI nem link já preenchidos à mão)"""
import re, json, sys, datetime, unicodedata, difflib, time, urllib.request, urllib.parse, os
ORCID = "0000-0003-3231-7515"
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_data", "publications.yml")
def get(u):
    r = urllib.request.Request(u, headers={"Accept": "application/json", "User-Agent": "site-publicacoes/1.0"})
    return json.load(urllib.request.urlopen(r, timeout=40))
def norm(s):
    s = unicodedata.normalize("NFKD", re.sub(r"<[^>]+>", "", s or "")).encode("ascii", "ignore").decode().lower()
    return " ".join(re.findall(r"[a-z0-9]+", s))
def sim(a, b):
    a, b = norm(a), norm(b)
    if not a or not b: return 0
    n = difflib.SequenceMatcher(None, a, b).ratio()
    return max(n, .95) if min(len(a), len(b)) > 45 and (a.startswith(b) or b.startswith(a)) else n
doi = lambda s: re.sub(r"^https?://(dx\.)?doi\.org/", "", s.strip(), flags=re.I).lower()
cand = []
for g in get(f"https://pub.orcid.org/v3.0/{ORCID}/works")["group"]:
    s = g["work-summary"][0]; d = [e["external-id-value"] for e in g["external-ids"]["external-id"] if e["external-id-type"] == "doi"]
    y = ((s.get("publication-date") or {}).get("year") or {}).get("value")
    if d: cand.append((s["title"]["title"]["value"], int(y or 0), doi(d[0]), "ORCID"))
cit, ot = {}, []
for r in get(f"https://api.openalex.org/works?filter=author.orcid:{ORCID}&per-page=200&select=doi,title,publication_year,cited_by_count")["results"]:
    if r["doi"]:
        d = doi(r["doi"]); cit[d] = r["cited_by_count"]; cand.append((r["title"], r["publication_year"], d, "OpenAlex"))
txt = open(F, encoding="utf-8").read(); blocks = re.split(r"(?m)^(?=- title:)", txt)
today = datetime.date.today().isoformat(); miss = []; log = []
for k, b in enumerate(blocks):
    if not b.startswith("- title:"): continue
    t = json.loads(re.match(r"- title: (.*)", b)[1]); y = int(re.search(r"year: (\d+)", b)[1])
    m = re.search(r"(?m)^  doi: (.+)$", b); d = doi(m[1].strip('"')) if m and "TODO" not in m[1] else None
    if not d:
        c = sorted(((sim(t, x[0]), x) for x in cand if abs(x[1]-y) <= 2), key=lambda z: (round(z[0],2), z[1][3] == "ORCID"), reverse=True)
        if c and c[0][0] >= .88: d = c[0][1][2]; log.append((c[0][0], c[0][1][3], t, c[0][1][0], y, c[0][1][1]))
    if not d:
        try:
            v = get("https://api.crossref.org/works?rows=3&query.bibliographic=" + urllib.parse.quote(t))["message"]["items"]; time.sleep(.3)
            for i in v:
                yy = i.get("issued", {}).get("date-parts", [[0]])[0][0] or 0
                fam = " ".join(norm(a.get("family", "")) for a in i.get("author", []))
                if sim(t, (i.get("title") or [""])[0]) >= .92 and abs(yy-y) <= 2 and ("limongi" in fam or "coelho" in fam):
                    d = doi(i["DOI"]); log.append((sim(t, i["title"][0]), "Crossref", t, i["title"][0], y, yy)); break
        except Exception as e: print("crossref", e)
    if not d: miss.append(t); continue
    if d not in cit:
        try: cit[d] = get("https://api.openalex.org/works/doi:" + urllib.parse.quote(d) + "?select=cited_by_count")["cited_by_count"]
        except Exception: pass
    b = re.sub(r"(?m)^  (doi|citations|citations_date): .*\n", "", b)
    add = f'  doi: "{d}"\n' + (f'  citations: {cit[d]}\n  citations_date: {today}\n' if d in cit else "")
    blocks[k] = b.rstrip("\n") + "\n" + add
open(F, "w", encoding="utf-8").write("".join(blocks))
n = len(blocks)-1
print(f"{n-len(miss)} de {n} com DOI; sem DOI:"); [print(" -", t) for t in miss]
if "-v" in sys.argv:
    for l in sorted(log): 
        if l[0] < .99 or l[4] != l[5]: print(l)
