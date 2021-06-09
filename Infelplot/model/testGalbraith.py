from scipy.stats import chi2
def test(ns,ni,dn,a):
    num= [n**2 for n in dif(ns,ni)]
    chi2s=div(num,ni)
    num= [n**2 for n in dif(dn,a)]
    chi2i= div(num,a)
    chi2galb=sum(chi2i)+sum(chi2s)
    chiv= chi2.ppf(0.95,len(ns)-1)
    porc=(chi2galb*100)/chiv
    k=None
    if chi2galb<=chiv:
        k="PASS!"
    else:
        k="FAIL!"
    return "Prob.: "+"{0:.4f}".format(chi2galb)+" Prob.(%): "+"{0:.4f}".format(porc)+" Response: "+k
def dif(a,b):
    dif=[]
    for i in range(0,len(a)):
        dif.append(a[i]-b[i])
    return dif
def div(a,b):
    div=[]
    for i in range(0,len(a)):
        div.append(a[i]/b[i])
    return div

def ffrecx2(ns,ni):
    n=[ns[i]+ni[i] for i in range(0,len(ns))]
    Ns,Ni = sum(ns),sum(ni)
    N=Ns+Ni
    num=[Ns*n[i] for i in range(len(n))]
    fps=[num[i]/N for i in range(0,len(num))]
    num=[Ni*n[i] for i in range(len(n))]
    fpi=[num[i]/N for i in range(0,len(num))]
    return test(ns,fps,ni,fpi)
