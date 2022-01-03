from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
# Create your views here.
from db_app.models import StaffWorkspaceModel, WorkspaceModel

from .forms import WorkspaceCreateForm, SearchTaskForm

from django.contrib.auth.models import User
# import redis

# red = redis.StrictRedis(host='localhost', port=6379)

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
        
class WorkspaceAddUserUpdateView(View):
    def get(self, request, workspace_id, username):
        print("hello !!!")
        staff_workspace = StaffWorkspaceModel.objects.filter(
            # workspace__id__contains=workspace_id,
            staff__username__contains=username
        )
        print("-----------------------",staff_workspace)
        if staff_workspace:
            StaffWorkspaceModel.objects.delete(staff_workspace)
        return redirect('workspace-add-user-update-view')


class WorkspaceStatisticView(View):
    def get(self, request, workspace_id):
        workspace_name = WorkspaceModel.objects.get(id=workspace_id).name
        print("heeeee")
        print(request.POST.__dict__)
        context={
            "user": request.user,
            "page_name": f"Thống kê {workspace_name}",
            "tasks":[{ 'index':1,  'name':'FE design','start_date':'02/05/2021','due_date':'03/06/2021',
                        'members':[{'name':'tuenguyen','url':'https://bootdey.com/img/Content/avatar/avatar1.png'},{'name':'long kun','url':'https://bootdey.com/img/Content/avatar/avatar3.png'}, ],
                        'progress':100,'status':'completed'},
                    {   'index':2,'name':'DB design','start_date':'02/02/2022','due_date':'03/04/2022',
                        'members':[{'name':'tuenguyen','url':'https://bootdey.com/img/Content/avatar/avatar1.png'},{'name':'hoa kun','url':'https://bootdey.com/img/Content/avatar/avatar2.png'}, ],
                        'progress':20,'status':'doing'}
                    ],
            "total":2,
            "pending":1,
            'completed':1,
            'forms':SearchTaskForm()
        }
        return render(request, template_name='manager_app/workspace-statistics-view.html', context=context)

    def post(self, request, workspace_id):
        workspace_name = WorkspaceModel.objects.get(id=workspace_id).name
        print("heeeee post")
        print(dir(request.POST), request.POST.get("start_date"))
        context={
            "user": request.user,
            "page_name": f"Thống kê {workspace_name}",
            "tasks":[{ 'index':1,  'name':'FE design','start_date':'02/05/2021','due_date':'03/06/2021',
                        'members':[{'name':'tuenguyen','url':'https://bootdey.com/img/Content/avatar/avatar1.png'},{'name':'long kun','url':'https://bootdey.com/img/Content/avatar/avatar3.png'}, ],
                        'progress':100,'status':'completed'},
                    {   'index':2,'name':'DB design','start_date':'02/02/2022','due_date':'03/04/2022',
                        'members':[{'name':'tuenguyen','url':'https://bootdey.com/img/Content/avatar/avatar1.png'},{'name':'hoa kun','url':'https://bootdey.com/img/Content/avatar/avatar2.png'}, ],
                        'progress':20,'status':'doing'}
                    ],
            "total":2,
            "pending":1,
            'completed':1,
            'forms':SearchTaskForm()
        }
        return render(request, template_name='manager_app/workspace-statistics-view.html', context=context)