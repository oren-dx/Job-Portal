from django import forms
from JobPortalApp.models import*
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username','display_name','email','password1','password2','user_type']


class RecruiterProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = RecruitersModel
        fields = '__all__'
        exclude = ['recruiter']


class SeekerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = SeekeerModel
        fields = '__all__'
        exclude = ['seeker']
        
class JobPostForm(forms.ModelForm):
    class Meta:
        model =  JobPostModel
        fields = '__all__'
        exclude = ['post_by']
        widgets = {
            'deadline': forms.DateInput(attrs={'type':'date'})
        }
        
class ApplyJobForm(forms.ModelForm):
    class Meta:
        model = ApplyJobModel
        fields = ['resume']