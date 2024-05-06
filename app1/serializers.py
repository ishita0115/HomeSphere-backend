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
    sender = serializers.UUIDField()
    sender_first_name = serializers.CharField(source='sender.first_name', read_only=True)
    sender_email = serializers.EmailField(source='sender.email', read_only=True)
    
    class Meta:
        model = ContactMessage
        fields = ['sender', 'message','created_at','sender_first_name','sender_email','id']

    def create(self, validated_data):
        sender_id = validated_data.pop('sender')
        try:
            sender = User.objects.get(uid=sender_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Sender user not found")
        return ContactMessage.objects.create(sender=sender, **validated_data)