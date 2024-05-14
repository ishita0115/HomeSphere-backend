
from http.client import NOT_FOUND
from django.forms import IntegerField
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Listing,Booking,Feedback
from app1.models import User
from .serializers import FeedbackSerializer, ListingSerializer,BookingSerializer
from app1.serializers import UserSerializer
from .permissions import IsSellerUser, IsAdminUser

class ManageListingView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request,*args, **kwargs):
        try:
            country = request.GET.get('country', None)
            city = request.GET.get('city', None)
            sale_type = request.GET.get('sale_type', None)
            bedrooms = request.GET.get('bedrooms', None)
            home_type = request.GET.get('home_type', None)
            address = request.GET.get('address', None)
            min_price = request.GET.get('min_price', None)
            max_price = request.GET.get('max_price', None)

            # Get all properties if no search parameters are provided
            if not any([country, city, sale_type, bedrooms, home_type, address, min_price, max_price]):
                properties = Listing.objects.all()
            else:
                # Filter properties based on provided search parameters
                properties = Listing.objects.all()

                if country:
                    properties = properties.filter(country__icontains=country)

                if city:
                    properties = properties.filter(city__icontains=city)

                if sale_type:
                    properties = properties.filter(sale_type__icontains=sale_type)

                if bedrooms:
                    properties = properties.filter(bedrooms=bedrooms)

                if home_type:
                    properties = properties.filter(home_type__icontains=home_type)

                if address:
                    properties = properties.filter(address__icontains=address)

                if min_price:
                    properties = properties.filter(price__gte=min_price)

                if max_price:
                    properties = properties.filter(price__lte=max_price)

            # Serialize the properties
            serializer = ListingSerializer(properties, many=True)
            
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):   
        try:
            authenticated_user = request.user
            user_pk = authenticated_user.pk 
            try:
                user_instance = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                raise NOT_FOUND("User not found")

            serializer = ListingSerializer(data=request.data)
            
            if serializer.is_valid():
                # Associate the listing with the user instance
                serializer.save(user=user_instance)
                print('insied if')
                return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e: # type: ignore
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    def put(self, request, pk, format=None):
        try:
            listing = Listing.objects.get(pk=pk)
            if request.user != listing.user:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
            serializer = ListingSerializer(listing, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Listing.DoesNotExist:
            return Response({'error': 'Listing does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, format=None):
        try:
            listing = Listing.objects.get(pk=pk)
            if request.user != listing.user:
                return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
            listing.delete()
            return Response({'success': 'Listing deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Listing.DoesNotExist:
            return Response({'error': 'Listing does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListingDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, format=None):  # Changed the method signature to accept pk
        print(pk)
        try:
            listing = Listing.objects.get(pk=pk)
              # Retrieve the listing using pk
            serializer = ListingSerializer(listing)
            
            return Response(serializer.data, status=status.HTTP_200_OK)    
        except Exception as e:
            
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserListingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        try:
            listings = Listing.objects.filter(user_id=user_id)
            serializer = ListingSerializer(listings, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class myListingAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request ,uid ):
        try:
            listings = Listing.objects.filter(user__uid=uid)
            serializer = ListingSerializer(listings, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class BookingListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                # Set the seller_listing field of the serializer to the authenticated user
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_message = {'error': str(e)}
            return Response(error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, uid):
        booking = get_object_or_404(Booking, id=uid)
        if(booking):
            booking.delete()
            Response({'message': 'successfully done booking .'}, status=status.HTTP_200_OK)
        return Response({'message': 'Booking deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
    

class MyBooking(APIView):
        permission_classes = [IsAuthenticated]
        def get(self, request, uid):
            try:
                user_bookings = Booking.objects.filter(booked_by=uid)
                listing_ids = []
                for booking in user_bookings:
                     listing_ids.append(booking.Listing.id)
                listings = Listing.objects.filter(id__in=listing_ids)
                listing_serializer = ListingSerializer(listings, many=True)
                serializer = BookingSerializer(user_bookings, many=True)
                return Response({'data': serializer.data,"listing_data":listing_serializer.data})
            except Exception as e:
                return Response({'error': str(e)}, status=500)

class sellerbookingmanage(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            user = request.user
            bookings = Booking.objects.filter(Listing__user__email=user.email)
            serializer = BookingSerializer(bookings, many=True, context={'request': request})
            listing_ids = []
            for booking in bookings:
                listing_ids.append(booking.Listing.id)
                listings = Listing.objects.filter(id__in=listing_ids)
                listing_serializer = ListingSerializer(listings, many=True)
            buyer_data = []
            for booking in bookings:
                buyer_id = booking.booked_by
                buyer = User.objects.get(uid=buyer_id)
                buyer_data.append({
                    'buyer_id': buyer.uid,
                    'buyer_fname': buyer.first_name,
                    'buyer_email': buyer.email,
                    'buyer_lname': buyer.last_name,
                })
            return Response({
                'data': serializer.data,
                "listing_data":listing_serializer.data,
                'buyer_data': buyer_data,
                
            })
        except Exception as e:
            error_message = {'error': str(e)}
            return Response(error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, booking_id, action, format=None):
        try:
            booking = Booking.objects.get(pk=booking_id)
            if action == 'accept':
                booking.statusmanage = 'success'
            elif action == 'reject':
                message = request.data.get('message', '')
                booking.statusmanage = message  # Set status to the rejection message
                booking.reject_message = message
            booking.save()
            serializer = BookingSerializer(booking)
            return Response(serializer.data)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

class FavoriteAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    def post(self, request, pk):
        try:
            listing = Listing.objects.get(pk=pk)
        except Listing.DoesNotExist:
            return Response({"error": "listing not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user in listing.favorited.all():
                listing.favorited.remove(request.user)
                return Response({'is_favorite': False})
        else:
                listing.favorited.add(request.user)
                return Response({'is_favorite': True})
     
class myallfavview(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id, format=None):
        user = get_object_or_404(User, uid=user_id)
        favorite_listings = user.favorites.all()
        serializer = ListingSerializer(favorite_listings, many=True)
        return Response({'data': serializer.data},status=status.HTTP_200_OK)
    

class listing_coordinates_api(APIView):
     def get(self, request):
        try:
            listings = Listing.objects.all()
            coordinates = []
            for listing in listings:
                coordinate = {
                    'latitude': listing.latitude,
                    'longitude': listing.longitude,
                    'address': listing.address,
                    'city': listing.city,
                    'country': listing.country,
                    'image1_url': listing.image1.url if listing.image1 else None
                }
                coordinates.append(coordinate)
            return Response({'coordinates': coordinates}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class fetchbookingstatus(APIView):
    def get(self, request, pk):
        booking = Booking.objects.get(pk=pk)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)
    
class SubmitFeedbackAPIView(APIView):
    def post(self, request, format=None):
        print(request.user)
        authenticated_user_id = request.data['feedback_by']  # Access the value using dictionary key access
        print(authenticated_user_id)
        user_instance = User.objects.get(uid=authenticated_user_id)
        print(user_instance)
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(feedback_by=user_instance)  # Make sure your serializer's field is named 'feedback_by'
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request, listing_id, format=None):
        try:
            # Assuming Rating model has a field named 'listing_id' to store the listing ID
            ratings = Feedback.objects.filter(listing_id=listing_id).values_list('rating', flat=True)
            ratings_list = list(ratings)
            total_ratings = len(ratings_list)
            if total_ratings > 0:
                average_rating = sum(ratings_list) / total_ratings
            else:
                average_rating = 0
            
            return Response({'average_rating': average_rating}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ListingFeedbackAPIView(APIView):
    def get(self, request, listing_id):
        try:
            feedbacks = Feedback.objects.filter(listing_id=listing_id)
            serializer = FeedbackSerializer(feedbacks, many=True)
            return Response(serializer.data)
        except Feedback.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class ListingListView(APIView):
    def post(self, request):
        sort_by = request.data.get('sort_by')
        listings = Listing.objects.all()
        if sort_by:
            if sort_by == 'price_asc':
                listings = listings.order_by('price')
            elif sort_by == 'price_desc':
                listings = listings.order_by('-price')
            elif sort_by == 'rating_asc':
                listings = listings.order_by('rating')
            elif sort_by == 'rating_desc':
                listings = listings.order_by('-rating')
            elif sort_by == 'bedrooms_asc':
                listings = listings.order_by('bedrooms')

        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)