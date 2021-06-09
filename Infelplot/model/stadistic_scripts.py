from scipy import stats
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg') #para evitar que se apague el servidor
import base64
from io import BytesIO

def sq(x): #sigma cuadrado
    m = media(x)
    sumq=0
    for xi in x:
        sumq=sumq+(xi-m)**2
    return sumq/(len(x)-1),m

def media(x):
    n=len(x)
    sum=0
    for xi in x:
        sum=sum+xi
    return sum/n

def grafic_norm(mu, sigma):
    normal = stats.norm(mu, sigma)
    x = np.linspace(normal.ppf(0.01)-5,normal.ppf(0.99)+5, 1000)
    fp = normal.pdf(x) # Función de Probabilidad
    plt.plot(x, fp)
    plt.title('Distribución Normal')
    plt.ylabel('probabilidad')
    plt.xlabel('valores')
    plt.show()

def regression(xi,yi):
    sum_numerator=0
    sum_denominator=0
    for i in range(len(xi)):
        sum_numerator+=xi[i]*yi[i]
        sum_denominator+=xi[i]**2
    return sum_numerator/sum_denominator

def regression_b(xi,yi):
    xm = np.mean(xi)
    ym = np.mean(yi)
    b  = np.cov(xi,yi)[0][1]/np.var(xi,ddof=1)
    a  = ym - b*xm
    return a,b

def lineal_plot(m,a,b,max,ni,ns):
    x = np.arange(0, max, 0.01)
    y = m*x

    y2 = b*x+a
    label_one="y = %.4fX"%m
    label_two="y = %.4fX + %.3f"%(b,a)
    fig, ax = plt.subplots(figsize=(4.8,4))
    ax.bbox_inches='tight'
    ax.plot(x, y, label=label_one,c="#4512AE")
    ax.plot(x, y2, label=label_two,c="#0B61A4")
    ax.plot(ni, ns,"x",c="#3BDA00")
    ax.margins(0.025,0.025)
    ax.legend()
    #ax.clf()
    plt.xlabel('Ni Values')
    plt.ylabel('Ns Values')
    plt.title('Lineal regression')
    plt.grid(True)
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    html = '<img src=\'data:image/png;base64,{}\' with =\'10\'>'.format(encoded)
    plt.close()
    return html

def plotp():
    x = np.arange(0, 4, 0.1)
    y = 2*x
    fig, ax = plt.subplots()
    ax.plot(x, y, label="label_one",c="#4512AE")
    #plot sth

    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    html = '<img src=\'data:image/png;base64,{}\'>'.format(encoded)
    print(html)
    return html
