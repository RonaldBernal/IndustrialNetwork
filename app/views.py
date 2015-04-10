from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from app.forms import UserCreateForm, AuthenticationForm, ProductForm
from app.models import *
# Create your views here.

@csrf_protect
def landing(request):
    r_form = UserCreateForm(auto_id='register_id_%s')
    l_form = AuthenticationForm(auto_id='login_id_%s')
    if request.user.is_authenticated():
        redirect('/profile/')
    else:
        if request.method == 'POST':
            print "Its posting something"
    return render_to_response('general/landing.html', {
            'r_form': r_form,
            'l_form': l_form,
            "title": "Bienvenido!",
        }, context_instance = RequestContext(request))

@login_required(login_url = '/')
@csrf_protect
def profile(request):
    template = loader.get_template('general/profile.html')
    user_id = request.user.id
    profile_user = None
    profile_user = User.objects.get(pk = user_id)
    
    
    dictionary = RequestContext(request, {
        "user_id": user_id,
        #"name" : profile_user.client.name,
        "contact" : profile_user.get_full_name(),
        #"phone" : profile_user.client.phone,
        #"address" : profile_user.client.address,
        #"description" : profile_user.client.description,
        #"mision" : profile_user.client.mision,
        #"vision" : profile_user.client.vision
    })
    
    
    context = RequestContext(request)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            dictionary["form"] = ProductForm()
            form.save(commit = True)
            return render_to_response('general/profile.html', dictionary, context)
        else:
            #The supplied form contained errors - just print them to the terminal.
            dictionary["form"] = form
            print form.errors
    else:
        dictionary["form"] = ProductForm()
    
    return render_to_response('general/profile.html', dictionary) #, context)

@login_required(login_url='/')
@csrf_protect
def new_product(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save(commit = True)
            # Now call the index() view.
            # The user will be shown the homepage.
            return landing(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        template = loader.get_template('products/new.html')
        context = RequestContext(request, {
            "title": "Registro de Productos"
            #"year" : now
        })
        form = ProductForm()
    return render_to_response('products/new.html', {'form': form}, context)

@login_required(login_url='/')
def product(request, id_product):
    template = loader.get_template('products/detail.html')
    context = RequestContext(request, {
        "title": "Vista Detalle",
        "product_name": id_product
    })
    return HttpResponse(template.render(context))


'''
User auth and reg views
'''

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserCreateForm(data = request.POST)
        if form.is_valid():
            # save user
            user = form.save()
            # auth user
            user = authenticate(username=request.POST.get('username', ''),
                                password=request.POST.get('password1', ''))
            # log in user
            django_login(request, user)
            return redirect('/profile/')
        print form.errors
    return redirect('/')

@csrf_protect
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return redirect('/profile/')
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                # the authentication system was unable to verify the username and password
                print("The username and password were incorrect.")
        print form.errors
    return redirect('/')

def logout(request):
    """
    Log out view
    """
    django_logout(request)
    return redirect('/')