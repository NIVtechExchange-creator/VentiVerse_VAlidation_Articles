# Two-compartment passive lung, pressure control 15 above PEEP 5, Ti 1 s, RR 15, 10 breaths.
import numpy as np, time, json
from scipy.integrate import solve_ivp
R=np.array([10.,20.]); C=np.array([0.025,0.025]); PS=15.; Ti=1.0; T=4.0; NB=10
tr=0.10; tf=0.15
def f(t,y,on):
    V1,V2,P=y; Pc=PS if on else 0.0
    tau=tr if Pc>=P else tf
    return [(P-V1/C[0])/R[0],(P-V2/C[1])/R[1],(Pc-P)/tau]
def euler(dt,rk4=False):
    y=np.zeros(3); ev=0; out=[]
    n=int(round(T/dt))
    for b in range(NB):
        for i in range(n):
            t=i*dt; on=t<Ti-1e-12
            if rk4:
                k1=np.array(f(t,y,on));k2=np.array(f(t,y+dt/2*k1,on));k3=np.array(f(t,y+dt/2*k2,on));k4=np.array(f(t,y+dt*k3,on));y=y+dt/6*(k1+2*k2+2*k3+k4);ev+=4
            else:
                y=y+dt*np.array(f(t,y,on));ev+=1
            if b==NB-1: out.append((t+dt,y[0]+y[1]))
    return np.array(out),ev
def adaptive(method,rtol,atol):
    y=np.zeros(3);ev=0;sol_last=[]
    for b in range(NB):
        for (a,c,on) in [(0,Ti,True),(Ti,T,False)]:
            s=solve_ivp(f,(a,c),y,method=method,rtol=rtol,atol=atol,args=(on,),dense_output=True)
            ev+=s.nfev; y=s.y[:,-1]
            if b==NB-1: sol_last.append((a,c,s.sol))
    return sol_last,ev
ref,_=adaptive('DOP853',1e-12,1e-14)
tt=np.arange(1,201)*0.02
def refV(t):
    for a,c,s in ref:
        if a-1e-12<=t<=c+1e-12: y=s(t); return y[0]+y[1]
Vref=np.array([refV(t) for t in tt])
Vt=Vref.max()
res={}
def err_fixed(out):
    vv=np.interp(tt,out[:,0],out[:,1]); return float(np.max(np.abs(vv-Vref))/Vt*100)
for name,dt,rk in [('Euler',0.0005,0),('Euler',0.001,0),('Euler',0.002,0),('Euler',0.005,0),('Euler',0.01,0),('Euler',0.02,0),('RK4',0.002,1),('RK4',0.01,1),('RK4',0.02,1)]:
    t0=time.perf_counter();out,ev=euler(dt,rk);w=time.perf_counter()-t0
    res[f'{name}_{dt}']=dict(err=err_fixed(out),nfev=ev,wall=w)
for m,rt in [('RK45',1e-3),('RK45',1e-6),('LSODA',1e-3),('BDF',1e-3),('Radau',1e-3)]:
    t0=time.perf_counter();sl,ev=adaptive(m,rt,1e-6);w=time.perf_counter()-t0
    vv=[]
    for t in tt:
        for a,c,s in sl:
            if a-1e-12<=t<=c+1e-12: y=s(t);vv.append(y[0]+y[1]);break
    res[f'{m}_{rt}']=dict(err=float(np.max(np.abs(np.array(vv)-Vref))/Vt*100),nfev=ev,wall=w)
res['VT_mL']=Vt*1000
json.dump(res,open('/home/ubuntu/book/tools/ch04_bench.json','w'),indent=1)
for k,v in res.items(): print(k,v)
