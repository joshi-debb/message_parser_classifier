
from django.shortcuts import render
from django.http import FileResponse
from proyecto3.forms import FileForm, AddForm, DeleteForm
import requests
import io


from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

endpoint = 'http://localhost:4000'

def index(request):
    return render(request, 'index.html')


def cargaMasiva(request):
    ctx = {
        'content':None,
        'response':None
    }
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['file']
            xml_binary = f.read()
            xml = xml_binary.decode('utf-8')
            ctx['content'] = xml
            response = requests.post(endpoint + 'read_datas', data=xml_binary)
            if response.ok:
                ctx['response'] = 'Archivo XML cargado corrrectamente'
            else:
                ctx['response'] = 'El archivo se envio, pero hubo un error en el servidor'
    else:
        return render(request, 'index.html')
    return render(request, 'index.html', ctx)