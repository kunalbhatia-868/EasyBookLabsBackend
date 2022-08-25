from django.contrib import admin
from booking_api import models
# Register your models here.

admin.site.register([
    models.Equipment,
    models.Experiment,
    models.Lab,
    models.LabType,
    models.Slot,
    models.Booking,
    models.Rating,
    models.Professor,
])
