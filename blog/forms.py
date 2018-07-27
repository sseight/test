from django import forms
from django.forms import widgets
from .models import *
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


class RegisterForm(forms.Form):
    user=forms.CharField(min_length=5,error_messages={"required":"该字段不能为空","min_length":"最短为5个字符"},
                         widget=widgets.TextInput(attrs={"class":"form-control","placeholder":"用户名"})
                         )
    pwd=forms.CharField(min_length=8,error_messages={"required":"该字段不能为空","min_length":"最短为个8字符"},
                        widget=widgets.PasswordInput(attrs={"class":"form-control","placeholder":"密码"})
                        )
    repeat_pwd=forms.CharField(min_length=8,error_messages={"required":"该字段不能为空","min_length":"最短为个8字符"},
                        widget=widgets.PasswordInput(attrs={"class":"form-control","placeholder":"确认密码"})
                               )
    email=forms.EmailField(error_messages={"required":"该字段不能为空","invalid":"格式错误"},
                           widget=widgets.EmailInput(attrs={"class":"form-control","placeholder":"邮箱"})
                           )

    def clean_user(self):
        val=self.cleaned_data.get("user")
        if not UserInfo.objects.filter(username=val):
            return val
        else:
            raise ValidationError("用户已存在！")

    def clean(self):
        pwd=self.cleaned_data.get("pwd")
        repeat_pwd=self.cleaned_data.get("repeat_pwd")
        if pwd and repeat_pwd:
            if pwd==repeat_pwd:
                return self.cleaned_data
            else:
                raise ValidationError("两次密码不一致")
        else:
            return self.cleaned_data


