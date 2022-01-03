from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
# Create your views here.
from db_app.models import WorkspaceModel

from .forms import WorkspaceCreateForm

from django.contrib.auth.models import User


class WorkspaceListView(View):

    def get(self, request):
        workspaces = WorkspaceModel.objects.all()
        context = {
            "workspaces": workspaces,
            "user": request.user,
            "page_name": "Danh sách Workspaces"
        }        
        print(request.user)
        return render(request, template_name='manager_app/workspace-list-view.html', context=context)


class WorkspaceCreateView(View):
    
    def get(self, request):
        form = WorkspaceCreateForm()
        form.initial['user'] = request.user
        context = {
            "form": form,
            "user": request.user,
            "page_name": "Tạo một Workspace"
        }
        return render(request, template_name='manager_app/workspace-create-view.html', context=context)

    def post(self, request):
        form = WorkspaceCreateForm({'user':request.user,'tag':request.POST['tag'],'name':request.POST['name']})
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        return redirect('workspace-list-manager-view')


class TaskListView(View):
    
    def get(self, request, workspace_id):
        workspace_name = WorkspaceModel.objects.get(id=workspace_id).name
        context = {
            "workspace_name": workspace_name,
            "user": request.user,
            "page_name": f"Danh Sách Công Việc trong {workspace_name}"
        }
        return render(request,template_name='manager_app/task-list-view.html', context=context)


class WorkspaceAddUserView(View):

    def get(self, request, workspace_id):
        workspace_name = WorkspaceModel.objects.get(id=workspace_id).name
        staffs = User.objects.filter(is_superuser=False)
        context = {
            "staffs":staffs,
            "user": request.user,
            "page_name": f"Danh sách tham gia {workspace_name}"
        }
        return render(request, template_name='manager_app/workspace-add-user-view.html', context=context)
        