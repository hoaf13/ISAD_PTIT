from django.shortcuts import redirect, render
from django.views import View
from django.http import HttpResponse
# Create your views here.
from db_app.models import EvaluationModel, StaffWorkspaceModel, WorkspaceModel, TaskModel
from django.contrib.auth.models import User
from .forms import TaskStatusForm


class WorkspaceListView(View):

    def get(self, request):
        user = request.user
        staff_workspaces = StaffWorkspaceModel.objects.filter(staff=user)
        workspaces = []
        for staff_workspace in staff_workspaces:
            workspaces.append(staff_workspace.workspace)
        context = {
            "workspaces": workspaces,
            "user": request.user,
            "page_name": "Danh sách Workspaces"
        }        
        return render(request, template_name="staff_app/workspace-list-view.html", context=context)


class TaskListView(View):
    def get(self, request, workspace_id):
        # lấy thông tin user đã tham gia vào workspace
        user = request.user
        workspace_name = WorkspaceModel.objects.get(id=workspace_id).name
        staff_workspaces = StaffWorkspaceModel.objects.filter(staff=user)
        tasks = TaskModel.objects.filter(staff_workspace__in=staff_workspaces)
        
        clusters = dict()
        for task in tasks:
            if task.tag not in clusters:
                clusters[task.tag] = [task]
            else:
                clusters[task.tag].append(task)
        
        context = {
            "clusters":clusters,
            "workspace_id": workspace_id,
            "workspace_name": workspace_name,
            "user": request.user,
            "page_name": f"Danh Sách Công Việc trong {workspace_name}"
        }
        return render(request,template_name='staff_app/task-list-view.html', context=context)


class TaskUpdateStatusView(View):
    def get(self, request, workspace_id, task_id, status):
        user = request.user
        task = TaskModel.objects.get(id=task_id)
        if status == "left":
            if task.status == "chưa xác nhận":
                pass
            elif task.status == "đang xử lý":
                task.status = "chưa xác nhận"
            elif task.status == "hoàn thành":
                task.status = "đang xử lý"
            elif task.status == "đóng":
                task.status = "hoàn thành"
        if status == "right":
            if task.status == "chưa xác nhận":
                task.status = "đang xử lý"
            elif task.status == "đang xử lý":
                task.status = "hoàn thành"
            elif task.status == "hoàn thành":
                task.status = "đóng"
            elif task.status == "đóng":
                pass
        task.save()
        return redirect(f'/staff/workspace-list-view/{workspace_id}/')


class DetailTaskView(View):
    def get(self ,request, workspace_id, task_id):
        workspace_name = WorkspaceModel.objects.get(id=workspace_id).name
        task = TaskModel.objects.get(id=task_id)
        evaluations = EvaluationModel.objects.filter(task__pk=task_id)
        print("evaluations: ", evaluations)
        context = {
            "task": task,
            "workspace_id": workspace_id,
            "evaluations": evaluations,
            "workspace_name":workspace_name,
            "user": request.user,
            "page_name": f"Đánh giá công việc {task.name}"
        }
        return render(request, template_name='staff_app/task-detail-view.html', context=context)

    