# Generated by Django 4.0.6 on 2022-07-20 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_resident_building_resident_floor_resident_household'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='building',
            field=models.SmallIntegerField(choices=[(1, '1号楼'), (2, '2号楼'), (3, '3号楼'), (4, '4号楼')], verbose_name='楼'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='floor',
            field=models.SmallIntegerField(choices=[(1, '1层'), (2, '2层'), (3, '3层'), (4, '4层'), (5, '5层'), (6, '6层'), (7, '7层'), (8, '8层')], verbose_name='层'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='household',
            field=models.SmallIntegerField(choices=[(1, '01户'), (2, '02户')], verbose_name='户'),
        ),
    ]