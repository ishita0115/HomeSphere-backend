
# class ImageUploadView(APIView):
#     def post(self, request, format=None):
#         serializer = ImageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Listing,Booking
from app1.models import User
from .serializers import ListingSerializer,BookingSerializer
from app1.serializers import UserSerializer
from .permissions import IsSellerUser, IsAdminUser

class ManageListingView(APIView):
    permission_classes = [IsAuthenticated]
    # parser_classes=[IsAdminUser]
    def get(self, request,*args, **kwargs):
        # try:
        #     listings = Listing.objects.all()
        #     serializer = ListingSerializer(listings, many=True)
        #     return Response({'data': serializer.data},status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            # Extract search parameters from the request query parameters
            country = request.GET.get('country', None)
            city = request.GET.get('city', None)
            sale_type = request.GET.get('sale_type', None)
            num_bedrooms = request.GET.get('num_bedrooms', None)
            home_type = request.GET.get('home_type', None)
            address = request.GET.get('address', None)
            min_price = request.GET.get('min_price', None)
            max_price = request.GET.get('max_price', None)

            # Get all properties if no search parameters are provided
            if not any([country, city, sale_type, num_bedrooms, home_type, address, min_price, max_price]):
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

                if num_bedrooms:
                    properties = properties.filter(num_bedrooms=num_bedrooms)

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
            user_pk = authenticated_user.pk  # Get the user's primary key

            # Fetch the user instance corresponding to the user_pk
            try:
                user_instance = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                raise NotFound("User not found")

            serializer = ListingSerializer(data=request.data)
            
            if serializer.is_valid():
                # Associate the listing with the user instance
                serializer.save(user=user_instance)
                print('insied if')
                return Response({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
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
        
class BookingListView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
      
            # Create a new Booking object with the seller_listing set to the authenticated user
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
        print("+++++++++++++++++")
        def get(self, request, uid):
            try:
                print("nice ")
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
    def get(self,request):
        try:
            listings = Listing.objects.all()

            coordinates = [
                {
                    'latitude': listing.latitude,
                    'longitude': listing.longitude,
                    'address': listing.address,
                    'city': listing.city,
                    'country': listing.country,
                    'image1': listing.image1.url if listing.image1 else None
                } 
                for listing in listings
            ]

            # Return the coordinates in the response
            return Response({'coordinates': coordinates}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)