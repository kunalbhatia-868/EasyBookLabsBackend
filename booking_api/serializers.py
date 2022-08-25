from rest_framework import serializers

from auth_api.serializers import InstituteSerializer,StudentSerializer
from .models import (
    LabType,
    Lab,    
    Equipment,
    Experiment,
    Rating,
    Slot,
    Booking,
    Rating,
    Professor
)

class LabTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=LabType
        fields="__all__"

class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lab
        fields="__all__"
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['institute_id'] = InstituteSerializer(instance.institute_id).data
        response['type']=LabTypeSerializer(instance.type).data
        response['experiments']=ExperimentSerializer(instance.experiments,many=True).data
        response['equipments']=EquipmentSerializer(instance.equipments,many=True).data
        return response

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Equipment
        fields="__all__"

class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Experiment
        fields="__all__"


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model=Slot
        fields="__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['lab_id']=LabSerializer(instance.lab_id).data
        return response

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields="__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['lab_id']=LabSerializer(instance.lab_id).data
        response['slot_id']=SlotSerializer(instance.slot_id).data
        response['student_id']=StudentSerializer(instance.student_id).data
        return response

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Rating
        fields="__all__"

        def to_representation(self, instance):
            response = super().to_representation(instance)
            response['lab_id']=LabSerializer(instance.lab_id).data
            return response

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Professor
        fields=['id','institute_id','first_name','last_name','research_description','research_field','qualification','designation']

        def to_representation(self, instance):
            response = super().to_representation(instance)
            response['institute_id']=InstituteSerializer(instance.institute_id).data
            return response