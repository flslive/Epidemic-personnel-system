# Generated by Django 4.0.6 on 2022-07-18 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_id', models.CharField(max_length=64, verbose_name='摄像头编号')),
                ('gate', models.SmallIntegerField(choices=[(1, '南门'), (2, '北门')], verbose_name='大门')),
                ('building', models.SmallIntegerField(choices=[(1, '1号楼'), (2, '2号楼'), (3, '3号楼'), (4, '4号楼')], verbose_name='楼')),
                ('floor', models.SmallIntegerField(choices=[(1, '1层'), (2, '2层'), (3, '3层'), (4, '4层'), (5, '5层'), (6, '6层'), (7, '7层'), (8, '8层')], verbose_name='层')),
                ('lift', models.SmallIntegerField(choices=[(1, '1梯'), (2, '2梯')], verbose_name='梯')),
                ('household', models.SmallIntegerField(choices=[(1, '01户'), (2, '02户')], verbose_name='户')),
            ],
        ),
    ]
