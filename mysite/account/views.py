#coding=utf-8

from django.shortcuts import render
from django import forms
from django .shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from account.models import User

# Create your views here.

class UserFrom(forms.Form):
    username = forms.CharField(label='Username: ', max_length=100)
    password = forms.CharField(label='Password: ', widget=forms.PasswordInput())
    email = forms.EmailField(label='Email: ')

def register(request):
    if request.method == 'POST':
        uf = UserFrom(request.POST)
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
            return render_to_response('success.html', {'username': username})
    else:
        uf = UserFrom()
    return render_to_response('register.html', {'uf': uf})

