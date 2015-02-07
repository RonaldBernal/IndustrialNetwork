from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from datetime import datetime
# Create your views here.

def home(request):
    now = datetime.now()
    return render_to_response("general/index.html", {"year" : now})

def product(request, id_product):
    template = loader.get_template("products/detail.html")
    context = RequestContext(request, {
        "title": "Prueba",
    })
    #return HttpResponse(template.render(context))
    return HttpResponse("Producto %s" % id_product)