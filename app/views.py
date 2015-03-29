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
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/profile/1')
        print form.errors
    else:
        form = RegistrationForm()
    
    return render_to_response('general/landing.html', {
        'form': form,
    }, context_instance=RequestContext(request))
    
def profile(request, id):
    template = loader.get_template('general/profile.html')
    profile_user = None
    try:
        profile_user = User.objects.get( id=int(id) ) # Url args are string by default
    except Exception, e:
        # If user was not found
        '''
            IMPORTANTE!!
            Colocar id propio en lugar de utilizar 1

        '''
        return redirect('/profile/1')

    data = RequestContext(request, {
        "user_id": request.user.id,
        "name" : profile_user.name,
        "contact" : profile_user.contact,
        "phone" : profile_user.phone,
        "address" : profile_user.address,
        "description" : profile_user.descripction,
        "mision" : profile_user.mision,
        "vision" : profile_user.vision
    })

    context = RequestContext(request)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            data["form"] = ProductForm()
            form.save(commit=True)
            return render_to_response('general/profile.html', data, context)
        else:
            # The supplied form contained errors - just print them to the terminal.
            data["form"] = form
            print form.errors
    else:
        data["form"] = ProductForm()

    
    return render_to_response('general/profile.html', data, context)

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