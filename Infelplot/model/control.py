
from Infelplot.model.standards import stnd
import pandas as pd
from Infelplot.model.Trace import Trace
class control():

    def __init__(self,csvOne,csvTwo,stnd,rhoD):
        self.csvOne=csvOne
        self.csvTwo=csvTwo
        self.trace=None
        self.stnd=stnd
        self.rhoD=rhoD
        self.ns=None
        self.ni=None

    def begin(self):
        n = self.openc(self.csvTwo)
        if len(n[0])==len(n[1]):
            standard=stnd(self.stnd)
            self.trace=Trace(n[0],n[1],341.8,self.rhoD)
            self.trace.begin()
            self.ns=n[0]
            self.ni=n[1]
        return "¡¡Error!! \nLas columnas no tienen la misma cantidad de datos"

    def openc(self,csv):
        csv_two = pd.read_csv(csv)
        ns= list(csv_two['Ns']) #Esta instruccion toma del archivo csv solamente la columna Ns
        ni= list(csv_two['Ni']) #Esta instruccion toma del archivo csv solamente la columna Ni
        return ns,ni

    def getAges(self):
        ages = self.trace.ages
        aux=[]
        for i in range(len(ages)):
            aux2=[i,self.ns[i],self.ni[i],ages[i]]
            aux.append(aux2)
        return aux

    def get_tx(self):
        t_mean = self.trace.t_mean
        t_pooled = self.trace.t_pooled
        t_isocrona = self.trace.t_isocrona

        print(t_mean,t_pooled,t_isocrona)
