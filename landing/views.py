from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

from django.views import View
from django.views.generic.base import RedirectView
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    ListView,
    DeleteView,
    FormView
)

import json

class LandingView(View):
    template_name = "landing/landing.html"

    def get(self, request, *args, **kwargs):
        # GET method
        context={}                
        return render(request, self.template_name, context)

class LoginView(FormView):
    template_name = "landing/login.html"

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        context = {'form':form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):        
        form = AuthenticationForm(data=request.POST)                        
        if form.is_valid():
            #log the user            
            user = form.get_user()                        
            login(request, user)
            print("login exitoso")
            if user.is_superuser:            
                return redirect('superuser:dashboard')
            if user.is_sms_manager:            
                return redirect('managers:dashboard')
            if user.is_employee:            
                return redirect('employees:dashboard')
        #if form not valid            
        context = {'form':form}
        return render(request, self.template_name, context)

class LogoutView(RedirectView):
    def get(self, request):        
        logout(request)        
        return HttpResponseRedirect(reverse('landing:landing'))