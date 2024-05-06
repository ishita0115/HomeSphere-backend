from django.db import models
from django.utils.timezone import now
from app1.models import User
import uuid
class AbstractModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now)

    class Meta:
        abstract = True

class ListingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
class Listing(AbstractModel):
    objects = ListingManager()

    class SaleType(models.TextChoices):
        FOR_SALE = 'For Sale'
        FOR_RENT = 'For Rent'
    
    class HomeType(models.TextChoices):
        ROWHOUSE = 'rowhouse'
        COLONIAL = 'colonial'
        FLAT = 'flat'
        COTTAGE = 'cottage'
        BUNGALOW = 'bungalow'
        OTHER = 'other'
    class Rental_choice(models.TextChoices):
        MONTH = 'per month'
        WEEK = 'per week'
        DAY = "per day"
        

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    favorited = models.ManyToManyField(User, related_name='favorites', blank=True)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=255)
    description = models.TextField()
    extrafacility = models.TextField()
    rental_choice = models.CharField(max_length=20 , blank=True, choices=Rental_choice.choices)
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    sale_type = models.CharField(max_length=10, choices=SaleType.choices, default=SaleType.FOR_SALE)
    home_type = models.CharField(max_length=10, choices=HomeType.choices, default=HomeType.ROWHOUSE)
    image1 = models.ImageField(upload_to='images')
    image2 = models.ImageField(upload_to='images')
    image3 = models.ImageField(upload_to='images')
    image4 = models.ImageField(upload_to='images')
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    @property
    def get_user_name(self):
        return self.user.first_name
    @property
    def get_profile_picture(self):
        return self.user.profilephoto
    
    @property 
    def get_user_email(self):
        return self.user.email

    def __str__(self):
        return self.title
    
    def delete(self, using=None, keep_parents=False):
        self.image1.storage.delete(self.image1.name)
        self.image2.storage.delete(self.image2.name)
        self.image3.storage.delete(self.image3.name)
        self.image4.storage.delete(self.image4.name)
        self.is_deleted = True
        super().delete(using=using, keep_parents=keep_parents)



class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Listing = models.ForeignKey(Listing, related_name='Bookings', on_delete=models.CASCADE)
    which_date = models.DateField()
    booked_by = models.CharField(max_length=55,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    statusmanage = models.CharField(max_length=20, default='pending')

    @property
    def get_user_by_listing(self):
        return self.Listing.get_user_email