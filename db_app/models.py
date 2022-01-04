from typing import KeysView
from django.db import models
from django.contrib.auth.models import User

"""Dự Án"""
class WorkspaceModel(models.Model):
    name = models.TextField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.TextField(max_length=256, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.id}. {self.name}"


"""Thêm Nhân Viên vào Dự Án"""
class StaffWorkspaceModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    workspace = models.ForeignKey(WorkspaceModel,on_delete=models.CASCADE, default=0)
    staff = models.ForeignKey(User,on_delete=models.CASCADE, default=0)
    """id to WorkspaceModel"""
    """id to UserModel"""
    
    def __str__(self) -> str:
        return f"{self.staff} - {self.workspace.name}"

"""Công việc"""
class TaskModel(models.Model):
    name = models.TextField(max_length=256)
    tag = models.TextField(max_length=256) 
    created_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(auto_created=True)
    description = models.TextField(max_length=2048)
    status = models.TextField(max_length=32)
    # chưa xác nhận
    # đang xử lý
    # đã hoàn thành     
    # đóng task 
    staff_workspace = models.ForeignKey(StaffWorkspaceModel, on_delete=models.CASCADE, default=0)
    """id to StaffWorkspaceModel"""

    def __str__(self):
        return f"{self.id}.{self.name} - {self.staff_workspace.staff.username}"
    
""" Đánh giá công việc """
class EvaluationModel(models.Model):
    description = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    point = models.IntegerField(null=True)
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE, null=True)
    """id to TaskModel"""
    def __str__(self) -> str:
        return f"{self.id}.{self.description} - {self.task}"

""" Issue trong công việc """
class IssueModel(models.Model):
    name = models.TextField(max_length=2000, null=True)
    description = models.TextField(max_length=2000)
    status = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(auto_created=True)
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    """id to TaskModel"""

""" Comment trong Issue """
class CommentModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1000)
    issue = models.ForeignKey(IssueModel, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    """id to Issue"""
