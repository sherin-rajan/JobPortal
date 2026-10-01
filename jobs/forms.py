from django import forms
from jobs.models import Jobs,Profile

class JobForm(forms.ModelForm):
    class Meta:
        model=Jobs
        fields='__all__'
        exclude=['slug']

        widgets={
            'end_date':forms.TextInput(attrs={
                'type':'date',
                "class":'form'
            })
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['dob','phone','place','qualification','headline']

        
