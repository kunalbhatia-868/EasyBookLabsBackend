from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,generics
from auth_api.models import Institute, Student, UserProfile
from auth_api.serializers import StudentSerializer, UserProfileSerializer,InstituteSerializer,LoginSerializer,ChangePasswordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from booking_api.models import StudentEvaluation
from booking_api.serializers import StudentEvaluationSerializer

# from user.permissions import isInstitute
# Create your views here.

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class UserProfileSignup(APIView):
    def post(self,request):
        serializer=UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

   
class StudentDetailView(APIView):
    def get(self,request,pk):
        student=Student.get_student(std_id=pk)
        serializer=StudentSerializer(student)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class InstituteListView(APIView):
    def get(self,request):
        institute=Institute.get_all_institutes()
        serializer=InstituteSerializer(institute,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)

class InstituteDetailView(APIView):
    def get(self,request,pk):
        institute=Institute.get_institute(inst_id=pk)
        serializer=InstituteSerializer(institute)
        return Response(data=serializer.data,status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = UserProfile.get_users()
    permission_classes=[IsAuthenticated]
    serializer_class = ChangePasswordSerializer

class InstituteUpdateView(generics.UpdateAPIView):
    queryset = Institute.get_all_institutes()
    permission_classes=[IsAuthenticated]
    # permission_classes=[IsAuthenticated,isInstitute]
    serializer_class = InstituteSerializer

class InstituteStudentsEvaluations(APIView):
    def get(self,request,id):
        institute_students=Institute.objects.get(id=id).student_set.all()
        student_evaluations=StudentEvaluation.objects.filter(booking_id__student_id__in=institute_students)
        serializer=StudentEvaluationSerializer(student_evaluations,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)