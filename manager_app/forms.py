from django import forms
from db_app.models import TaskModel, WorkspaceModel, StaffWorkspaceModel

class WorkspaceCreateForm(forms.ModelForm):
  class Meta:
      model = WorkspaceModel
      fields = ("name","tag","user")
      widgets = {
        'name': forms.Textarea(attrs={'rows':3, 'cols':60}),
        'tag': forms.Textarea(attrs={'rows':3, 'cols':60}),
      }
    

class TaskForm(forms.ModelForm):
  class Meta:
    model = TaskModel
    fields = ("name", "tag", "due_at", "description", "status", "staff_workspace")
    widgets = {
        'name': forms.Textarea(attrs={'rows':3, 'cols':60}),
        'tag': forms.Textarea(attrs={'rows':3, 'cols':60}),
        'due_at': forms.DateInput(format='%d/%m/%Y'),
        'description': forms.Textarea(attrs={'rows':3, 'cols':60}),
      }
    