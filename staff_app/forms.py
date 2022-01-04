from django import forms
from django.forms import fields
from db_app.models import EvaluationModel, IssueModel, TaskModel, WorkspaceModel, StaffWorkspaceModel

class TaskStatusForm(forms.Form):
    CHOICES=[('1','chưa xác nhận'),
             ('2','đang xử lý'),
             ('3','hoàn thành'),
             ('4','đóng')
            ]
    status = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class IssueForm(forms.ModelForm):
    pass