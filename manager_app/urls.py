from django.urls import path, re_path
from .views import DetailTaskView, WorkspaceListView, WorkspaceCreateView, TaskListView, WorkspaceAddUserView, WorkspaceAddUserUpdateView, WorkspaceDeleteView, TaskCreateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # view - danh sách workspace
    path('workspace-list-view/', login_required(WorkspaceListView.as_view(),login_url='login-view'), name='workspace-list-manager-view'),
    # view - tạo workspace
    path('workspace-create-view/', login_required(WorkspaceCreateView.as_view(),login_url='login-view'), name='workspace-create-manager-view'),
    # view - danh sách công việc trong workspace
    path('workspace-list-view/<int:workspace_id>/', login_required(TaskListView.as_view(),login_url='login-view'), name='task-list-view'),
    # action - xóa workspace
    path('workspace-list-view/<int:workspace_id>/workspace-delete-view/', login_required(WorkspaceDeleteView.as_view(),login_url='login-view'), name='workspace-delete-view'),
    # view - thêm người vào workspace
    path('workspace-list-view/<int:workspace_id>/workspace-add-user-view/', login_required(WorkspaceAddUserView.as_view(),login_url='login-view'), name='workspace-add-user-view'),
    # action - thêm người vào workspace
    path('workspace-list-view/<int:workspace_id>/workspace-add-user-view/<str:username>/workspace-add-user-update-view/', login_required(WorkspaceAddUserUpdateView.as_view(),login_url='login-view'), name='workspace-add-user-update-view'),
    # view - tạo công việc 
    path('workspace-list-view/<int:workspace_id>/task-create-view/', login_required(TaskCreateView.as_view(),login_url='login-view'), name='task-create-view'),
    # view - hiển thị chi tiết công việc (bao gồm đánh giá)
    path('workspace-list-view/<int:workspace_id>/<int:task_id>/',login_required(DetailTaskView.as_view(), login_url='login-view'), name='task-detail-view')
]