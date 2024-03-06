from django.contrib.auth.forms import UserCreationForm
from .models import MyUser,Address
from django import forms


# class MyRegisterForm(UserCreationForm):
#     class Meta:
#         model = MyUser
#         fields = ["first_name", "last_name", "email", "password1","password2"]
class MyRegisterForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ["email", "password1", "password2"]


class VerifyCodeForm(forms.Form):
    code = forms.CharField(
        label="کدتایید",
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
    )
class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['city','province','detail','zipcode']
class UserProfile(forms.ModelForm):
    class Meta:
        model=MyUser
        fields=['first_name',"last_name","email"]

