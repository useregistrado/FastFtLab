from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

def sq(x): #sigma cuadrado
    m = media(x)
    sumq=0
    for xi in x:
        sumq=sumq+(xi-m)**2
    return sumq/len(x),m

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
