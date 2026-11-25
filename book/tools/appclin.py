import re,json
B='/home/ubuntu/book/'
src=open(B+'notes/src_appA.md').read()
amap=json.load(open(B+'tools/artrefmap.json'))
P=json.load(open(B+'tools/phenotypes.json'))
abgseg=open(B+'notes/code_phenoabg.js').read()
ABG={n:(a,b,c) for n,a,b,c in re.findall(r'"([^"]+)"\s*:\s*\{paCO2:([\d.]+),sao2:([\d.]+),hco3:([\d.]+)\}',abgseg[abgseg.find('Adult:{'):])}
PROG=set(['Tracheobronchomalacia','Excessive dynamic airway collapse (EDAC)','Tracheobronchomalacia with COPD','Cystic fibrosis, hypercapnic respiratory failure','Tracheal stenosis (fixed)','SCI C1–C2 complete (no diaphragm)','SCI C3–C4 complete','SCI C5 complete','SCI C6–C8 complete','SCI C4 incomplete','Guillain-Barré (respiratory involvement)','ALS: limb onset','ALS: bulbar onset','ALS / motor neuron disease','Adult DMD / NMD','COPD / emphysema, stable hypercapnic','COPD / chronic bronchitis, stable hypercapnic','COPD / OSA overlap syndrome'])
MAP={'A.2.1':[('Adult','ALS / motor neuron disease')],'A.2.2':[('Adult','Adult DMD / NMD')],'A.2.3':[('Adult','Myasthenia gravis (MG crisis)')],'A.2.4':[('Adult','Guillain-Barré (respiratory involvement)')],'A.2.5':[('Adult','SCI C3–C4 complete')],'A.3.1':[('Adult','COPD exacerbation (AECOPD)')],'A.3.2':[('Adult','Status asthmaticus (intubated)')],'A.3.3':[('Adult','COPD / expiratory flow limitation (EFL), intrinsic PEEP')],'A.4.1':[('Adult','ARDS (moderate — P/F 100–200)')],'A.4.2':[('Adult','ARDS (severe — P/F <100)')],'A.4.3':[('Adult','Obese ARDS (BMI 40 — P/F 120)')],'A.4.4':[('Adult','Post-op abdominal / laparotomy')],'A.4.5':[('Adult','Pulmonary fibrosis (IPF)')],'A.5.1':[('Adult','Obesity hypoventilation (OHS)')],'A.5.2':[('Adult','OHS + obstructive lung disease')],'A.6.1':[('Infant','SMA type 1')],'A.6.2':[('Infant','RSV bronchiolitis')],'A.6.3':[('Preterm','RDS'),('Neonate','RDS')],'A.6.4':[('Neonate','BPD (bronchopulmonary dysplasia)')],'A.6.5':[('Neonate','Meconium aspiration (MAS)')],'A.6.6':[('Neonate','Pulm. hypertension (PPHN)')],'A.6.7':[('Neonate','Congenital diaphragmatic hernia (CDH)')],'A.6.8':[('Child','Acute severe asthma')],'A.6.9':[('Child','Cystic fibrosis (CF, moderate)')],'A.6.10':[('Neonate','Neonatal pneumonia / GBS sepsis')]}
def tags(n):
    t=lambda p:bool(re.search(p,n,re.I))
    return dict(obstructive=t(r'copd|asthm|bpd|bronch|rsv|cf\b|cystic|pertuss|obliter|aecopd|malacia|efl|edac'),secretion=t(r'aecopd|exac|pneumon|cf\b|cystic|pertuss|rsv|meconi|neonat.*pneum|bronchitis|efl'),nm=t(r'als|nmd|dmd|myasthenia|mg\b|mg cr|guillain|spinal cord|sma\b|sma type|diaphragm para'),infl=t(r'ards|pneumon|asthm|aecopd|rds\b|meconi'),atel=t(r'ards|pneumon|post.op|laparot|ohs|obesity|rds\b|cdh'),asthma=t('asthm'),cfb=t(r'cf\b|cystic|bronchiect'),rds=t(r'rds\b|ards|mas\b|cdh|meconi'),pphn=t(r'pphn|pulm.*hypert|ards|cdh'),croup=t(r'croup|laryn|subglot|stenosis|post.ext'),mg=t(r'myasthen|mg cr'),tx=t('after lung transplant'))
def scales(n):
    g=tags(n)
    S={'neostigmine':1 if g['mg'] else 0,'pyridostigmine':1 if g['mg'] else 0,
    'SABA':0 if g['tx'] else (1 if g['obstructive'] else .15 if g['infl'] else 0),'LABA':0 if g['tx'] else (1 if g['obstructive'] else 0),'ipratropium':0 if g['tx'] else (1 if g['obstructive'] else 0),
    'MgSO$_4$':1 if g['asthma'] else .3 if g['obstructive'] else 0,'corticosteroids':1 if (g['obstructive'] or g['infl']) else 0,'racemic epinephrine':1 if g['croup'] else .15 if g['obstructive'] else 0,
    'surfactant':1 if g['rds'] else .4 if g['atel'] else 0,'inhaled NO':1 if g['pphn'] else .3 if g['infl'] else 0,'hypertonic saline':1 if g['cfb'] else .7 if g['secretion'] else 0,
    'N-acetylcysteine':1 if g['cfb'] else .7 if g['secretion'] else .4 if g['obstructive'] else 0,'dornase alfa':1 if g['cfb'] else .3 if g['secretion'] else 0,'inhaled antibiotics':1 if g['cfb'] else .5 if g['secretion'] else 0,
    'HFCWO':1 if g['secretion'] else .5 if g['nm'] else .2,'insufflation--exsufflation':1 if g['nm'] else .6 if g['secretion'] else .15,'prone position':1 if g['atel'] else 0}
    return S
U={'₂':r'\textsubscript{2}','₃':r'\textsubscript{3}','₄':r'\textsubscript{4}','⁻':r'\textsuperscript{$-$}','—':'---','–':'--','×':r'$\times$','→':r'$\to$','κ':r'$\kappa$','≥':r'$\geq$','≤':r'$\leq$','≈':r'$\approx$','↓':r'$\downarrow$','↑':r'$\uparrow$','τ':r'$\tau$','Δ':r'$\Delta$','·':r'$\cdot$','§':r'\S{}','°':r'\textdegree{}','±':r'$\pm$','β':r'$\beta$'}
def cites(m):
    ks=[]
    for part in m.group(1).split(','):
        part=part.strip()
        r=re.match(r'(\d+)\s*[–-]\s*(\d+)$',part)
        nums=range(int(r.group(1)),int(r.group(2))+1) if r else [int(part)]
        for x in nums:
            k=amap.get(str(x))
            if k and k not in ks: ks.append(k)
    return r'~\citep{%s}'%','.join(ks) if ks else ''
def conv(x):
    x=re.sub(r'\b(?:Clung|Cl|Ccw|Pmax|pmax|Raw|R)\s*[↓↑]?\s*×\s*[\d.]+\s*[,;]?\s*','',x)
    x=re.sub(r'\b(?:shuntFrac|lowVQFrac|shunt|lowVQ)\s*=?\s*0\.\d+\s*[,;]?\s*','',x)
    x=re.sub(r',?\s*κ\s*=\s*[\d.]+','',x)
    x=re.sub(r'\(\s*\)','',x); x=re.sub(r':\s*\.',':',x)
    x=re.sub(r'\s*\[(\d+(?:\s*[,–-]\s*\d+)*)\]',cites,x)
    x=re.sub(r'\s*\([^()]*(?:pmax|Pmax|Ccw|Cl\b|shunt ?[\d×]|lowVQ|\bdg\b|\bfg\b|×\s*0\.)[^()]*\)','',x)
    x=x.replace('&',r'\&').replace('%',r'\%').replace('#',r'\#')
    x=re.sub(r'(?<![\\$])<',r'$<$',x); x=re.sub(r'(?<![\\$])>',r'$>$',x)
    x=re.sub(r'\*\*(.+?)\*\*',r'\\textbf{\1}',x); x=re.sub(r'\*(.+?)\*',r'\\emph{\1}',x)
    x=x.replace('"',"''")
    for a,b in U.items(): x=x.replace(a,b)
    x=x.replace('paediatric','pediatric').replace('Paediatric','Pediatric').replace('oedema','edema').replace('haem','hem').replace('oe','e') if False else x
    for a,b in [('Paediatric','Pediatric'),('paediatric','pediatric'),('oedema','edema'),('haemo','hemo'),('anaem','anem'),('hypoxaem','hypoxem'),('hypercapnoea','hypercapnia'),('dyspnoea','dyspnea'),('apnoea','apnea'),('orthopnoea','orthopnea'),('Orthopnoea','Orthopnea'),('tachypnoea','tachypnea'),('Dyspnoea','Dyspnea'),('normalise','normalize'),('minimise','minimize'),('optimis','optimiz'),('recognis','recogniz'),('centre','center'),('colour','color'),('litre','liter'),('sialorrhoea','sialorrhea'),('oesophag','esophag'),('fibre','fiber'),('behaviour','behavior'),('parameterised','parameterized'),('modelled','modeled'),('modelling','modeling')]: x=x.replace(a,b)
    return x
def model(sec):
    out=[]
    for cat,name in MAP.get(sec,[]):
        p=P[cat].get(name)
        if not p: out.append('%%missing %s'%name); continue
        e=p.get('extra') or {}
        bits=[]
        for k,lab in [('R','airway resistance'),('Cl','lung compliance'),('Ccw','chest-wall compliance'),('pmax','maximal inspiratory pressure')]:
            v=p.get(k)
            if v is not None and abs(v-1)>1e-9: bits.append('%s $\\times%g$'%(lab,v))
        if e.get('shuntFrac'): bits.append('shunt %g\\%%'%(100*e['shuntFrac']))
        if e.get('lowVQFrac'): bits.append('low-$\\dot V/\\dot Q$ fraction %g\\%%'%(100*e['lowVQFrac']))
        if p.get('sf') is not None: bits.append('slow fraction %g with $\\kappa=%g$'%(p['sf'],p.get('tc',1)))
        if p.get('dg') not in (None,1): bits.append('drive gain multiplier %g'%p['dg'])
        s='\\textbf{Model representation.} %s phenotype ``%s'"'"': %s.'%(cat,conv(name),'; '.join(bits) if bits else 'baseline mechanics')
        if cat=='Adult' and name in ABG:
            a=ABG[name]; s+=' Untreated seed: PaCO\\textsubscript{2} %s mmHg, SaO\\textsubscript{2} %s\\%%, HCO\\textsubscript{3}\\textsuperscript{$-$} %s mEq/L.'%a
        if name in PROG: s+=' A months-since-onset progression time line is available.'
        S=scales(name); full=[k for k,v in S.items() if v>=1]; part=['%s (%g)'%(k,v) for k,v in S.items() if 0<v<1]
        s+=' Adjuncts at full effectiveness: %s.'%(', '.join(full) if full else 'none')
        if part: s+=' Partial: %s.'%', '.join(part)
        out.append(s)
    return '\n\n'.join(out)
L=[r'\chapter{Clinical Pathology Reference}',r'\label{app:clin}','',
r'This appendix summarizes, for each phenotype that commonly needs ventilatory support, the mechanism of failure, the presentation, the ventilation strategy and the adjunct treatments reported in the literature. Each entry ends with the phenotype as it is implemented: the parameter changes of \cref{sec:par-lib}, the untreated blood gas of \cref{tab:par-abg} for adults, and the adjuncts of \cref{tab:adj-defs} that the model applies to that phenotype, with their effectiveness. Clinical recommendations are summaries of the cited literature, not treatment guidance.','']
parts=re.split(r'\n(?=#{3,4} A\.)',src)
for p in parts:
    h=p.split('\n',1)[0]; body=p.split('\n',1)[1] if '\n' in p else ''
    m=re.match(r'(#{3,4}) (A\.[\d.]+) (.*)',h)
    if not m: continue
    lev,sec,title=m.groups()
    if sec in ('A.1','A.7','A.5.3'): continue
    L.append(('\\section{%s}' if lev=='###' else '\\subsection{%s}')%conv(title.strip()))
    paras=[x.strip() for x in body.split('\n') if x.strip() and x.strip()!='---']
    for x in paras:
        if re.match(r'\*\*Simulator (capability|gaps)',x): continue
        if x.startswith('|'): continue
        L.append(conv(x)); L.append('')
    if lev=='####': L.append(model(sec)); L.append('')
open(B+'backmatter/appClin.tex','w').write('\n'.join(L))
print(len(L),'lines', sum(1 for x in L if x.startswith('%missing')))
