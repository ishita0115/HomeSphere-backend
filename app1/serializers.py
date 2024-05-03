from rest_framework import serializers
from .models import User,ContactMessage
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['first_name','last_name','email','role','mobileno','password','uid','profilephoto']

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value
    
    def create(self,validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        mobileno = validated_data.get('mobileno')
        role = validated_data.get('role')
        print('role ',role)
        password = validated_data.get('password')

        user = User(email=email, first_name=first_name, last_name=last_name,mobileno=mobileno,role=role)
        user.set_password(password)
        user.save()
        
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields=['email','password','first_name']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'