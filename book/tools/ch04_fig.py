import json
r=json.load(open('tools/ch04_bench.json'))
e=[(float(k.split('_')[1])*1000,v['err']) for k,v in r.items() if k.startswith('Euler_')]
k4=[(float(k.split('_')[1])*1000,v['err']) for k,v in r.items() if k.startswith('RK4_')]
s=r"""\begin{tikzpicture}
\begin{loglogaxis}[width=0.8\linewidth,height=6.2cm,xlabel={Step size $\Delta t$ (ms)},ylabel={Max.\ volume error (PCT of $V_T$)},
 grid=major,grid style={gray!20},legend pos=south west,legend style={font=\small,draw=none,fill=none},ymin=1e-8,ymax=5,xtick={0.5,1,2,5,10,20},xticklabels={0.5,1,2,5,10,20}]
\addplot[bkblue,thick,mark=*] coordinates {EUL};
\addlegendentry{explicit Euler}
\addplot[bkorange,thick,mark=square*] coordinates {RKC};
\addlegendentry{classical RK4}
\addplot[gray,dashed,domain=0.5:20] {0.25*x};
\addlegendentry{reference slope 1}
\addplot[gray,dotted,thick,domain=2:20] {1.0e-7*(x/2)^4};
\addlegendentry{reference slope 4}
\draw[red!70!black,thick] (axis cs:2,1e-8) -- (axis cs:2,5);
\node[red!70!black,font=\scriptsize,anchor=west] at (axis cs:2.1,1.5) {VentiVerse step};
\end{loglogaxis}
\end{tikzpicture}
"""
s=s.replace('PCT','\\%').replace('EUL',' '.join('(%g,%.5g)'%p for p in sorted(e))).replace('RKC',' '.join('(%g,%.5g)'%p for p in sorted(k4)))
open('figures/gen/ch04_conv.tex','w').write(s)
def row(lbl,key,step):
    v=r[key]; err=v['err']
    if err>=1e-3: es='%.2g'%err
    else:
        m,ex=('%.1e'%err).split('e'); es='$%s\\times10^{%d}$'%(m,int(ex))
    return "%s & %s & %s & %d \\\\\n"%(lbl,step,es,v['nfev'])
t=""
for lbl,key,step in [("Explicit Euler (\\texttt{ode1})","Euler_0.002","fixed, \\SI{2}{\\milli\\second}"),
("Explicit Euler (\\texttt{ode1})","Euler_0.01","fixed, \\SI{10}{\\milli\\second}"),
("Classical RK4 (\\texttt{ode4})","RK4_0.002","fixed, \\SI{2}{\\milli\\second}"),
("Classical RK4 (\\texttt{ode4})","RK4_0.01","fixed, \\SI{10}{\\milli\\second}"),
("Dormand--Prince (\\texttt{ode45}), rtol $10^{-3}$","RK45_0.001","variable"),
("Dormand--Prince (\\texttt{ode45}), rtol $10^{-6}$","RK45_1e-06","variable"),
("LSODA (Adams/BDF switching), rtol $10^{-3}$","LSODA_0.001","variable"),
("BDF, as in \\texttt{ode15s}, rtol $10^{-3}$","BDF_0.001","variable"),
("Radau IIA (implicit), rtol $10^{-3}$","Radau_0.001","variable")]:
    t+=row(lbl,key,step)
open('figures/gen/ch04_tab.tex','w').write(t)
