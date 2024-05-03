# urls.py
from django.urls import path
from .views import ManageListingView,ListingDetailView,UserListingAPIView,BookingListView,MyBooking,FavoriteAPIView,myallfavview,listing_coordinates_api

urlpatterns = [
 path('ManageListingView/', ManageListingView.as_view(), name='image_ManageListingView'), 
 path('detailisting/<int:pk>/', ListingDetailView.as_view(), name='image_ListingDetailView'), 
 path('user-listings/<int:user_id>/', UserListingAPIView.as_view(), name='user_listings'),
 path('bookings/', BookingListView.as_view(), name='booking-list'),
 path('mybooking/<str:uid>/', MyBooking.as_view(), name='mybooking'),
 path('bookingsdelete/<str:uid>/', BookingListView.as_view(), name='delete_booking'),
 path('favorite/<int:pk>/', FavoriteAPIView.as_view(), name='favorite'),
 path('myFavorites/<uuid:user_id>/',myallfavview.as_view(),name='myalllisting'),
 path('listing-coordinates/', listing_coordinates_api.as_view(), name='listing_coordinates_api'),

]

