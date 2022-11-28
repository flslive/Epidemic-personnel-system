from django.db import models


class Admin(models.Model):
    # 管理员
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)

    def __str__(self):
        return self.username


class Nurse(models.Model):
    # 医护人员信息
    gender_choice = (
        (1, '男'),
        (2, '女'),
    )
    building_choice = (
        (1, '1号楼'),
        (2, '2号楼'),
        (3, '3号楼'),
        (4, '4号楼'),
    )

    name = models.CharField(verbose_name='姓名', max_length=16)
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice)
    phone_number = models.CharField(verbose_name='手机号', max_length=11)

    building = models.SmallIntegerField(verbose_name='楼', choices=building_choice)

    def __str__(self):
        return self.name


class Resident(models.Model):
    # 住户信息
    gender_choice = (
        (1, '男'),
        (2, '女'),
    )
    category_choices = (
        (1, '阴性人员'),
        (2, '次密接者'),
        (3, '密接者'),
        (4, '阳性人员'),
    )
    building_choice = (
        (1, '1号楼'),
        (2, '2号楼'),
        (3, '3号楼'),
        (4, '4号楼'),
    )
    floor_choice = (
        (1, '1层'),
        (2, '2层'),
        (3, '3层'),
        (4, '4层'),
        (5, '5层'),
        (6, '6层'),
        (7, '7层'),
        (8, '8层'),
    )
    household_choice = (
        (1, '01户'),
        (2, '02户'),
    )
    name = models.CharField(verbose_name='姓名', max_length=16)
    age = models.CharField(verbose_name='年龄', max_length=4)
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice)
    phone_number = models.CharField(verbose_name='手机号', max_length=11)
    id_number = models.CharField(verbose_name='身份证号', max_length=18)
    category = models.SmallIntegerField(verbose_name='人员类别', choices=category_choices, default=1)
    crate_time = models.DateField(verbose_name='核酸时间')
    head = models.ForeignKey(verbose_name='负责人', to='Nurse', on_delete=models.CASCADE)

    building = models.SmallIntegerField(verbose_name='楼', choices=building_choice)
    floor = models.SmallIntegerField(verbose_name='层', choices=floor_choice)
    household = models.SmallIntegerField(verbose_name='户', choices=household_choice)

    def __str__(self):
        return self.name


class Area(models.Model):
    camera_id = models.CharField(verbose_name='摄像头编号', max_length=64)
    gate_choice = (
        (1, '南门'),
        (2, '北门'),
    )
    building_choice = (
        (1, '1号楼'),
        (2, '2号楼'),
        (3, '3号楼'),
        (4, '4号楼'),
    )
    floor_choice = (
        (1, '1层'),
        (2, '2层'),
        (3, '3层'),
        (4, '4层'),
        (5, '5层'),
        (6, '6层'),
        (7, '7层'),
        (8, '8层'),
    )
    lift_choice = (
        (1, '1梯'),
        (2, '2梯'),
    )
    household_choice = (
        (1, '01户'),
        (2, '02户'),
    )
    gate = models.SmallIntegerField(verbose_name='大门', choices=gate_choice)
    building = models.SmallIntegerField(verbose_name='楼', choices=building_choice)
    floor = models.SmallIntegerField(verbose_name='层', choices=floor_choice)
    lift = models.SmallIntegerField(verbose_name='梯', choices=lift_choice)
    household = models.SmallIntegerField(verbose_name='户', choices=household_choice)


class Notice(models.Model):
    title = models.CharField(verbose_name='标题', max_length=32)
    head = models.ForeignKey(verbose_name='发布者', to='Nurse', on_delete=models.CASCADE)
    context = models.CharField(verbose_name='内容', max_length=400)


class Register(models.Model):
    head = models.ForeignKey(verbose_name='住户姓名', to='Resident', on_delete=models.CASCADE)


class Record(models.Model):
    name = models.CharField(verbose_name='name', max_length=32)
    current_time = models.CharField(verbose_name='当前时间', max_length=64)
