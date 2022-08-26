from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView,DestroyAPIView
from booking_api.helper import dateToDay
from booking_api.helper import get_lab_text_search,get_experiment_text_search,get_equipment_text_search,get_research_text_search
from booking_api.models import (
    Equipment,
    Experiment,
    Lab, 
    LabType,
    Professor,
    Rating,
    Slot,
    Booking,
    Confirmation,
    StudentEvaluation
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from booking_api.serializers import (
    BookingSerializer,
    EquipmentSerializer,
    ExperimentSerializer,
    LabSerializer,
    LabTypeSerializer,
    ProfessorSerializer,
    RatingSerializer,
    SlotSerializer,
    ConfirmationSerializer,
    StudentEvaluationSerializer
)
from auth_api.models import Institute

# Create your views here.

class EquipmentListCreateView(APIView):
    def get(self,request):
        equipment_list=Equipment.get_all_equipments()
        serializer=EquipmentSerializer(equipment_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        equipments=request.data['equipments']
        new_equipments=request.data['new_equipment']
        lab_id=request.data['lab_id']
        for equipment_id in equipments:
            equipment=Equipment.objects.get(id=equipment_id)
            lab=Lab.objects.get(id=lab_id)
            lab.equipments.add(equipment)
            lab.save()

        for equipment in new_equipments:
            equipment=Equipment(name=equipment.name,description=equipment.description)
            equipment.save()
            lab=Lab.objects.get(id=lab_id)
            lab.equipments.add(equipment)
            lab.save()

        return Response(status=status.HTTP_201_CREATED)

class EquipmentRUDView(RetrieveUpdateDestroyAPIView):
    queryset=Equipment.get_all_equipments()
    serializer_class=EquipmentSerializer


class ExperimentListCreateView(APIView):
    def get(self,request):
        experiment_list=Experiment.get_all_experiments()
        serializer=ExperimentSerializer(experiment_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        experiments=request.data['experiments']
        new_experiments=request.data['new_experiment']
        lab_id=request.data['lab_id']
        for experiment_id in experiments:
            experiment=Experiment.objects.get(id=experiment_id)
            lab=Lab.objects.get(id=lab_id)
            lab.experiments.add(experiment)
            lab.save()

        for experiment in new_experiments:
            experiment=Experiment(name=experiment.name,description=experiment.description)
            experiment.save()
            lab=Lab.objects.get(id=lab_id)
            lab.experiments.add(experiment)
            lab.save()

        return Response(status=status.HTTP_201_CREATED)
        
class ExperimentRUDView(RetrieveUpdateDestroyAPIView):
    queryset=Experiment.get_all_experiments()
    serializer_class=ExperimentSerializer


class LabExperimentsView(APIView):
    def get(self,request,id):
        if not id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        experiment_list=Lab.get_all_lab_experiments(lab_id=id)
        serializer=ExperimentSerializer(experiment_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)



class LabEquipmentsView(APIView):
    def get(self,request,id):
        if not id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        equipment_list=Lab.get_all_lab_equipments(lab_id=id)
        serializer=EquipmentSerializer(equipment_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LabTypeListCreateView(APIView):
    def get(self,request):
        lab_type_list=LabType.get_all_lab_types()
        serializer=LabTypeSerializer(lab_type_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=LabTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LabListCreateView(APIView):
    def get(self,request):
        lab_list=Lab.get_all_labs()
        serializer=LabSerializer(lab_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=LabSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LabRUDView(RetrieveUpdateDestroyAPIView):
    queryset=Lab.get_all_labs()
    serializer_class=LabSerializer

class InstituteLabsView(APIView):
    def get(self,request,id):
        if not id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        lab_list=Lab.get_institute_labs(institute_id=id)
        serializer=LabSerializer(lab_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class InstituteProfessorsListCreateView(APIView):
    def get(self,request,id):
        institute_professors_list=Professor.get_all_institute_professors(inst_id=id)
        serializer=ProfessorSerializer(institute_professors_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,id):
        request.data['institute_id']=id
        serializer=ProfessorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class SlotListCreateView(APIView):
    def get(self,request,id):
        lab_slots_list=Slot.get_lab_slots(lab_id=id)
        serializer=SlotSerializer(lab_slots_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,id):
        start_time=request.data['start_time']
        end_time=request.data['end_time']
        lab_id=id
        days=request.data['days']
        
        return_data=[]
        for day in days: 
            slot_data={
                'start_time': start_time,
                'end_time': end_time,
                'day': day,
                'lab_id': lab_id
            } 
            serializer=SlotSerializer(data=slot_data)
            if(serializer.is_valid()):
                serializer.save()
                return_data.append(serializer.data)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        return Response(return_data,status=status.HTTP_201_CREATED)    

class LabSlotDateListView(APIView):
    def get(self,request,id,date):
        day=dateToDay(date)
        lab_slots_list=Slot.get_lab_slots_by_date(lab_id=id,day=day)
        serializer=SlotSerializer(lab_slots_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

# 2022-08-21 Booking
# 21082022  input

class SlotDeleteView(DestroyAPIView):
    queryset=Slot.get_slots()
    serializer_class=SlotSerializer

class BookingStudentListCreateView(APIView):
    def get(self,request,id):
        student_booking_list=Booking.get_all_student_bookings(student_id=id)
        serializer=BookingSerializer(student_booking_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self,request,id):
        request.data['student_id']=id
        serializer=BookingSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
class BookingInstituteListView(APIView):
    def get(self,request,id):
        institute_booking_list=Booking.get_all_institute_bookings(inst_id=id)
        serializer=BookingSerializer(institute_booking_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class BookingLabListView(APIView):
    def get(self,request,id):
        lab_booking_list=Booking.get_all_lab_bookings(lab_id=id)
        serializer=BookingSerializer(lab_booking_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class BookingDeleteView(DestroyAPIView):
    queryset=Booking.get_bookings()
    serializer_class=BookingSerializer

class RatingCreateRetrieveView(APIView):
    def get(self,request,id):
        return Lab.objects.get(id=id).rating
    
    def post(self,request,id):
        request.data['lab_id']=id
        serializer=RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            Rating.update_lab_rating(id,request.data['star'])
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    

class SearchView(APIView):
    def get(self,request):
        text=request.GET.get('text') or ''
        filter=request.GET.get('filter')

        labs_set=None 
        if filter=='experiment':
            labs_set=get_experiment_text_search(text)
        elif filter=='equipment':
            labs_set=get_equipment_text_search(text)
        else:
            labs_set=get_lab_text_search(text)    
        serializer=LabSerializer(labs_set,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ResearchSearchView(APIView):
    def get(self,request):
        text=request.GET.get('text') or ''
        research_set=get_research_text_search(text) 
        serializer=ProfessorSerializer(research_set,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class LabTypeSearch(APIView):
    def get(self,request):
        text=request.GET.get('text') or ''
        labs_set=Lab.get_labs_by_lab_type(text) 
        serializer=LabSerializer(labs_set,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class ResearchDetailView(APIView):
    def get(self,request,id):
        research_professor=Professor.get_professor(p_id=id)
        if research_professor:
            serializer=ProfessorSerializer(research_professor)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
        

class ConfirmationListCreateView(APIView):
    def post(self,request,id):
        request.data['reciever_institute']=id
        serializer=ConfirmationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,id):
        confirmations=Confirmation.objects.filter(reciever_institute__id=id)
        serializer=ConfirmationSerializer(confirmations,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
class ConfirmationUpdateView(APIView):
    def patch(self,request,id):
        confirmation=Confirmation.objects.get(id=id)
        booking=Booking.objects.get(booking_id=confirmation.booking_id.id)
        decision=request.data['decision']
        if decision=="yes":
            booking.status=Booking.StatusChoices.SUCCESS
            booking.save()
            confirmation.status=Confirmation.StatusChoices.SUCCESS
        else:
            confirmation.status=Confirmation.StatusChoices.REJECTED
        confirmation.save()
        return confirmation

class BookingEvaluation(APIView):
    def post(self,request,id):
        request.data['booking_id']=id
        serializer=StudentEvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

            