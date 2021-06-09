from math import sqrt
from datetime import date
import base64
class Fluence():
    def __init__(self,rhod0,rhod1,nd0,nd1,pos0,pos1,desc):
        self.rhod0=rhod0
        self.rhod1=rhod1
        self.nd0=nd0
        self.nd1=nd1
        self.pos0=pos0
        self.pos1=pos1
        self.pos=[]
        self.distance=[]
        self.Nd=[]
        self.RhoD=[]
        self.RErhod=[]
        self.RErhod0=None
        self.RErhod1=None
        self.desc=desc
    def poss(self):
        for i in range(1,self.pos1+1):
            self.pos.append(i)

    def distances(self):
        distace=0
        incremento = 100/(self.pos1-1)
        for i in range(self.pos1):
            self.distance.append(float("{0:.1f}".format(distace)))
            distace+=incremento
    def nds(self):
        Nd=[]
        incremento = (self.nd1-self.nd0)/(self.pos1-1)
        ndi=self.nd0
        for i in range(self.pos1):
            Nd.append(ndi)
            ndi=ndi+incremento
        for j in Nd:
            self.Nd.append(round(j))
    def rhods(self):
        incremento = (self.rhod1-self.rhod0)/(self.pos1-1)
        rhodi = self.rhod0
        for i in range(self.pos1):
            self.RhoD.append(int("{0:.0f}".format(rhodi)))
            rhodi+=incremento
    def rerhod(self):
        j=0
        for k in self.distance:
            i = k/100
            term0 = (1-i)*self.RErhod0*self.rhod0
            term1 = i*self.RErhod1*self.rhod1
            sex = sqrt(term0**2+term1**2)
            rex = sex/self.RhoD[j]
            self.RErhod.append(float("{0:.2f}".format(rex)))
            j+=1
    def begin(self):
        self.RErhod0 = float("{0:.2f}".format(sqrt(1/self.nd0)*100))
        self.RErhod1 = float("{0:.2f}".format(sqrt(1/self.nd1)*100))
        print(self.RErhod0,self.RErhod1)
        self.poss()
        self.distances()
        self.nds()
        self.rhods()
        self.rerhod()
        t=str(self.imprimir())
        doc = t[2:-1]
        return doc

    def imprimir(self):
        text0='INTERPOLATED TRACK DENSITY USING A PAIR OF GLASS STANDARDS\nDate:;'+str(date.today())+'\n'+self.desc
        text = text0+'\nmonitor label;Position;Distance(%);Nd;RhoD(t/cm^2);RE[RhoD](%)'
        for i in range(self.pos1):
            label=''
            if i+1 == self.pos0:
                label='First Monitor'
            elif i+1==self.pos1:
                label='Second Monitor'
            text= text + '\n' + label+';'+str(self.pos[i])+';'+str(self.distance[i])+';'+str(self.Nd[i])+';'+str(self.RhoD[i])+';'+str(self.RErhod[i])
        return base64.b64encode(bytes(text, 'utf-8'))
