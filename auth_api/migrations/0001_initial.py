# Generated by Django 4.1 on 2022-08-25 05:17

import auth_api.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200, verbose_name='username')),
                ('is_student', models.BooleanField(default=False)),
                ('is_institute', models.BooleanField(default=False)),
                ('email', auth_api.utils.LowercaseEmailField(max_length=254, unique=True, verbose_name='email address')),
                ('data', models.JSONField(default={}, verbose_name='data')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('email', auth_api.utils.LowercaseEmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone_number', models.BigIntegerField(verbose_name='phone number')),
                ('address', models.CharField(max_length=300, verbose_name='address')),
                ('city', models.CharField(max_length=200, verbose_name='city')),
                ('state', models.CharField(max_length=200, verbose_name='state')),
                ('is_disabled', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institutes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=200, verbose_name='username')),
                ('email', auth_api.utils.LowercaseEmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('phone_number', models.BigIntegerField(verbose_name='phone number')),
                ('address', models.CharField(max_length=300, verbose_name='address')),
                ('gender', models.CharField(max_length=200, verbose_name='gender')),
                ('city', models.CharField(max_length=200, verbose_name='city')),
                ('state', models.CharField(max_length=200, verbose_name='state')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('institute_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='auth_api.institute')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
