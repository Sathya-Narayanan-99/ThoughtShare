# Generated by Django 3.2.2 on 2021-05-09 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blogger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('profile_pic', models.ImageField(upload_to='')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('category', models.CharField(choices=[('Bussiness', 'Bussiness'), ('Growth', 'Growth')], max_length=200)),
                ('date_published', models.DateTimeField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.blogger')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('date_published', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.post')),
            ],
        ),
    ]