import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from auth_api.models import Institute, Student
from django.core.validators import MaxValueValidator, MinValueValidator
from auth_api.utils import LowercaseEmailField
from django.http import Http404
# Create your models here.

class Equipment(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    name = models.CharField(_('name'),max_length = 200)
    description = models.TextField(_('description'),max_length = 1000)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_all_equipments():
        return Equipment.objects.all()


class Experiment(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    name = models.CharField(_('name'),max_length = 200)
    description = models.TextField(_('description'),max_length = 1000)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_experiments():
        return Experiment.objects.all()

    
class LabType(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    name = models.CharField(max_length = 200)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_lab_types():
        return LabType.objects.all()
    
    @staticmethod
    def get_lab_type(id):
        try:
            return LabType.objects.get(id=id)
        except LabType.DoesNotExist:
            return Http404


class Lab(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    name = models.CharField(_('name'),max_length = 200)
    institute_id = models.ForeignKey(Institute,on_delete = models.CASCADE,related_name = "labs")
    admin = models.CharField(_('admin'),max_length = 200)
    type = models.ForeignKey(LabType,on_delete = models.CASCADE,related_name = "labs")
    description = models.TextField(_('description'),max_length = 1000)
    price = models.IntegerField(_('price'))
    rating=models.IntegerField(_('rating'),default=0)
    rating_count=models.BigIntegerField(_('rating count'),default=0)
    equipments = models.ManyToManyField(Equipment,related_name="labs",blank = True)
    experiments = models.ManyToManyField(Experiment,related_name="labs",blank = True)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.name


    @staticmethod
    def get_all_labs():
        return Lab.objects.all()
    
    @staticmethod
    def get_lab(lab_id):
        return Lab.objects.get(lab_id = lab_id)
    
    @staticmethod
    def get_institute_labs(institute_id):
        return Lab.objects.filter(institute_id = institute_id)
        
    @staticmethod
    def get_all_lab_experiments(lab_id):
        return Lab.objects.get(id=lab_id).experiments.all()
    
    @staticmethod
    def get_all_lab_equipments(lab_id):
        return Lab.objects.get(id=lab_id).equipments.all()

class Slot(models.Model):
    class DayChoices(models.TextChoices):
        MONDAY = 'MO',"MONDAY"
        TUESDAY = 'TU',"TUESDAY"  
        WEDNESDAY = 'WE',"WEDNESDAY"
        THURSDAY = 'TH',"THURSDAY"
        FRIDAY = 'FR',"FRIDAY"
        SATURDAY = 'SA',"SATURDAY"
        SUNDAY = 'SU',"SUNDAY"


    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    lab_id = models.ForeignKey(Lab,on_delete = models.CASCADE,related_name = "slots")
    start_time = models.TimeField(_("start time"), blank = True)
    end_time = models.TimeField(_("end time"), blank = True)
    day = models.CharField(max_length = 2,choices = DayChoices.choices)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)

    @staticmethod
    def get_slots():
        return Slot.objects.all()

    @staticmethod
    def get_slot(slot_id):
        return Slot.objects.get(slot_id = slot_id)

    @staticmethod
    def get_lab_slots(lab_id):
        return Slot.objects.filter(lab_id = lab_id)

    @staticmethod
    def get_lab_slots_by_date(lab_id,day):
        slots = Slot.get_lab_slots(lab_id).filter(day=day)
        return slots

class Booking(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    slot_id = models.ForeignKey(Slot,on_delete = models.CASCADE,related_name = "bookings")
    lab_id = models.ForeignKey(Lab,on_delete = models.CASCADE,related_name = "bookings")
    student_id = models.ForeignKey(Student,on_delete = models.CASCADE,related_name = "bookings")
    date = models.DateField()
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    # status

    def __str__(self):
        return str(self.student_id)

    @staticmethod
    def get_bookings():
        return Booking.objects.all()

    @staticmethod
    def get_all_student_bookings(student_id):
        return Student.objects.get(id=student_id).bookings.all()

    @staticmethod
    def get_all_institute_bookings(inst_id):
        institute_labs=Lab.get_institute_labs(institute_id=inst_id)
        return Booking.objects.filter(lab_id__in=institute_labs)
    
    @staticmethod
    def get_all_lab_bookings(lab_id):
        return Booking.objects.filter(lab_id=lab_id)
    
class Rating(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    lab_id = models.ForeignKey(Lab,on_delete = models.CASCADE,related_name = "ratings")
    star  =  models.IntegerField(validators = [MaxValueValidator(5), MinValueValidator(1)])
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.star

    @staticmethod
    def update_lab_rating(lab_id,curr_rating): 
        lab=Lab.objects.get(id=lab_id)
        lab.rating_count+=1
        lab.rating=(lab.rating+curr_rating)/lab.rating_count
        lab.save()

class Professor(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    institute_id = models.ForeignKey(Institute,on_delete = models.CASCADE,related_name = "professors")
    first_name  =  models.CharField(_("first name"), max_length = 150)
    last_name  =  models.CharField(_("last name"), max_length = 150)
    email = LowercaseEmailField(_('email address'),unique = True)
    research_field=models.CharField(_('research field'),max_length=200,blank=True)
    research_description=models.TextField(_('research description'),blank=True)
    qualification=models.CharField(_("qualification"), max_length = 300,default="")
    designation=models.CharField(_("designation"), max_length = 300,default="")

    def __str__(self):
        return self.research_field
        
    @staticmethod
    def get_all_institute_professors(inst_id):
        return Professor.objects.filter(institute_id=inst_id)

    @staticmethod
    def get_professor(p_id):
        try:
            professor=Professor.objects.get(id=p_id)
            return professor
        except Professor.DoesNotExist:
            return None
        
    