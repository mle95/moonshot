from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    email = forms.CharField(max_length=100, required=True, label='E-mail address')
    balance = forms.IntegerField(required=True, min_value=5, label='Amount deposit (minimum is $5)')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.balance = self.cleaned_data['balance']
        user.save()
        return user
