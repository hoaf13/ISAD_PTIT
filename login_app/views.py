from django.shortcuts import redirect, render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.views import View 
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth.decorators import login_required, permission_required

class  ValidateUser(LoginRequiredMixin, View):    
    def get(self,request):
        if request.user.is_authenticated:
            redirect_field_name = '/hoaf13'
            user = User.objects.get(id=request.user.id)
            if user.is_superuser:    
                return redirect('workspace-list-manager-view')
            return redirect('workspace-list-staff-view')
