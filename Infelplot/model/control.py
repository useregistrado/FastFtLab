from Infelplot.model.standards import stnd
import pandas as pd
from Infelplot.model.Trace import Trace
from Infelplot.model.Zscripts import Zscripts
import base64
class control():

    def __init__(self,csvTwo,analista,rhoD,z,nd,zerror,date):
        self.csvTwo=csvTwo
        self.trace=None
        self.analista=analista
        self.rhoD=rhoD
        self.ns=None
        self.ni=None
        self.z = z
        self.nd=nd
        self.zerror=zerror
        self.date=date

    def begin(self):
        nt = self.openc(self.csvTwo)
        if len(nt[0])==len(nt[1]):
            self.trace=Trace(nt[0],nt[1],self.z,self.rhoD,self.nd,self.zerror)
            self.trace.begin()
            self.ns=nt[0]
            self.ni=nt[1]
        return "¡¡Error!! \nLas columnas no tienen la misma cantidad de datos"

    def openc(self,csv):
        csv = pd.read_csv(csv)
        ns= list(csv['Ns']) #Esta instruccion toma del archivo csv solamente la columna Ns
        ni= list(csv['Ni']) #Esta instruccion toma del archivo csv solamente la columna Ni
        return ns,ni

    def getAges(self):
        ages = self.trace.ages
        aux=[]
        for i in range(len(ages)):
            aux2=[i,self.ns[i],self.ni[i],ages[i]]
            aux.append(aux2)
        return aux

    def get_tx(self):
        t_central=self.trace.tcentral
        t_mean = self.trace.t_mean
        t_pooled = self.trace.t_pooled
        t_isocrona = self.trace.t_isocrona

        return t_central,t_mean, t_pooled, t_isocrona

    def get_parameters(self):
        return self.trace.parameters()

    def get_plots(self):
        return self.trace.get_plots()

    def get_doc(self):
        cabeza='Fission-Track Age Calculation\nAnalyst:;'+self.analista+'\nDate:;'+self.date+'\nZeta:;'+str(self.z)+';\nZeta error:;'+str(self.zerror)+'\nrho-d:;'+str(self.rhoD)+'\nNd:;'+str(self.nd)
        pie='\n\n\nCentral age:;'+str(self.trace.tcentral)+'\nError:;'+str(self.trace.centralerror)+'\nDispersion:;'+'\n\nPooled age:;'+str(self.trace.t_pooled)+'\nError:;'+str(self.trace.poolederror)+'\n\nMean age:;'+str(self.trace.t_mean)+'\n\nT isocrona:;'+str(self.trace.t_isocrona)
        doc = (cabeza+pie).replace('.',',')
        base = str(base64.b64encode(bytes(doc, 'utf-8')))[2:-1]
        return base

    def get_histo(self):
        return self.trace.histograma()
