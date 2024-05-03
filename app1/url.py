from .views import registerview,UserLoginView,UserDetailView,UserProfileView
from django.urls import path

# from dj_rest_auth.jwt_auth import get_refresh_view
# from rest_framework_simplejwt.views import TokenVerifyView
urlpatterns = [
    
    
    path('register/',registerview.as_view()),
    path('login/',UserLoginView.as_view(), name='login'),
    # path('login/google/',UserGoogleLogin.as_view(), name='login'),
    path('UserDetailView/<int:pk>/', UserDetailView.as_view(), name='UserDetailView'), 
    path('UserProfileView/<uuid:uid>/', UserProfileView.as_view(), name='UserProfileView'),
    path('usersupdate/<uuid:uid>/', UserDetailView.as_view(), name='user-detail'),
]