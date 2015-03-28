from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from datetime import datetime
from django.contrib.auth import login as django_login, authenticate, logout as django_logout
from django.core.context_processors import csrf
from app.forms import RegistrationForm, AuthenticationForm, ProductForm
from app.models import *
# Create your views here.

def landing(request):
    now = datetime.now()
    template = loader.get_template('general/landing.html')
    context = RequestContext(request, {
        "title": "Bienvenido!"
        #"year" : now
    })
    return HttpResponse(template.render(context))
    
def profile(request):
    now = datetime.now()
    template = loader.get_template('general/profile.html')
    
    profile = User.objects.get(id=1)

    print profile.name

    context = RequestContext(request, {
        "user_id": request.user.id,
        "name" : profile.name,
        "contact" : profile.contact,
        "phone" : profile.phone,
        "address" : profile.address,
        "description" : profile.descripction,
        "mision" : profile.mision,
        "vision" : profile.vision
    })

    return render_to_response('general/profile.html', context)

def new_product(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            # Now call the index() view.
            # The user will be shown the homepage.
            return landing(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        template = loader.get_template('products/new.html')
        context = RequestContext(request, {
            "title": "Bienvenido!"
            #"year" : now
        })
        form = ProductForm()
    return render_to_response('products/new.html', {'form': form}, context)

def product(request, id_product):
    template = loader.get_template('products/detail.html')
    context = RequestContext(request, {
        "title": "Vista Detalle",
        "product_name": id_product
    })
    return HttpResponse(template.render(context))

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return redirect('/profile')
    else:
        form = AuthenticationForm()
    return render_to_response('general/login.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/profile')
    else:
        form = RegistrationForm()
    return render_to_response('general/register.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def logout(request):
    """
    Log out view
    """
    django_logout(request)
    return redirect('/')