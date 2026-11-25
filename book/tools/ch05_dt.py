import pandas as pd, json, io, sys
D='/home/ubuntu/vv/blind_dt/'
def load(sid):
    fn=D+sid+'.csv'; hdr=[]; st=None
    with open(fn) as f:
        for i,l in enumerate(f):
            if l.startswith('# Breath_table'): bt=int(l.split('skiprows=')[1].split(';')[0]); bn=int(l.split('nrows=')[1].split(')')[0])
            if l.startswith('# SETTINGS_JSON'): st=json.loads(l.split('SETTINGS_JSON',1)[1]); break
    b=pd.read_csv(fn,skiprows=bt,nrows=bn)
    b=b[b.Start_s>=1800]
    w=b.Duration_s
    m=lambda c:(b[c]*w).sum()/w.sum()
    vco2=float(st['vo2'])*float(st['rer'])
    co2out=((b.VA_Lmin*b.PaCO2_mmHg/0.863)*w).sum()/w.sum()
    return dict(PaCO2=m('PaCO2_mmHg'),PaO2=m('PaO2_mmHg'),SaO2=m('SaO2_pct'),VT=b.VT_mL.median(),RR=len(b)/(w.sum()/60),VE=m('VE_Lmin'),Pmus=b.Pmus_cmH2O.median(),AutoPEEP=m('AutoPEEP_cmH2O'),CO2bal=100*(co2out/vco2-1))
R={s:load(s) for s in sys.argv[1:]}
json.dump(R,open('/home/ubuntu/book/tools/ch05_dt.json','w'),indent=1)
for k,v in R.items(): print(k,{a:round(x,2) for a,x in v.items()})
