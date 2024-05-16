from .views import SendPasswordResetEmailView, UserChangePasswordView, UserPasswordResetView, registerview,UserLoginView,UserDetailView,UserProfileView,ContactMessageList,ContactMessageSendAPIView,UserListView
from django.urls import path

# from dj_rest_auth.jwt_auth import get_refresh_view
# from rest_framework_simplejwt.views import TokenVerifyView
urlpatterns = [
    
    
    path('register/',registerview.as_view()),
    path('login/',UserLoginView.as_view(), name='login'),
    path('UserDetailView/<int:pk>/', UserDetailView.as_view(), name='UserDetailView'), 
    path('UserProfileView/<uuid:uid>/', UserProfileView.as_view(), name='UserProfileView'),
    path('usersupdate/<uuid:uid>/', UserDetailView.as_view(), name='user-detail'),
    path('contact/', ContactMessageList.as_view(), name='create_contact_message'),
    path('contact/<int:pk>/', ContactMessageList.as_view(), name='contact-message-delete'),
    path('contact/<int:pk>/send/', ContactMessageSendAPIView.as_view(), name='contact-message-send'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('userslist/', UserListView.as_view(), name='userlist'),
    path('contact/<int:message_id>/status/', ContactMessageSendAPIView.as_view(), name='get_message_status'),
]