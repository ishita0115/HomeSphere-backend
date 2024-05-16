from rest_framework import serializers

from app1.serializers import UserSerializer
from .models import Listing,Booking,Feedback

class ListingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name',read_only=True)
    profilephoto = serializers.CharField(source='user.profilephoto',read_only=True)

    class Meta:
        model = Listing
        fields = '__all__'

class Listingupdateserializer(serializers.ModelSerializer):
    image1 = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Listing
        fields = ["image1",'title','address','city','country','description','extrafacility','rental_choice','price','bedrooms','bathrooms','sale_type','home_type','latitude','longitude']
        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'Listing', 'which_date', 'booked_by', 'created_at', 'statusmanage']

class FeedbackSerializer(serializers.ModelSerializer):
    feedback_by = serializers.CharField(source='feedback_by.uid')
    user_fname = serializers.CharField(source='feedback_by.first_name',read_only=True)
    user_lname = serializers.CharField(source='feedback_by.last_name',read_only=True)
    profilephoto = serializers.CharField(source='feedback_by.profilephoto',read_only=True)
    class Meta:
        model = Feedback
        fields = ['id', 'feedback_by', 'rating', 'message', 'created_at', 'listing_id','user_fname','user_lname','profilephoto']
