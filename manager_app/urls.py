from django.urls import path, re_path
from .views import WorkspaceListView, WorkspaceCreateView, TaskListView, WorkspaceAddUserView, WorkspaceAddUserUpdateView, WorkspaceStatisticView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('workspace-list-view/', login_required(WorkspaceListView.as_view(),login_url='login-view'), name='workspace-list-manager-view'),
    path('workspace-create-view/', login_required(WorkspaceCreateView.as_view(),login_url='login-view'), name='workspace-create-manager-view'),
    path('workspace-list-view/<int:workspace_id>/', login_required(TaskListView.as_view(),login_url='login-view'), name='task-list-view'),
    path('workspace-list-view/<int:workspace_id>/workspace-add-user-view/', login_required(WorkspaceAddUserView.as_view(),login_url='login-view'), name='workspace-add-user-view'),
    path('workspace-list-view/<int:workspace_id>/workspace-add-user-view/<str:username>/workspace-add-user-update-view/', login_required(WorkspaceAddUserUpdateView.as_view(),login_url='login-view'), name='workspace-add-user-update-view'),
    path('workspace-list-view/<int:workspace_id>/workspace-statistics-view/', login_required(WorkspaceStatisticView.as_view(),login_url='login-view'))
]