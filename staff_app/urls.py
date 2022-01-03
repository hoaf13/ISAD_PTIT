from django.urls import path
from .views import WorkspaceListView

urlpatterns = [
    path('workspace-list-view/', WorkspaceListView.as_view(), name='workspace-list-staff-view')
]