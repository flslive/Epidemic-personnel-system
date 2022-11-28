from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm
from app01.utils.encrypt import md5


class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def clean_username(self):
        txt_username = self.cleaned_data['username']
        exists = models.Admin.objects.filter(username=txt_username).exists()
        if exists:
            raise ValidationError('用户名已存在')
        return txt_username


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']

    def clean_username(self):
        txt_username = self.cleaned_data["username"]
        exists = models.Admin.objects.exclude(id=self.instance.pk).filter(username=txt_username).exists()
        if exists:
            raise ValidationError("用户名已存在")
        return txt_username


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd)

        if exists:
            raise ValidationError('密码不能与之前的一致')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm:
            raise ValidationError('两次输入的密码不一致')
        # 下面return的confirm就是返回数据库的值
        return confirm


class Loginform(BootStrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True
    )

    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class NurseModelForm(BootStrapModelForm):
    phone_number = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.Nurse
        fields = ['name', 'gender', 'phone_number', 'building']

    def clean_name(self):
        txt_name = self.cleaned_data['name']
        exists = models.Nurse.objects.filter(name=txt_name).exists()
        if exists:
            raise ValidationError('该医护人员姓名已存在')
        return txt_name


class NurseEditModelForm(BootStrapModelForm):
    phone_number = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )

    class Meta:
        model = models.Nurse
        fields = ['name', 'gender', 'phone_number', 'building']

    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        exists = models.Nurse.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()
        if exists:
            raise ValidationError("该医护人员姓名已存在")
        return txt_name


class ResidentModelForm(BootStrapModelForm):
    phone_number = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )
    id_number = forms.CharField(
        label="身份证号",
        validators=[RegexValidator(r"^[1-9]\d{13,16}[a-zA-Z0-9]{1}$", '身份证号格式错误'), ],
    )

    class Meta:
        model = models.Resident
        fields = ['name', 'age', 'gender', 'phone_number', 'id_number',
                  'category', 'crate_time', 'head', 'building', 'floor',
                  'household']

    def clean_name(self):
        txt_name = self.cleaned_data['name']
        exists = models.Resident.objects.filter(name=txt_name).exists()
        if exists:
            raise ValidationError('该住户姓名已存在')
        return txt_name


class ResidentEditModelForm(BootStrapModelForm):
    phone_number = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    )
    id_number = forms.CharField(
        label="身份证号",
        validators=[RegexValidator(r"^[1-9]\d{13,16}[a-zA-Z0-9]{1}$", '身份证号格式错误'), ],
    )

    class Meta:
        model = models.Resident
        fields = ['name', 'age', 'gender', 'phone_number', 'id_number',
                  'category', 'crate_time', 'head', 'building', 'floor',
                  'household']

    def clean_name(self):
        txt_name = self.cleaned_data["name"]
        exists = models.Resident.objects.exclude(id=self.instance.pk).filter(name=txt_name).exists()
        if exists:
            raise ValidationError("住户姓名已存在")
        return txt_name


class AreaModelForm(BootStrapModelForm):
    class Meta:
        model = models.Area
        exclude = ['camera_id']


class NoticeModelForm(BootStrapModelForm):
    class Meta:
        model = models.Notice
        fields = ['title', 'head', 'context']


class NoticeDetailModelForm(BootStrapModelForm):
    class Meta:
        model = models.Notice
        fields = ['context']


class NoticeEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Notice
        fields = ['title', 'head', 'context']


class RegisterModelForm(BootStrapModelForm):
    class Meta:
        model = models.Register
        fields = ['head']


class RegisterEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Register
        fields = ['head']


class RecordModelForm(BootStrapModelForm):
    class Meta:
        model = models.Record
        fields = ['name', 'current_time']
