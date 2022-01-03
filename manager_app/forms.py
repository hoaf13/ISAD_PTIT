from django import forms
from db_app.models import WorkspaceModel

class WorkspaceCreateForm(forms.ModelForm):
  class Meta:
      model = WorkspaceModel
      fields = ("name","tag","user")
      widgets = {
        'name': forms.Textarea(attrs={'rows':3, 'cols':60}),
        'tag': forms.Textarea(attrs={'rows':3, 'cols':60}),
      }
    
    