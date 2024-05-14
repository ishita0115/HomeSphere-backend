from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary import CloudinaryImage
from cloudinary import CloudinaryVideo

from app1.permissions import IsAdminUser
from .serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserPasswordResetSerializer, UserSerializer,UserLoginSerializer,ContactMessageSerializer
from .models import User,ContactMessage
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from app1.renderers import UserRenderer
from django.core.mail import send_mail
# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'uid': str(user.uid),
    }
    
class registerview(APIView):
    renderer_classes=[UserRenderer]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token': token,'success':True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        print(request)
        # serializer = UserLoginSerializer(data=request.data)
        serializer = UserLoginSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user:
              token = get_tokens_for_user(user)
              queryset = User.objects.get(email=user.email)
              userdata = UserSerializer(queryset)
              return Response({'token':token,'success':True,'msg' : 'Login success','user': userdata.data},status=status.HTTP_200_OK)
            else:
              return Response({'errors' : {'email':['Email or Password is not correct match']},'success':False},status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):  # Changed the method signature to accept pk
        try:
            userdata = User.objects.get(pk=pk)  # Retrieve the listing using pk
            serializer = UserSerializer(userdata)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': "User with this primary key does not exist or is not published"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, uid, format=None):
        try:
            user = User.objects.get(uid=uid)
            serializer = UserSerializer(user, data=request.data, partial=True)
            print(request.data)
            if serializer.is_valid():
                # Save the changes to the user object
                serializer.save()
                print(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,uid, format=None):
        try:
            userdata = User.objects.get(uid=uid) 
            print(userdata)
            serializer = UserSerializer(userdata)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class ContactMessageList(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        admin = User.objects.filter(role=User.ADMIN).first()  # Assuming there's only one admin
        if not admin:
            return Response({"error": "No admin found"}, status=status.HTTP_404_NOT_FOUND)

        sender_id = request.data.get('sender')
        print(sender_id)
        serializer = ContactMessageSerializer(data=request.data, context={'sender_id': sender_id, 'recipient': admin})
        if serializer.is_valid():
            
            serializer.save()
            print(serializer.data)
            return Response({'data':serializer.data}, status=status.HTTP_201_CREATED)
        else:
            # Return error response with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # Retrieve all contact messages and include related user information
        contact_messages = ContactMessage.objects.all()
        serializer = ContactMessageSerializer(contact_messages, many=True)
        return Response({"data":serializer.data})
    
    def delete(self, request, pk):
        try:
            message = ContactMessage.objects.get(pk=pk)
            message.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ContactMessage.DoesNotExist:
            return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)
        

class ContactMessageSendAPIView(APIView):
    def post(self, request, pk):
        try:
            original_message = ContactMessage.objects.get(pk=pk)
            sender = original_message.sender
            # Create a new message object to send back to the user
            reply_message = ContactMessage.objects.create(sender=sender, message=request.data['message'])
            reply_message.save()
            return Response(status=status.HTTP_201_CREATED)
        except ContactMessage.DoesNotExist:
            return Response({"error": "Original message not found"}, status=status.HTTP_404_NOT_FOUND)
    def put(self, request, pk):
        try:
            print(request)
            message = ContactMessage.objects.get(pk=pk)
            # Update the message to mark it as acknowledged
            message.acknowledged = True
            print(message)
            message.save()
            serializer = ContactMessageSerializer(message)
            return Response(serializer.data)
        except ContactMessage.DoesNotExist:
            return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
  

class UserListView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)