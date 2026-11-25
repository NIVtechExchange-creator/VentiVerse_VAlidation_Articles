import re,json,unicodedata
md=open('/home/ubuntu/vv/article/article_v69.md').read()
refs=md.split('## References',1)[1]
items={}
for line in refs.split('\n'):
    m=re.match(r'^(\d+)\.\s+(.*)',line.strip())
    if m: items[int(m.group(1))]=m.group(2).strip()
bib=open('/home/ubuntu/book/references.bib').read()
exist={}
for m in re.finditer(r'@\w+\{([^,]+),\s*author=\{([^}]*)\}.*?year=\{(\d{4})\}',bib,re.S):
    sur=m.group(2).split(',')[0].strip().lower(); exist[(strip:=unicodedata.normalize('NFKD',sur).encode('ascii','ignore').decode(),m.group(3))]=m.group(1)
def asc(s): return unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
def tex(s):
    s=s.replace('&','\\&').replace('%','\\%').replace('_','\\_').replace('#','\\#')
    s=re.sub(r'\*([^*]+)\*',r'\1',s)
    rep={'₂':'\\textsubscript{2}','₃':'\\textsubscript{3}','⁻':'\\textsuperscript{-}','−':'--','–':'--','—':'---','→':'$\\rightarrow$','≥':'$\\geq$','≤':'$\\leq$','±':'$\\pm$','×':'$\\times$','α':'$\\alpha$','β':'$\\beta$','μ':'$\\mu$','~':'$\\sim$','̇':''}
    for k,v in rep.items(): s=s.replace(k,v)
    return s
out=[];mp={};used=set(re.findall(r'@\w+\{([^,]+),',bib))
for n,r in sorted(items.items()):
    r0=re.sub(r'\s*\((?![^)]*\d{4};)[^)]*\)\s*$','',r)  # drop trailing annotation
    r0=re.sub(r'\s*doi:\S+','',r0).strip()
    ym=re.search(r'(19|20)\d{2}',r0); yr=ym.group(0) if ym else 'nd'
    sur=asc(re.split(r'[ ,]',r0.strip())[0]).lower()
    sur=re.sub(r'[^a-z]','',sur) or 'anon'
    if (sur,yr) in exist: mp[n]=exist[(sur,yr)]; continue
    k=sur+yr; base=k; i=0
    while k in used: i+=1; k=base+'abcdefghij'[i-1]
    used.add(k); mp[n]=k
    # split authors. title. rest
    parts=re.split(r'(?<=[a-z\)\]A-Z])\.\s+',r0,maxsplit=2)
    if len(parts)>=3: au,ti,rest=parts
    else: au,ti,rest=parts[0],'',' '.join(parts[1:])
    out.append('@misc{%s,author={%s},title={%s},note={%s},year={%s}}'%(k,tex(au).replace(', ',' and ') if 'eds' not in au else tex(au),tex(ti),tex(rest),yr))
open('/home/ubuntu/book/refs_article.bib','w').write('\n'.join(out)+'\n')
json.dump(mp,open('/home/ubuntu/book/tools/artrefmap.json','w'))
print(len(items),'refs',len(out),'new',len(items)-len(out),'reused')
