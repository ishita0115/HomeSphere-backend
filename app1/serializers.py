from rest_framework import serializers
from .models import User,ContactMessage
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail

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
    


class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      token = PasswordResetTokenGenerator().make_token(user)
      link = 'http://localhost:3000/reset/'+uid+'/'+token
      body = 'Click Following Link to Reset Your Password '+link
      send_mail(
            'Password Reset',
            f'link click and reset your password: ${body}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
  