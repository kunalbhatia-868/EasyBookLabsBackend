from rest_framework import permissions
import jwt
from auth_api.models import Institute, UserProfile
from backend.settings import SECRET_KEY
    
# class isInstitute(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         token=request.META['HTTP_AUTHORIZATION'].split(" ")[1]
#         user_email=jwt.decode(token,SECRET_KEY, algorithms=['HS256'])['user_id']
#         try:
#             user=UserProfile.objects.get(email=user_email)
#         except Institute.DoesNotExist:
#             return False
#         is_institute=user.is_institute
#         return is_institute
        