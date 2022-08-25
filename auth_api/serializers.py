from rest_framework import serializers
from auth_api.models import Institute,Student,UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = {
            'token': super().validate(attrs),
            'email': self.user.email,
            'is_student': self.user.is_student,
            'is_institute': self.user.is_institute,
            'username': self.user.username,
            'id':self.user.id
        }
        if self.user.is_student:
            try:
                data['student_id']=StudentSerializer(Student.objects.get(user_id=self.user.id)).data
            except Student.DoesNotExist:
                pass
        elif self.user.is_institute:
            try:
                data['institute_id']=InstituteSerializer(Institute.objects.get(user_id=self.user.id)).data
            except Institute.DoesNotExist:
                pass

        return data

class UserProfileSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=UserProfile
        fields=['id','email','password','password2','data','is_student','is_institute']
        extra_kwargs={
            'password':{'write_only':True},
            'data':{'write_only':True}
        }
        
    def save(self, **kwargs):
        email=self.validated_data['email']
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        is_student=self.validated_data['is_student']
        is_institute=self.validated_data['is_institute']
        data=self.validated_data['data']
        if password2!=password:
            raise serializers.ValidationError("p1 and p2 not same")
        
        
        if (UserProfile.objects.filter(email=email).exists()):
            raise serializers.ValidationError("email already exists")
        
        account=UserProfile(email=data['email'],is_student=is_student,is_institute=is_institute)
        account.set_password(password)
        account.save()

        inst_id=Institute.get_institute(inst_id=data['institute_id'])
        if inst_id:
            student=Student(
                user_id=account,
                institute_id=inst_id,
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone_number=data['phone_number'],
                address=data['address'],
                gender=data['gender'],
                city=data['city'],
                state=data['state']
            )
            student.save()
            return student
        else:
            account.delete()
            account = UserProfile.objects.none()
            return account


class InstituteSerializer(serializers.ModelSerializer):
    user_id = UserProfileSerializer()
    class Meta:
        model=Institute
        fields="__all__"
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_id']=UserProfileSerializer(instance.user_id).data
        return response

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields="__all__" 

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['institute_id']=InstituteSerializer(instance.institute_id).data
        response['user_id']=UserProfileSerializer(instance.user_id).data
        return response

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserProfile
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance