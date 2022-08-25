from django.urls import path
from .views import (
    InstituteListView,
    InstituteDetailView,
    InstituteStudentsEvaluations,
    InstituteUpdateView,
    StudentDetailView,
    UserProfileSignup,
    LoginView,
    ChangePasswordView
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("signup/",UserProfileSignup.as_view()),
    path("token/obtain/",LoginView.as_view()),
    path("token/refresh/",TokenRefreshView.as_view()),
    path("student/<uuid:pk>/",StudentDetailView.as_view()),
    path("institutes/",InstituteListView.as_view()),
    path("institutes/<uuid:pk>/update/",InstituteUpdateView.as_view()),
    path('institutes/<uuid:id>/student-evaluations/',InstituteStudentsEvaluations.as_view()),
    path("institutes/<uuid:pk>/",InstituteDetailView.as_view()),
    path('change_password/<uuid:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
]
