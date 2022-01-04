from django import forms
from django.forms import fields
from db_app.models import EvaluationModel, TaskModel, WorkspaceModel, StaffWorkspaceModel

class WorkspaceCreateForm(forms.ModelForm):
  class Meta:
      model = WorkspaceModel
      fields = ("name","tag","user")
      widgets = {
        'name': forms.Textarea(attrs={'rows':3, 'cols':60}),
        'tag': forms.Textarea(attrs={'rows':3, 'cols':60}),
      }
    
GEEKS_CHOICES =(
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
)
class SearchTaskForm(forms.Form):
    start_date  = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    due_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    status = forms.ChoiceField(
      choices = GEEKS_CHOICES
    )

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
    
      'name': forms.Textarea(attrs={'rows':3, 'cols':60}),
      'tag': forms.Textarea(attrs={'rows':3, 'cols':60}),
      'due_at': forms.DateInput(format='%d/%m/%Y'),
      'description': forms.Textarea(attrs={'rows':3, 'cols':60}),
      'staff_workspace': forms.widgets.CheckboxSelectMultiple
    }
    
class EvaluationForm(forms.ModelForm):
  class Meta:
    SCORE_CHOICES = zip( range(1,100), range(1,100) )

    model = EvaluationModel
    fields = ("description", "point")
    widgets = {
      'description': forms.Textarea(attrs={'rows':3, 'cols':60}),
      'point':  forms.TextInput(attrs = {
                  'min': 0,
                  'value': 0,
                  'type': 'number',
                  'style': 'max-width: 3em'
                })
    }
      
