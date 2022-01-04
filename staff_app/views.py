from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# Create your views here.

class WorkspaceListView(View):

    def get(self, request):
        context = {
            "user": request.user,
            "page_name": "Danh sách Workspaces"
        }        
        return render(request, template_name="staff_app/workspace-list-view.html", context=context)