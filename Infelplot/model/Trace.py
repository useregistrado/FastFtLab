from math import log, sqrt
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') #para evitar que se apague el servidor
import Infelplot.model.stadistic_scripts as sts
from Infelplot.model.Tcentral import Tcentral
import statistics as sttcs
from scipy import stats
import numpy as np
from io import BytesIO
import base64
class Trace():

    def __init__(self,ns,ni,z,rhod,nd,zetaerr):
        #constantes
        self.LAMBDA_ALPHA=1.55125e-10
        self.RHO_D=rhod
        self.G=0.5

        #datos de entrada
        self.ni=ni
        self.ns=ns

        #datos de salida
        self.ages=[]
        self.t_pooled = 0
        self.t_isocrona = 0
        self.t_mean = 0
        self.tcentral = 0
        self.m=0
        self.a=0
        self.b=0
        #variables
        self.z=z
        self.zetaerr=zetaerr
        self.sumation_ns=0
        self.sumation_ni=0
        self.rho_i=0
        self.size=0
        self.nd=nd
        self.eta=0
        self.sumw=0
        self.centralerror=0
        self.poolederror=0
    def begin(self): #Esta funcion inicializa los valores de las sumatorias de ns y ni y calcula el tamaño de los datos de entrada
        self.summation()
        self.c_rho_i()
        self.size=len(self.ni)
        self.t_single()
        self.t_meanf()
        self.t_pooledf()
        self.m = sts.regression(self.ni,self.ns)
        self.a,self.b = sts.regression_b(self.ni,self.ns)
        self.t_isocronaf()
        self.t_central()
        self.get_errors()
        
    def histograma(self):
        m=sttcs.mean(self.ages)
        s=sttcs.stdev(self.ages)
        dist = stats.norm(m,s)
        x = np.linspace(dist.ppf(0.001),dist.ppf(0.999), 100)
        plt.hist(self.ages,bins=5,edgecolor = 'black', color='#4040ff', density=True, label="Ages")
        plt.plot(x, dist.pdf(x), "r-", label="Pdf",color="#40ff40")
        plt.legend()
        plt.xlabel('Millions of years')
        tmpfile=BytesIO()
        plt.savefig(tmpfile,format="png")
        encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
        plt.close()
        return encoded


    def c_rho_i(self):#rho_i se definio como la suma de los ns sobre la suma de los ni
        self.rho_i = self.sumation_ns/self.sumation_ni

    def rho_s(ns,area):
        return summation(ns)/area

    def summation(self): #calcula la sumatoria de los ns y los ni
        sumi,sums=0,0
        for i in self.ns:
            sums=sums+i
        for i in self.ni:
            sumi=sumi+i
        self.sumation_ni, self.sumation_ns=sumi,sums


    def t_single(self): #calcula las edades individuales
        def calculate(self,ni,ns):
            ln=self.LAMBDA_ALPHA*(ns/ni)*self.G*self.z*self.RHO_D+1
            return float("{0:.8f}".format((1/self.LAMBDA_ALPHA)*log(ln)/1e+6))

        for n in range(self.size):
            self.ages.append(calculate(self,self.ni[n],self.ns[n])) #agrega las edades individuales a la lista ages

    def t_pooledf(self):
        ln=self.LAMBDA_ALPHA*(self.sumation_ns/self.sumation_ni)*self.G*self.z*self.RHO_D+1
        self.t_pooled = float("{0:.4f}".format((1/self.LAMBDA_ALPHA)*log(ln)/1e+6))

    def t_isocronaf(self):
        ln=self.LAMBDA_ALPHA*(self.m)*self.G*self.z*self.RHO_D+1
        self.t_isocrona = float("{0:.4f}".format((1/self.LAMBDA_ALPHA)*log(ln)/1e+6))

    def t_meanf(self):
        self.t_mean = float("{0:.4f}".format(sts.media(self.ages)))

    def t_central(self):
        tc=Tcentral(self.ns,self.ni,self.z,self.RHO_D)
        self.tcentral=float("{0:.4f}".format(tc.begin()))
        self.eta,self.sumw = tc.params_error()

    def parameters(self):
        return self.z,self.RHO_D,self.G,self.LAMBDA_ALPHA

    def get_plots(self):
        return sts.lineal_plot(self.m,self.a,self.b,max(self.ni),self.ni,self.ns)

    def get_errors(self):
        #error edad central
        vc=(1/((self.sumw)*(self.eta**2)*(1-self.eta)**2))+(1/self.nd)+((self.zetaerr/self.z**2)**2)
        self.centralerror=self.tcentral*sqrt(vc)

        #error edad pooled
        vc=(1/sum(self.ns))+(1/sum(self.ni))+(self.zetaerr/self.z**2)**2
        self.poolederror=self.t_pooled*sqrt(vc)
