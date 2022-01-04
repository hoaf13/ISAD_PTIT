from django.urls import path
from .views import WorkspaceListView, TaskListView, TaskUpdateStatusView, DetailTaskView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('workspace-list-view/',login_required(WorkspaceListView.as_view(),login_url='login-view'), name='workspace-list-staff-view'),
    path('workspace-list-view/<int:workspace_id>/', login_required(TaskListView.as_view(),login_url='login-view'), name='task-list-view'), 
    path('workspace-list-view/<int:workspace_id>/<int:task_id>/<str:status>/', login_required(TaskUpdateStatusView.as_view(),login_url='login-view'), name='task-update-status-view'),
    path('workspace-list-view/<int:workspace_id>/<int:task_id>/', login_required(DetailTaskView.as_view(),login_url='login-view'), name='task-detail-view')
    
]