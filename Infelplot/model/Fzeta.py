from math import e,sqrt,log10
import numpy as np
import base64
from statistics import stdev
class Fzeta():
    def __init__(self,muestra,analista,date,edad,error,rhod,nd,uds,ns,ni,ng):
        self.muestra=muestra
        self.analista=analista
        self.date=date
        self.edad=edad
        self.errori=error
        self.rhod=rhod
        self.nd=nd
        self.uds=uds
        self.ns=ns
        self.ni=ni
        self.ng=ng
        self.rhos=[]
        self.rhoi=[]
        self.divrho=[]
        self.zeta=[]
        self.error=[]
        self.k=[]
        self.nsexpected=[]
        self.niexpected=[]
        self.chifactor=[]
        self.m=[]
        self.y=[]
        self.z=[]
        self.w=[]
        self.size=None
        self.sumni=None
        self.sumns=None
        self.zpooled=None
        self.erzpo=None
        self.zmean=None
        self.erzme=None
        self.centralz=None
        self.chi_squared=None
        self.ercentral=None
        self.posrr=None
    def begin(self):
        self.size=len(self.ns)
        self.sumni=sum(self.ni)
        self.sumns=sum(self.ns)
        self.rhoj()
        eta,sumw,sigma=self.iteraciones()
        self.zpooled=self.zetaf(self.sumns,self.sumni)
        self.zmean=self.zetaf(np.mean(self.divrho),1)
        self.centralz=self.zetaf(eta,(1-eta))
        self.errorzpooled()
        self.erzme=stdev(self.zeta)
        self.chi_squared=sum(self.chifactor)
        v=1/((eta**2)*((1-eta)**2)*sumw)
        self.ercentralf(v)
        self.posrr=sigma*100
        d=str(self.writeout())[2:-1]
        return d

    def writeout(self):
        cabeza1='CALIBRATION ZETA\n'+'Sample:;;'+str(self.muestra)+'\nAnalyst:;;'+str(self.analista)+'\nDate:;;'+str(self.date)+'\nAge +- Error:;;'+str(self.edad)+';'+str(self.errori)
        cabeza2='\nRhod:;;'+str(self.rhod)+';10^5 traces/cm^2\nNd:;;'+str(self.nd)+'\nUnit Area:;;'+str(self.uds)+';10^-6 cm^2'
        cabeza=cabeza1+cabeza2
        cuerpo='\nNs;Ni;Ng;Rhos;Rhoi;Rhos/Rhoi;Zeta:;Error;;(Rhos/Rhoi)^2;Ns (expected);Ni (expected);Chi Factor;m;y;z'
        for i in range(self.size):
            cuerpo=cuerpo+'\n'+str(self.ns[i])+';'+str(self.ni[i])+';'+str(self.ng[i])+';'+str(self.rhos[i])+';'+str(self.rhoi[i])+';'+str(self.divrho[i])+';'+str(self.zeta[i])+';'+str(self.error[i])+';;'+str(self.divrho[i])+';'+str(self.nsexpected[i])+';'+str(self.niexpected[i])+';'+str(self.chifactor[i])+';'+str(self.m[i])+';'+str(self.y[i])+';'+str(self.z[i])
        pie = '\n\nPooled Zeta:;'+str(self.zpooled)+';'+str(self.erzpo)+'\nMean Zeta:;'+str(self.zmean)+';'+str(self.erzme)+'\nCentral Zeta:;'+str(self.centralz)+';'+str(self.ercentral)+';'+str(self.posrr)+';%\nChi-Squared:;'+str(self.chi_squared)
        doc = str(cabeza+cuerpo+pie).replace('.',',')
        base = base64.b64encode(bytes(doc, 'utf-8'))
        return base
    def rhoj(self):
        #rhos= ns/(ng*uds)
        #rhoi= ni/(ng*uds)
        #z=ecuacion
        for i in range(self.size):
            ns=self.ns[i]
            ni=self.ni[i]
            self.rhos.append(float("{0:.4f}".format(ns/(self.ng[i]*self.uds))))
            self.rhoi.append(float("{0:.4f}".format(ni/(self.ng[i]*self.uds))))
            self.divrho.append(float("{0:.8f}".format(self.rhos[-1]/self.rhoi[-1])))
            self.zeta.append(float("{0:.4f}".format(self.zetaf(ns,ni))))
            self.error.append(float("{0:.4f}".format(self.errorf(self.zeta[-1],ns,ni))))
            self.k.append(float("{0:.8f}".format(self.divrho[-1]**2)))
            self.nexpected(ns,ni)
            self.chifactor.append(float("{0:.8f}".format(self.chifactorf(ns,ni,self.nsexpected[-1],self.niexpected[-1]))))
            self.m.append(ns+ni)
            self.y.append(ns/self.m[-1])
            self.z.append(log10((ns+0.5)/(ni+0.5)))
        return 0

    def zetaf(self,ns,ni):
        la = 1.55125e-10 #LAMBDA_ALPHA
        numerador = e**(la*self.edad*1000000)-1
        denominador = la*(ns/ni)*self.rhod*0.5*100000
        return numerador/denominador

    def errorf(self,z,ns,ni):
        aux = (1/ns)+(1/ni)+(1/self.nd)+(self.errori/self.edad)**2
        return z*sqrt(aux)

    def nexpected(self,ns,ni):
        value=(ns+ni)/(self.sumns+self.sumni)
        self.nsexpected.append(float("{0:.8f}".format(value*self.sumns)))
        self.niexpected.append(float("{0:.8f}".format(value*self.sumni)))

    def chifactorf(self,ns,ni,nse,nie):
        v1=((ns-nse)**2)/nse
        v2=((ni-nie)**2)/nie
        return v1+v2

    def iteraciones(self):
        wv=[]
        wcv=[]
        wy=[]
        sigma=0.6*stdev(self.z)
        eta=sum(self.ns)/sum(self.m)
        for j in range(self.size):
            wv[:]=[]
            wcv[:]=[]
            wy[:]=[]
            for i in range(self.size):
                wv.append(self.wf(self.m[i],eta,sigma))
                wcv.append(self.wc(self.y[i],eta,wv[-1]))
                wy.append(self.y[i]*wv[-1])
            eta=sum(wy)/sum(wv)
            sigma=sigma*sqrt(sum(wcv)/sum(wv))
        return eta,sum(wv),sigma
    def wf(self,m,t,s):
        return m/(t*(1-t)+(m-1)*(t**2)*((1-t)**2)*(s**2))
    def wc(self,y,t,w):
        return (w**2)*((y-t)**2)
    def errorzpooled(self):
        value=(1/self.sumns)+(1/self.sumni)+(1/self.nd)+(self.errori/self.edad)**2
        self.erzpo = sqrt(value)*self.zpooled
    def ercentralf(self,value):
        v=value+(1/self.nd)+(self.errori/self.edad)**2
        self.ercentral = self.centralz*sqrt(v)
