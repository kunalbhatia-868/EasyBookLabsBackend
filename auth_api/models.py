import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from auth_api.utils import LowercaseEmailField
from django.contrib.auth.models import AbstractUser
from auth_api.managers import UserProfileManager
from django.http import Http404
# Create your models here.

class UserProfile(AbstractUser):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    username=models.CharField(_('username'),max_length=200)
    is_student=models.BooleanField(default=False)
    is_institute=models.BooleanField(default=False)
    email=LowercaseEmailField(_('email address'),unique=True)
    data=models.JSONField("data",default=dict())
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    
    objects=UserProfileManager()
    
    def __str__(self):
        return self.email
    
    @staticmethod
    def get_users():
        return UserProfile.objects.all()


class Institute(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user_id=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="institutes")
    name=models.CharField(_('name'),max_length=200)
    email=LowercaseEmailField(_('email address'),unique=True)
    phone_number=models.BigIntegerField(_("phone number"))
    address=models.CharField(_("address"),max_length=300)
    city=models.CharField(_("city"),max_length=200)
    state=models.CharField(_("state"),max_length=200)
    is_disabled=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_institutes():
        return Institute.objects.all()
    
    @staticmethod
    def get_institute(inst_id):
        try:
            return Institute.objects.get(id=inst_id)
        except Institute.DoesNotExist:
            return None
    

class Student(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user_id=models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name="students")
    institute_id=models.ForeignKey(Institute,on_delete=models.CASCADE,related_name="students")
    username=models.CharField(_('username'),max_length=200)
    email=LowercaseEmailField(_('email address'),unique=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    phone_number=models.BigIntegerField(_("phone number"))
    address=models.CharField(_("address"),max_length=300)
    gender=models.CharField(_("gender"),max_length=200)
    city=models.CharField(_("city"),max_length=200)
    state=models.CharField(_("state"),max_length=200)
    created_on=models.DateTimeField(auto_now_add=True)
    updated_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    @staticmethod
    def get_student(std_id):
        try:
            return Student.objects.get(id=std_id)
        except Student.DoesNotExist:
            return None