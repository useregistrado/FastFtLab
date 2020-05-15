import pandas as pd
from scripts import t_mean_single
import stadistic_scripts
from math import sqrt
import time

s = time.time()
LAMBDA_ALPHA=1.55125e-10
G=0.5
Z=341.8
RHO_D=1508625
input = pd.read_csv('input.csv')
ns= list(input['Ns']) #Esta instruccion toma del archivo input solamente la columna Ns
ni= list(input['Ni']) #Esta instruccion toma del archivo input solamente la columna Ni

ti=[]
for i in range(len(ns)):
    t=t_mean_single(lamda_alpha=LAMBDA_ALPHA,ns=ns[i],ni=ni[i],g=G,z=Z,rho_d=RHO_D)
    ti.append(float("{0:.2f}".format(t)))

var=stadistic_scripts.sq(ti)
print("varianza poblacional: {0:.3f}".format(var[0]))
print("media: {0:.3f}".format(var[1]))
print(ti)
#
#
stadistic_scripts.grafic_norm(var[0],sqrt(var[1]))
print((time.time()-s))
