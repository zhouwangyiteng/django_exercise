#coding=utf-8

from django.shortcuts import render
from django import forms
from django .shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from account.models import User

# Create your views here.

class RegisterFrom(forms.Form):
    username = forms.CharField(label='Username: ', max_length=100)
    password = forms.CharField(label='Password: ', widget=forms.PasswordInput())
    email = forms.EmailField(label='Email: ')

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

def register(request):
    if request.method == 'POST':
        uf = RegisterFrom(request.POST)
        if uf.is_valid():
            #get post information
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            #write data into sql
            user = User()
            user.username = username
            user.password = password
            user.email = email
            user.save()
            #return successed page
            return render_to_response('successRegister.html', {'username': username})
    else:
        uf = RegisterFrom()
    return render_to_response('register.html', {'uf': uf}, context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST':
        uf = LoginForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = User.objects.filter(username__exact = username, password__exact = password)
            if user:
                response = HttpResponseRedirect('/account/index/')
                response.set_cookie('username', username, 3600)
                return response
            else:
                return HttpResponseRedirect('/account/login/')
    else:
        uf = LoginForm()
    return render_to_response('login.html', {'uf': uf}, context_instance=RequestContext(request))

def index(request):
    username = request.COOKIES.get('username', '')
    return render_to_response('index.html', {'username': username})

def logout(request):
    response = HttpResponse('Logout !!!')
    response.delete_cookie('username')
    return response