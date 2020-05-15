from django.shortcuts import render
from django.http import HttpResponse
from Infelplot.model.control import control
import random
import pdfkit as pdf
from django.http import HttpResponse
from django.template.loader import get_template

def base(request):
    return render(request,'base.html')

def pdff(request):
    #basado en https://stackoverflow.com/questions/50008935/how-to-get-the-rendered-template-from-django-pdfkit
    template = get_template('base.html')
    css = 'C:/Users/Usuario/Documents/Django projects/Infelplo/Infelplot/static/css/styles2.css'
    html = template.render({})
    options = {
        'page-size': 'Letter',
        'encoding': "UTF-8",
        'quiet': '',
    }
    pdfile = pdf.from_string(html,False,options)
    response = HttpResponse(pdfile, content_type='application/pdf')
    response['Content-Disposition'] = ' filename="reporte.pdf"'
    return response


def form(request):
    if request.method=='POST':
        csvOne=request.FILES["file1"]
        csvTwo=request.FILES["file2"]
        rhod=int(request.POST["rho"])
        stnd=request.POST["selector"]
        c = control(csvOne,csvTwo,stnd,rhod)
        c.begin()
        ages=c.getAges()
        c.get_tx()
        return render(request,'index.html',{"rows":ages})

    return render(request,'index.html')
