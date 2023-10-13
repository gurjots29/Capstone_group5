from django import forms

<<<<<<< HEAD
=======
from apps.users.models import Post, Comment

>>>>>>> 5afe1c1 (Pushing for POST API and Comments API)
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

<<<<<<< HEAD
    
=======
class SignupForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please enter the same password in both fields.")
        
        return cleaned_data


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'file']

class CommentForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    class Meta:
        model = Comment
        fields = ['text']
>>>>>>> 5afe1c1 (Pushing for POST API and Comments API)
