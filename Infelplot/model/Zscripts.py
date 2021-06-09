from math import e
import Infelplot.model.stadistic_scripts as sts
class Zscripts():

    def __init__(self,ns,ni,t,rhod):
        #constantes
        self.LAMBDA_ALPHA=1.55125e-10
        self.RHO_D=rhod
        self.G=0.5

        #datos de entrada
        self.ni=ni
        self.ns=ns
        self.t=t

        #datos de salida
        self.z=0

    def zc(self):
        zs=[]
        def calculate(self,n):
            return ((e**(self.LAMBDA_ALPHA*self.t)-1)/(self.LAMBDA_ALPHA*n*self.RHO_D*self.G))*1e+6
        for i in range(len(self.ns)):
            n=self.ns[i]/self.ni[i]
            zs.append(calculate(self,n))
        return float("{0:.2f}".format(sts.media(zs)))
