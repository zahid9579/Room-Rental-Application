from django import forms

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'placeholder': 'Email address'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    tc = forms.BooleanField(required=True, label="I agree to the Terms and Conditions")  # Add TC checkbox

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Password validation
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        # Ensure TC checkbox is checked
        if not cleaned_data.get('tc'):
            raise forms.ValidationError("You must agree to the terms and conditions.")
        
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=50, widget=forms.EmailInput(attrs={'placeholder': 'Email address'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))



