from django.contrib import admin
from .models import WorkspaceModel, EvaluationModel, IssueModel, StaffWorkspaceModel, TaskModel, User
# Register your models here.

admin.site.register(WorkspaceModel)
admin.site.register(EvaluationModel)
admin.site.register(IssueModel)
admin.site.register(StaffWorkspaceModel)
admin.site.register(TaskModel)
