from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
# Create your views here.
from db_app.models import StaffWorkspaceModel, TaskModel, WorkspaceModel

from .forms import WorkspaceCreateForm, SearchTaskForm

from django.contrib.auth.models import User
# import redis

# red = redis.StrictRedis(host='localhost', port=6379)
from .forms import WorkspaceCreateForm, TaskForm

from django.contrib.auth.models import User

from datetime import datetime


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
        # lấy thông tin user đã tham gia vào workspace
        workspace_name = WorkspaceModel.objects.get(id=workspace_id).name
        staffs = User.objects.filter(is_superuser=False)
        staff_workspaces = StaffWorkspaceModel.objects.filter(workspace__pk=workspace_id)
        users = []
        for staff in staffs:
            for staff_workspace in staff_workspaces:
                if staff.username == staff_workspace.staff.username:
                    users.append(staff)
                    break
        staff_workspaces = StaffWorkspaceModel.objects.filter(staff__in=users)
        tasks = TaskModel.objects.filter(staff_workspace__in=staff_workspaces)

        clusters = dict()
        for task in tasks:
            if task.tag not in clusters:
                clusters[task.tag] = [task]
            else:
                clusters[task.tag].append(task)
        print(clusters)
        context = {
            "clusters":clusters,
            "tasks": tasks,
            "workspace_name": workspace_name,
            "user": request.user,
            "page_name": f"Danh Sách Công Việc trong {workspace_name}"
        }
        return render(request,template_name='manager_app/task-list-view.html', context=context)


class WorkspaceAddUserView(View):

    def get(self, request, workspace_id):
        workspace_name = WorkspaceModel.objects.get(id=workspace_id).name
        staffs = User.objects.filter(is_superuser=False)

        staff_workspaces = StaffWorkspaceModel.objects.filter(workspace__pk=workspace_id)
        for staff in staffs:
            staff.status = False
            for staff_workspace in staff_workspaces:
                if staff.username == staff_workspace.staff.username:
                    staff.status = True
                    break
        context = {
            "staffs":staffs,
            "workspace_id": workspace_id,
            "user": request.user,
            "page_name": f"Danh sách tham gia {workspace_name}"
        }
        return render(request, template_name='manager_app/workspace-add-user-view.html', context=context)
        

class WorkspaceAddUserUpdateView(View):
    def get(self, request, workspace_id, username):
        print(f"workspace: {workspace_id} - username: {username}")
        staff_workspace = StaffWorkspaceModel.objects.filter(
            workspace__pk=workspace_id,
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
        if len(staff_workspace):            
            staff_workspace.delete()
            print("delete successfull !")
        else:
            instance = StaffWorkspaceModel.objects.create(workspace=WorkspaceModel.objects.get(id=workspace_id),staff=User.objects.filter(username=username)[0])
            instance.save()
            print("create successfull !")
        return redirect(f'/manager/workspace-list-view/{workspace_id}/workspace-add-user-view/')


class WorkspaceDeleteView(View):
    def get(self, request, workspace_id):
        workspace = WorkspaceModel.objects.get(id=workspace_id)
        workspace.delete()
        return redirect('workspace-list-manager-view')


class TaskCreateView(View):
    def get(self, request, workspace_id):
        workspace_name = WorkspaceModel.objects.get(id=workspace_id).name
        staff_workspaces = StaffWorkspaceModel.objects.filter(workspace__pk=workspace_id, staff__is_superuser=False)
        choices = [(staff_workspace.staff.username, staff_workspace.staff.username) for staff_workspace in staff_workspaces ]
        form = TaskForm()
        form.fields["staff_workspace"].choices = choices
        # print(form.cleaned_data['staff_workspace'])
        context = {
            "form": form,
            "workspace_id": workspace_id,
            "workspace_name": workspace_name,
            "user": request.user,
            "page_name": f"Tạo Công Việc trong {workspace_name}"
        }
        return render(request,template_name='manager_app/task-create-view.html', context=context)

    def post(self, request, workspace_id):
        # tạo TaskModel
        username = request.POST['staff_workspace']
        staff_workspace = StaffWorkspaceModel.objects.filter(workspace__pk=workspace_id, staff=User.objects.filter(username=username)[0])[0]
        print(staff_workspace)
        form = WorkspaceCreateForm(
            {
                'name':request.POST['name'],
                'tag':request.POST['tag'],
                'due_at':request.POST['due_at'], 
                'description': request.POST['description'],
                'status': 'chưa xác nhận',
                'staff_workspace': request.POST['staff_workspace']
            }   
        )

        date_time_obj = datetime.strptime(request.POST['due_at'], '%d/%m/%Y')
        instances = TaskModel.objects.create(
            name=request.POST['name'],
            tag=request.POST['tag'],
            due_at=date_time_obj,
            description=request.POST['description'],
            status='chưa xác nhận',
            staff_workspace=staff_workspace
        )
        instances.save()
        return redirect(f'/manager/workspace-list-view/{workspace_id}/')
        
