import datetime
import calendar
from django.db.models import Q
from booking_api.models import Equipment, Experiment,Lab, Professor


def dateToDay(date):
    format_date=datetime.datetime.strptime(date, "%d%m%Y").date()
    day=calendar.day_name[format_date.weekday()]
    return day.upper()[:2]


def get_lab_text_search(text):
    labs=Lab.objects.filter(Q(name__icontains=text) | Q(description__icontains=text)) 
    return labs

def get_experiment_text_search(text):
    experiments=Experiment.objects.filter(Q(name__icontains=text.lower()) | Q(description__icontains=text.lower()))
    labs=[]
    print(Lab.get_all_labs())
    for lab in Lab.get_all_labs():
        print("a")
        lab_exp=lab.experiments.all()
        print(lab_exp)
        if lab_exp.intersection(experiments).count()>0:
            print(lab)
            labs.append(lab.id)
    labs_set=Lab.objects.filter(id__in=labs)
    return labs_set

def get_equipment_text_search(text):
    equipments=Equipment.objects.filter(Q(name__icontains=text.lower()) | Q(description__icontains=text.lower()))
    labs=[]
    for lab in Lab.get_all_labs():
        lab_eq=lab.equipments.all()
        if lab_eq.intersection(equipments).count()>0:
            labs.append(lab.id)
    labs_set=Lab.objects.filter(id__in=labs)
    return labs_set

def get_research_text_search(text):
    professors=Professor.objects.filter(Q(research_field__icontains=text) | Q(research_description__icontains=text)) 
    return professors
