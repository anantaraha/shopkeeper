from django import forms
from django.contrib.auth.models import Group, User, AbstractUser
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.db.models import fields
from . import models

class StaffUpdateCredentialForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[AbstractUser.username_validator])
    oldpassword = forms.CharField(label='Old password', required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text='Old password')
    newpassword = forms.CharField(label='New password', required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text='New password')
    confirmpassword = forms.CharField(label='Confirm password', required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text='Confirm password')
    
    class Meta:
        model = models.Staff
        fields = ['username', 'oldpassword', 'newpassword', 'confirmpassword']
    
    def clean_username(self):
        un = self.cleaned_data.get('username', None)
        if User.objects.exclude(pk=self.instance.pk).filter(username=un):
            raise ValidationError('Username already exists. Try using a different username.')
        return un
    
    def clean_oldpassword(self):
        op = self.cleaned_data['oldpassword']
        print(op)
        if op and not models.Staff.objects.get(pk=self.instance.pk).user.check_password(op):
            raise ValidationError('Old password did not match.')
        return op
    
    def clean_newpassword(self):
        np = self.cleaned_data['newpassword']
        if np:
            password_validation.validate_password(np)
        return np
    
    def clean(self):
        data = super().clean()
        op = data.get('oldpassword', None)
        np = data.get('newpassword', None)
        cp = data.get('confirmpassword', None)
        if np or cp:
            if op:
                if np != cp:
                    raise ValidationError('New passwords did not match.')
            else:
                raise ValidationError('Old password is required.')
        return data
    
    def save(self):
        un =  self.cleaned_data.get('username', None)
        pw =  self.cleaned_data.get('newpassword', None)
        user = self.instance.user
        if un:
            user.username = un
        if pw:
            user.set_password(pw)
        user.save()
        return super().save()


class StaffUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='First name', required=True, max_length=150, help_text='First name')
    last_name = forms.CharField(label='Last name', required=True, max_length=150, help_text='Last name')
    email = forms.EmailField(label='Email address',required=True, help_text='Email address')
    first_name.widget = forms.TextInput(attrs={'class': 'form-control'})
    last_name.widget = forms.TextInput(attrs={'class': 'form-control'})
    email.widget = forms.EmailInput(attrs={'class': 'form-control'})

    class Meta:
        model = models.Staff
        fields = ['first_name', 'last_name', 'email', 'born', 'salary', 'address']
        widgets = {
            'born': forms.DateInput(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-select'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class StaffNewForm(forms.ModelForm):
    username = forms.CharField(label='Username', max_length=150, required=True, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[AbstractUser.username_validator])
    first_name = forms.CharField(label='First name', required=True, max_length=150, help_text='First name')
    last_name = forms.CharField(label='Last name', required=True, max_length=150, help_text='Last name')
    email = forms.EmailField(label='Email address',required=True, help_text='Email address')
    username.widget = forms.TextInput(attrs={'class': 'form-control'})
    first_name.widget = forms.TextInput(attrs={'class': 'form-control'})
    last_name.widget = forms.TextInput(attrs={'class': 'form-control'})
    email.widget = forms.EmailInput(attrs={'class': 'form-control'})

    class Meta:
        model = models.Staff
        fields = ['username', 'admin', 'first_name', 'last_name', 'email', 'born', 'salary', 'address']
        widgets = {
            'admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}), 
            'born': forms.SelectDateWidget(attrs={'class': 'form-select'}, years=range(1900, 2100)),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }
    
    def clean_username(self):
        un = self.cleaned_data['username']
        if User.objects.filter(username=un):
            raise ValidationError('Username already exists. Try using a different username.')
        return un
    
    def save(self):
        a = self.cleaned_data.get('admin', False)
        un = self.cleaned_data.get('username', None)
        fn = self.cleaned_data.get('first_name', None)
        ln = self.cleaned_data.get('last_name', None)
        em = self.cleaned_data.get('email', None)
        if not User.objects.filter(username=un):
            u = User.objects.create_user(username=un, password='user1234', first_name=fn, last_name=ln, email=em)
            if a:
                admin_group = Group.objects.get(name='StaffAdmin')
                admin_group.user_set.add(u)
            self.instance.user = u
            return super().save(self)

