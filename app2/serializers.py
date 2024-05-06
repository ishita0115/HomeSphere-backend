from rest_framework import serializers
from .models import Listing,Booking

class ListingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name',read_only=True)
    profilephoto = serializers.CharField(source='user.profilephoto',read_only=True)
    class Meta:
        model = Listing
        fields = '__all__'


        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'Listing', 'which_date', 'booked_by', 'created_at','statusmanage']