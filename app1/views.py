from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import generics
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary import CloudinaryImage
from cloudinary import CloudinaryVideo
from .serializers import UserSerializer,UserLoginSerializer
from .models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from app1.renderers import UserRenderer
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
        print(serializer)
        if serializer.is_valid():
            user = serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token': token,'success':True,'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
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
             return Response({'errors' : {'non_field_errors':['Email or Password is not Valid']},'success':False},status=status.HTTP_400_BAD_REQUEST)
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
    
# class UserGoogleLogin(APIView):
#     def post(self, request):
#         # Retrieve user data from the request
#         first_name = request.data.get('first_name')
#         last_name = request.data.get("last_name")
#         email = request.data.get('email')
#         profilephoto_url = request.data.get('profilephoto')

#         # Check if 'name' (first_name) is provided
#         if not first_name:
#             return Response({'error': 'First name is missing in the request'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Check if the user exists
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             # If the user does not exist, create a new user
#             user = User.objects.create_user(email=email, first_name=first_name,last_name=last_name)
        
#         # Update user profile information including the profile photo
#         user.first_name = first_name
#         user.profilephoto = profilephoto_url
#         user.save()

#         # Generate JWT token
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
        
#         # Return user data and token
#         return Response({
#             'user': {
#                 'id': user.id,
#                 'first_name': user.first_name,
#                 'last_name':user.last_name,
#                 'email': user.email,
#                 'profilephoto': user.profilephoto
#             },
#             'token': access_token
#         }, status=status.HTTP_200_OK)
