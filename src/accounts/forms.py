from django import forms
from .models import Account, Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'gender']

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Your passwords don\'t match!')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password',
            'gender',
        )
        
        # Add placeholders and Tailwind classes to each field
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Enter First Name',
            'class': 'input input-bordered w-full'
        })
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Enter Last Name',
            'class': 'input input-bordered w-full'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter Email Address',
            'class': 'input input-bordered w-full'
        })
        self.fields['gender'].widget.attrs.update({
            'class': 'select select-bordered w-full'  
        })

        # Add the submit button using Crispy
        self.helper.add_input(Submit('submit', 'Sign Up', css_class='w-full py-2 px-4 bg-blue-700 text-white rounded-md hover:bg-blue-800'))
        
        
        
        
        
        
        
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'photo', 'position']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'bio',
            'photo',
            'position'
        )
        
        # Add placeholders and Tailwind classes to each field
        self.fields['bio'].widget.attrs.update({
            'placeholder': 'Write something about you...',
            'class': 'input input-bordered w-full'
        })
        self.fields['photo'].widget.attrs.update({
            'class': 'input input-bordered w-full'
        })
        self.fields['position'].widget.attrs.update({
            'placeholder': 'Position...Backend, Django developer...etc',
            'class': 'input input-bordered w-full'
        })
     