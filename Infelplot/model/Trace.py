from math import log
import Infelplot.model.stadistic_scripts as sts
class Trace():

    def __init__(self,ns,ni,z,rhod):
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
        #variables
        self.z=z
        self.sumation_ns=0
        self.sumation_ni=0
        self.rho_i=0
        self.size=0

    def begin(self): #Esta funcion inicializa los valores de las sumatorias de ns y ni y calcula el tamaño de los datos de entrada
        self.summation()
        self.c_rho_i()
        self.size=len(self.ni)
        self.t_single()
        self.t_meanf()
        self.t_pooledf()
        m = sts.regression(self.ni,self.ns)
        self.t_isocronaf(m)

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
            return float("{0:.2f}".format((1/self.LAMBDA_ALPHA)*log(ln)/1e+6))

        for n in range(self.size):
            self.ages.append(calculate(self,self.ni[n],self.ns[n])) #agrega las edades individuales a la lista ages

    def t_pooledf(self):
        ln=self.LAMBDA_ALPHA*(self.sumation_ns/self.sumation_ni)*self.G*self.z*self.RHO_D+1
        self.t_pooled = float("{0:.2f}".format((1/self.LAMBDA_ALPHA)*log(ln)/1e+6))

    def t_isocronaf(self,m):
        ln=self.LAMBDA_ALPHA*(m)*self.G*self.z*self.RHO_D+1
        self.t_isocrona = float("{0:.2f}".format((1/self.LAMBDA_ALPHA)*log(ln)/1e+6))

    def t_meanf(self):
        self.t_mean = float("{0:.3f}".format(sts.media(self.ages)))
