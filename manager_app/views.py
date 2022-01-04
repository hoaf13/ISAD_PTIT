from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
# Create your views here.
from db_app.models import EvaluationModel, StaffWorkspaceModel, TaskModel, WorkspaceModel

from .forms import WorkspaceCreateForm, SearchTaskForm

from django.contrib.auth.models import User
# import redis
from datetime  import datetime, time
# red = redis.StrictRedis(host='localhost', port=6379)
from .forms import WorkspaceCreateForm, TaskForm
from .forms import EvaluationForm, WorkspaceCreateForm, TaskForm

from django.contrib.auth.models import User

from datetime import datetime, date


class WorkspaceListView(View):

    def get(self, request):
        workspaces = WorkspaceModel.objects.all()
        context = {
            "workspaces": workspaces,
            "user": request.user,
            "page_name": "Danh sách Workspaces"
        }        
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
            "workspace_id": workspace_id,
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
        tasks = TaskModel.objects.all()
        task_views = {}
        for index,t in enumerate(tasks):
            # print(dir(t))
            
            if t.name not in task_views:
                progress=0# đang xử lý
    # đã hoàn thành     
    # đóng task 
                if str(t.status) == 'chưa xác nhận':
                    progress = 0
                    # print("headads")
                if str(t.status)  == 'đang xử  lý':
                    progress = 50
                if str(t.status)  == 'đã hoàn thành':
                    progress = 100
                elif str(t.status)  == 'đóng task':
                    progress = 100
                print(t.created_at.date() > date(2022,1,1), t.created_at.date())
                value = {
                    'index':index,
                    'name':t.name,
                    'start_date':t.created_at.date(),
                    'due_date':t.due_at.date(),
                    'description':t.description,
                    'status':t.status,
                    'members':[
                        {   'name':t.staff_workspace.staff.username,
                            'url':f'https://bootdey.com/img/Content/avatar/avatar{t.staff_workspace.staff.id}.png'}
                        ],
                    'progress':progress
                }
                task_views[t.name] = value
            else:
                task_views[t.name]['member'].append(t.staff_workspace.staff)
        task_views = list(task_views.values())
        for v,i in enumerate(task_views):task_views[v]['index'] = v
        pending = 0
        for t in task_views:
            if str(t['status'])  == 'chưa xác nhận' or str(t['status'])  == 'đang xử  lý':pending += 1
        completed = 0
        for t in task_views:
            if str(t['status'])   == 'đóng task' or str(t['status'])   == 'đã hoàn thành':completed += 1
        # print(task_views)
        context={
            "user": request.user,
            "page_name": f"Thống kê {workspace_name}",
            "tasks":task_views,
            "total":len(task_views),
            "pending":pending,
            'completed':completed,
            'forms':SearchTaskForm()
        }
        return render(request, template_name='manager_app/workspace-statistics-view.html', context=context)
    def filter_by_start_date(self,task_view, date):
        return [i for i in task_view if date <= i['start_date']]
    def filter_by_due_date(self,task_view, date):
        return [i for i in task_view if date <= i['due_date']]
    def filter_by_status(self, task_view, status):
        return [i for i in task_view if status in i['status']]
    def filter_by_name(self, task_view, name):
        def check(i, name):
            for j in i['members']:
                print(j)
                if name in j['name']:return True
            return False
        return [i for i in task_view if check(i,name)]
    def post(self, request, workspace_id):
        workspace_name = WorkspaceModel.objects.get(id=workspace_id).name
        print("heeeee post")
        print(dir(request.POST), request.POST.get("start_date"))

        tasks = TaskModel.objects.all()
        task_views = {}
        for index,t in enumerate(tasks):
            # print(dir(t))
            
            if t.name not in task_views:
                progress=0# đang xử lý
    # đã hoàn thành     
    # đóng task 
                if str(t.status) == 'chưa xác nhận':
                    progress = 0
                    # print("headads")
                if str(t.status)  == 'đang xử  lý':
                    progress = 50
                if str(t.status)  == 'đã hoàn thành':
                    progress = 100
                elif str(t.status)  == 'đóng task':
                    progress = 100
                # print(dir(t.created_at))
                value = {
                    'index':index,
                    'name':t.name,
                    'start_date':t.created_at.date(),
                    'due_date':t.due_at.date(),
                    'description':t.description,
                    'status':t.status,
                    'members':[
                        {   'name':t.staff_workspace.staff.username,
                            'url':f'https://bootdey.com/img/Content/avatar/avatar{t.staff_workspace.staff.id}.png'}
                        ],
                    'progress':progress
                }
                task_views[t.name] = value
            else:
                task_views[t.name]['member'].append(t.staff_workspace.staff)
        task_views = list(task_views.values())
        for v,i in enumerate(task_views):task_views[v]['index'] = v


        pending = 0
        for t in task_views:
            if str(t['status'])  == 'chưa xác nhận' or str(t['status'])  == 'đang xử  lý':pending += 1
        completed = 0
        for t in task_views:
            if str(t['status'])   == 'đóng task' or str(t['status'])   == 'đã hoàn thành':completed += 1
        # print(task_views)
        if request.POST.get("start_date") != "":
            start_date = request.POST.get("start_date").split("/")
            start_date = date(start_date[2], start_date[1], start_date[0])
            start_date = [int(i) for i in start_date]
            task_views = self.filter_by_start_date(task_views, start_date)
        if request.POST.get("due_date") != "":
            due_date = request.POST.get("due_date").split("/")
            due_date = [int(i) for i in due_date]
            due_date = date(due_date[2], due_date[1], due_date[0])
            print(due_date)
            task_views = self.filter_by_due_date(task_views, due_date)
        if request.POST.get("staff") !="":
            name = request.POST.get("staff")
            print(name)
            task_views = self.filter_by_name(task_views, name)
        context={
            "user": request.user,
            "page_name": f"Thống kê {workspace_name}",
            "tasks":task_views,
            "total":len(task_views),
            "pending":pending,
            'completed':completed,
            'forms':SearchTaskForm()
        }
        return render(request, template_name='manager_app/workspace-statistics-view.html', context=context)
        


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
        usernames = request.POST.getlist('staff_workspace')
        print("username: ", usernames)
        for username in usernames:
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


class DetailTaskView(View):
    def get(self ,request, workspace_id, task_id):
        workspace_name = WorkspaceModel.objects.get(id=workspace_id).name
        task = TaskModel.objects.get(id=task_id)
        evaluations = EvaluationModel.objects.filter(task__pk=task_id)
        print("evaluations: ", evaluations)
        form = EvaluationForm()
        context = {
            "form": form,
            "task": task,
            "evaluations": evaluations,
            "workspace_name":workspace_name,
            "user": request.user,
            "page_name": f"Đánh giá công việc {task.name}"
        }
        return render(request, template_name='manager_app/task-detail-view.html', context=context)

    def post(self, request, workspace_id, task_id):
        task = TaskModel.objects.get(id=task_id)
        form = EvaluationForm({
                'description':request.POST['description'],
                'point':request.POST['point'],
                'task':task
            }
        )
<<<<<<< HEAD
        instances.save()
        return redirect(f'/manager/workspace-list-view/{workspace_id}/')
        
=======
        if form.is_valid():
            instance = EvaluationModel.objects.create(
                description=request.POST['description'],
                point=int(request.POST['point']),
                task=task
            )
            instance.save()
        else:
            print(form.errors)
        return redirect(f'/manager/workspace-list-view/{workspace_id}/{task_id}/')
>>>>>>> 6503d489f8f3dc426f26a84438c60db66a8ddaf1
