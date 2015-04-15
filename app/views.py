# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect
from app.forms import *
from app.models import *

@csrf_protect
def landing(request):
    r_form = UserCreateForm(auto_id='register_id_%s')
    l_form = AuthenticationForm(auto_id='login_id_%s')
    if request.user.is_authenticated():
        redirect('/profile/')
    else:
        if request.method == 'POST':
            print "Its posting something"
    return render(request, 'general/landing.html', {
            'r_form': r_form,
            'l_form': l_form,
            "title": "Bienvenido!",
        })

@login_required(login_url = '/')
@csrf_protect
def profile(request):
    try:
        template = loader.get_template('general/profile.html')
        user_id = request.user.id
        profile_user = User.objects.get(pk = user_id)
        client = Client.objects.get(pk = user_id)
        dictionary = {
            "user_id":          user_id,
            "title":            "Perfil de " + client.org_name,
            "profile_picture":  client.profile_picture,
            "org_name" :        client.org_name,
            "contact" :         profile_user.get_full_name(),
            "phone" :           client.phone,
            "address" :         client.address,
            "description" :     profile_user.client.description,
            "mision" :          profile_user.client.mision,
            "vision" :          profile_user.client.vision,
            "client_type":      client.client_type,
            "products":         Product.objects.filter(client_fk = user_id)
        }
        
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                dictionary["form"] = ProductForm()
                new_product = form.save(commit = False)
                new_product.client_fk = Client.objects.get(pk = user_id)
                new_product.save()
                return render(request, 'general/profile.html', dictionary)
            else:
                #The supplied form contained errors - just print them to the terminal.
                dictionary["form"] = form
                print form.errors
        else:
            dictionary["form"] = ProductForm()
        
        return render(request, 'general/profile.html', dictionary)
    except ObjectDoesNotExist:
        return redirect('/profile/update')

@login_required(login_url = '/')
@csrf_protect
def profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit = True)
            return redirect('/profile/')
        else:
            print form.errors
            return redirect('/profile/update')
    
    dictionary = {
        "title":            "Actualiza tu Perfil",
        }
    dictionary["form"] = UserUpdateForm(initial={'user_id': request.user.id})
    return render(request, 'general/profile_update.html', dictionary)

@login_required(login_url='/')
def product(request, id_product):
    user_id = request.user.id
    profile_user = User.objects.get(pk = user_id)
    client = Client.objects.get(pk = user_id)
    product = Product.objects.get(pk = id_product)

    dictionary = {
        "title":            "Vista Detalle",
        "contact" :         profile_user.get_full_name(),
        "org_name" :        client.org_name,
        "phone" :           client.phone,
        "address" :         client.address,
        "product":          Product.objects.get(pk = id_product),
    }

    return render(request, 'products/detail.html', dictionary)


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
            return redirect('/profile/update')
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

"""
def handler404(request):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response


def handler500(request):
    response = render(request, '500.html', {})
    response.status_code = 500
    return response
"""