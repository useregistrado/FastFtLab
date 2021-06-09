from django.shortcuts import render
from django.http import HttpResponse
from Infelplot.model.control import control
from Infelplot.model.Fluence import Fluence
from Infelplot.model.fluence1 import monitor
from Infelplot.model.testGalbraith import ffrecx2
from Infelplot.model.Fzeta import Fzeta
import Infelplot.model.radialplot as rd
import pandas as pd
import pdfkit as pdf
import base64
from django.template.loader import get_template

def base(request):
    return render(request,'base.html')

def acerca(request):
    return render(request,'acerca.html')

def index(request):
    return render(request,'home.html')


def zeta(request):
    if request.method == 'POST':
        muestra=int(request.POST['muestra'])
        analista=request.POST['analista']
        date=request.POST['date']
        date=date.split('-')
        ndate=date[2]+'/'+date[1]+'/'+date[0]
        edad=float(request.POST['edad'])
        error=float(request.POST['error'])
        rhod=float(request.POST['rhod'])
        nd=int(request.POST['nd'])
        uds=float(request.POST['uds'])
        csvf=request.FILES['csvzeta']

        csv = pd.read_csv(csvf,sep=',')
        print('archivo debe estar separado por comas')
        try:
            ns= list(csv['Ns']) #Esta instruccion toma del archivo csv solamente la columna Ns
            ni= list(csv['Ni']) #Esta instruccion toma del archivo csv solamente la columna Ni
            ng= list(csv['Ng']) #Esta instruccion toma del archivo csv solamente la columna Ni
        except:
            return render(request,'zeta.html')
        fz=Fzeta(muestra,analista,ndate,edad,error,rhod,nd,uds,ns,ni,ng)
        doc = fz.begin()
        return render(request,'zeta.html',{'doc':doc,'disable':True})
    return render(request,'zeta.html')

def radialplot(request):
    if request.method == 'POST':
        csvf=request.FILES['datafileplot']
        p = csvf.temporary_file_path()
        i0=rd.radialp(p,"arcsine")
        i1=rd.radialp(p,"logarithmic")
        i2=rd.radialp(p,"linear")
        return render(request,'radialplot.html',{'i':[i0,i1,i2]})
    return render(request,'radialplot.html')

def fluence(request):
    if request.method=='POST':
        rhodM0=int(request.POST['rhodM0'])
        rhodM1=int(request.POST['rhodM1'])
        ndM0 =int(request.POST['NdM0'])
        ndM1 =int(request.POST['NdM1'])
        pos0 =int(request.POST['pos0'])
        pos1 =int(request.POST['pos1'])
        desc=request.POST['description']
        irrNum=request.POST['numberi']
        reactor=request.POST['reactor']
        irrDate=request.POST['datei']
        irrDate=irrDate.split('-')
        nirrDate=irrDate[2]+'/'+irrDate[1]+'/'+irrDate[0]
        vidrio=request.POST['vidrio']
        details='Irradiation number: '+irrNum+'\n'+'Reactor: '+reactor+'\n'+'Irradiation date: '+nirrDate+'\n'+'Glass: '+vidrio+'\n'+'Description:;'+desc
        f = Fluence(rhodM0,rhodM1,ndM0,ndM1,pos0,pos1,details)
        doc = f.begin()
        return render(request,'fluence.html',{'doc':doc,'disable':True})
    else:
        return render(request,'fluence.html',{'disable':False})

def fluence1(request):
    if request.method=='POST':
        c=float(request.POST["csz"])
        file=request.FILES["fluencefile"]
        csv = pd.read_csv(file,sep=',')
        a=list(csv["A"])
        b=list(csv["B"])
        rho, n = monitor(a,b,c)
        return render(request,'fluence.html',{'d':True,'r':rho,'n':n})

def pdff(request):
    #basado en https://stackoverflow.com/questions/50008935/how-to-get-the-rendered-template-from-django-pdfkit
    if request.method=='POST':
        template = get_template('reporte.html')
        date = request.POST["date"]
        date=date.replace("-","")
        date=date[6:]+"/"+date[4:6]+"/"+date[0:4]
        rhod=float(request.POST["rho"])
        nd=float(request.POST["Nd"])
        z = float(request.POST["zeta"])
        zerror=float(request.POST['zerror'])
        analista=request.POST["analista"]
        csvTwo=request.FILES["file2"]
        c = control(csvTwo,analista,rhod,z,nd,zerror,date)
        c.begin()
        doc=c.get_doc()
        ages=c.getAges()
        t = c.get_tx()
        p = c.get_parameters()
        i = c.get_plots()
        html = template.render({"rows":ages,"ages":t,"p":p,"i":i,"date":date})
        options = {
            'page-size': 'Letter',
            'encoding': "UTF-8",
            'quiet': '',
        }
        pdfile = pdf.from_string(html,False,options)
        encoded_string = str(base64.b64encode(pdfile))[2:-1]
        hist=c.get_histo()

        return render(request,'edades.html',{'doc':doc,'docp':encoded_string,'disable':True,'h':hist})

def index(request):
    return render(request,'index.html')

def cedades(request):
    return render(request,'edades.html')

def testG(request):
    if request.method == 'POST':
        file = request.FILES['csvgalb']
        csvo = pd.read_csv(file)
        ni = list(csvo['Ni'])
        ns = list(csvo['Ns'])
        r = ffrecx2(ns,ni)
        return render(request,'testG.html',{'response':r})
    return render(request,'testG.html')

def plot(request):
    # Creamos los datos para representar en el gráfico
    x = range(1,11)
    y = sample(range(20), len(x))

    # Creamos una figura y le dibujamos el gráfico
    f = plt.figure()

    # Creamos los ejes
    axes = f.add_axes([0.15, 0.15, 0.75, 0.75]) # [left, bottom, width, height]
    axes.plot(x, y)
    axes.set_xlabel("Eje X")
    axes.set_ylabel("Eje Y")
    axes.set_title("Mi gráfico dinámico")

    # Como enviaremos la imagen en bytes la guardaremos en un buffer
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    # Creamos la respuesta enviando los bytes en tipo imagen png
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    # Limpiamos la figura para liberar memoria
    f.clear()

    # Añadimos la cabecera de longitud de fichero para más estabilidad
    response['Content-Length'] = str(len(response.content))

    # Devolvemos la response
    return response
