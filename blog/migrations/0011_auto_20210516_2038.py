# Generated by Django 3.2.2 on 2021-05-16 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20210513_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Growth', 'Growth'), ('Others', 'Others'), ('Bussiness', 'Bussiness')], max_length=200),
        ),
    ]
