from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from unicodedata import category

from .models import AdvUser
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import user_registrated

class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput)



    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError(
                 'Введенные пароли не совпадают', code='password_mismatch'
            )}
            raise ValidationError(errors)
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        if commit:
            user.save()
        user_registrated.send(RegisterUserForm, instance=user)
        return user

    # def clean_last_name(self):
    #     sur_name = self.cleaned_data['sur_name']
    #     if not sur_name.isalpha():
    #         raise forms.ValidationError("В фамилии не должны присутствовать цифры")
    #     return sur_name
    #
    # def clean_name(self):
    #     n_name = self.cleaned_data['n_name']
    #     if not n_name.isalpha():
    #         raise forms.ValidationError("В имени не должны присутствовать цифры")
    #     return n_name
    #
    # def clean_patronymic(self):
    #     pat_mic = self.cleaned_data['pat_mic']
    #     if not pat_mic.isalpha():
    #         raise forms.ValidationError("В отчестве не должны присутствовать цифры")
    #     return pat_mic
    #
    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if AdvUser.objects.filter(email=email).exists():
    #         raise forms.ValidationError("Пользователь с таким email уже существует")
    #     return email

    class Meta:
        model = AdvUser
        fields = ('sur_name', 'n_name', 'pat_mic', 'username', 'email', 'password1', 'password2', 'ava')
