from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskCreationForm(forms.Form):
    title = forms.CharField(label='タイトル', max_length=255)
    content = forms.CharField(label='内容', widget=forms.Textarea())

class MemberCreationForm(forms.Form):
    username = forms.CharField(label='username', max_length=255)
    email = forms.CharField(label='email address', max_length=255)
    age=forms.IntegerField(label='age')
    password = forms.CharField(label='password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm password', widget=forms.PasswordInput())

class MemberLoginForm(forms.Form):
    email = forms.CharField(label='email address', max_length=255)
    password = forms.CharField(label='password', widget=forms.PasswordInput())

class MemberUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'age']

        labels = {
            'username': 'Username',
            'email': 'Email address',
            'age': 'Age',
        }
class MemberPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label='Current password',
        widget=forms.PasswordInput
    )
    new_password = forms.CharField(
        label='New password',
        widget=forms.PasswordInput
    )
    confirm_new_password = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput
    )