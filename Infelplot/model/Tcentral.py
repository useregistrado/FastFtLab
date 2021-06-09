from math import log10,log
from Infelplot.model.stadistic_scripts import sq
import math
import numpy as np
class Tcentral():
    def __init__(self,ns,ni,z,rhod):
        self.ns=ns
        self.ni=ni
        self.z=z
        self.RHO_D=rhod
        self.LAMBDA_ALPHA=1.55125e-10
        self.G=0.5
        self.mi=[]
        self.zi=[]
        self.yi=[]
        self.sigeta=[[],[]]
        self.iterations=[]
        self.size=0
    def begin(self):
        self.size=len(self.ni)
        self.m()
        self.zf()
        self.y()
        self.begin_sigma_eta()
        #no cambiar el 1 el cero si es variable
        for i in range(0,self.size):
            self.iterationsf(self.sigeta[0][i],self.sigeta[1][i])
        return self.t_central()

    def zf(self):
        for i in range(0,self.size):
            frac = (self.ns[i]+0.5)/(self.ni[i]+0.5)
            self.zi.append(float("{0:.7f}".format(log10(frac))))

    def y(self):
        for i in range(0,self.size):
            self.yi.append(float("{0:.7f}".format(self.ns[i]/self.mi[i])))

    def m(self):
        for i in range(0,self.size):
            self.mi.append(self.ns[i]+self.ni[i])

    def begin_sigma_eta(self):
        self.sigeta[0].append(float("{0:.9f}".format(0.6*math.sqrt(np.var(self.zi,ddof=1)))))
        self.sigeta[1].append(float("{0:.7f}".format(sum(self.ns)/sum(self.mi))))

    def sigma_eta(self,wji,aji,wyji):
        sig_ultimo=self.sigeta[0][-1]
        self.sigeta[0].append(float("{0:.9f}".format(sig_ultimo*math.sqrt(sum(aji)/sum(wji)))))
        self.sigeta[1].append(float("{0:.7f}".format(sum(wyji)/sum(wji))))

    def iterationsf(self,sigma,eta):
        iteration=[[],[],[]]

        for i in range(0,self.size):
            #Acontinuacion el calculo para Wji
            denominator=(eta-eta**2)+(self.mi[i]-1)*(eta**2)*((1-eta)**2)*(sigma**2)
            wji=float("{0:.7f}".format(self.mi[i]/denominator))
            iteration[0].append(wji)
            #Finalizacion del calculo de Wji y posterior agregacion a la matriz
            #Acontinuacion el calculo para Aji
            aji=float("{0:.7f}".format((wji**2)*(self.yi[i]-eta)**2))
            iteration[1].append(aji)
            #Finalizacion del calculo de aji y posterior agregacion a la matriz

            #Acontinuacion el calculo para wyji
            wyji=float("{0:.7f}".format(wji*self.yi[i]))
            iteration[2].append(wyji)
            #Finalizacion del calculo de wyji y posterior agregacion a la matriz

        self.iterations.append(iteration)
        self.sigma_eta(wji=iteration[0],aji=iteration[1],wyji=iteration[2])
    def t_central(self):
        etaf=self.sigeta[1][-1]
        ln=self.LAMBDA_ALPHA*(etaf/(1-etaf))*self.G*self.z*self.RHO_D+1
        self.params_error()
        return float("{0:.8f}".format((1/self.LAMBDA_ALPHA)*log(ln)/1e+6))

    def params_error(self):
        #funcion que obtendra los parametros para calcular el error
        etaf=self.sigeta[1][-1]
        wf=self.iterations[-1][0]
        return etaf, sum(wf)
