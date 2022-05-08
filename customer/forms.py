from django import forms
from allauth.account.forms import SignupForm
from .models import CustomerModel

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, required=True, label='First Name')
    last_name = forms.CharField(max_length=30, required=True, label='Last Name')
    email = forms.CharField(max_length=100, required=True, label='E-mail address')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        return user


# create HTML form based on CustomerModel (models.py)
class NewCustomerForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = CustomerModel
        fields = "__all__"
