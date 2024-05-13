from .views import ForgotPasswordAPIView, registerview,UserLoginView,UserDetailView,UserProfileView,ContactMessageList,ContactMessageSendAPIView
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
    path('contact/', ContactMessageList.as_view(), name='create_contact_message'),
    path('contact/<int:pk>/', ContactMessageList.as_view(), name='contact-message-delete'),
    path('contact/<int:pk>/send/', ContactMessageSendAPIView.as_view(), name='contact-message-send'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
]