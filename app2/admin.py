from django.contrib import admin
from .models import Listing,Booking

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'address', 'city', 'price', 'sale_type', 'home_type','is_deleted')
    list_filter = ('sale_type', 'home_type')
    search_fields = ('title', 'address', 'city')



admin.site.register(Listing, ListingAdmin)

admin.site.register(Booking)