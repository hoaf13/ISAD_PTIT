from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.

class WorkspaceListView(View):

    def get(self, request):
        return HttpResponse("Server is running ... ")