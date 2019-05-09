from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.forms import UserCreationForm



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone_no = forms.CharField(required=True)
    bvn = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    username = None

    class Meta:
        model = User
        fields = (
            'first_name', 
            'last_name', 
            'email', 
            'bvn',
            'phone_no',
            'password1', 
            'password2', 
        )

    # def save(self, commit=True):
    #     user = super(SignUpForm, self).save(commit=False)
    #     user.first_name = (self.cleaned_data['first_name']).casefold()
    #     user.last_name = self.cleaned_data['last_name']
    #     user.email = self.cleaned_data['email']
    #     user.is_staff = self.cleaned_data['is_staff']

    #     if commit:
    #         user.save()

    #     return user
