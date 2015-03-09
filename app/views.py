from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from datetime import datetime
# Create your views here.

def login(request):
    now = datetime.now()
    template = loader.get_template("general/login.html")
    context = RequestContext(request, {
        "title": "Bienvenido!",
        "year" : now
    })
    return HttpResponse(template.render(context))
    
def home(request):
    now = datetime.now()
    template = loader.get_template("general/index.html")
    context = RequestContext(request, {
        "title": "Industrial Network",
        "year" : now
    })
    return HttpResponse(template.render(context))

def product(request, id_product):
    template = loader.get_template("products/detail.html")
    context = RequestContext(request, {
        "title": "Vista Detalle",
        "product_name": id_product
    })
    return HttpResponse(template.render(context))
    #return HttpResponse("Producto %s" % id_product)