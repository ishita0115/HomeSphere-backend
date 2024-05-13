# urls.py
from django.urls import path
from .views import ListingFeedbackAPIView, ListingListView, ManageListingView,ListingDetailView, SubmitFeedbackAPIView,UserListingAPIView,BookingListView,MyBooking,FavoriteAPIView,myallfavview,listing_coordinates_api,sellerbookingmanage,fetchbookingstatus

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
 path('bookings/<int:pk>/<str:action>/', sellerbookingmanage.as_view()),
 path('seller-bookings/', sellerbookingmanage.as_view()),
 path('seller-bookings/<uuid:booking_id>/<str:action>/', sellerbookingmanage.as_view(), name='seller_booking_manage'),
 path('bookings/<int:pk>/status/', fetchbookingstatus.as_view(), name='fetch-booking-status'),
 path('submitfeedback/', SubmitFeedbackAPIView.as_view(), name='submit_feedback'),
 path('listing/<int:listing_id>/rating/', SubmitFeedbackAPIView.as_view(), name='listing_rating'),
 path('listingfeedback/<int:listing_id>/', ListingFeedbackAPIView.as_view(), name='listing_feedback'),
 path('listinglist/', ListingListView.as_view(), name='property-list'),
]


