from django.db import models
# from django.contrib.gis.db import models
#geo-location
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

REGEX_PHONE_NUMBER = RegexValidator(regex=r'^\d{10}$', message="PHONE MUST BE 10 DIGITS: '4731234567'.")
        
class CustomUser(AbstractUser):
    org = models.CharField(max_length=10, blank=True)
    user_access = models.CharField(max_length=10, blank=True)
    
    def __str__(self):
        return self.username

class OrganizationAccount(models.Model):
    org_name = models.TextField(max_length=10, blank=True)
    org_token = models.TextField(max_length=300, blank=True)
    org_sid = models.TextField(max_length=300, blank=True)  
    org_gui_name = models.URLField(max_length=300, blank=True, null = True)  
    org_youtube_link = models.URLField(max_length=300, blank=True, null = True)  
    org_facebook_link = models.URLField(max_length=300, blank=True, null = True)  
    org_instagram_link = models.URLField(max_length=300, blank=True, null = True)  
    org_tiktk_link = models.URLField(max_length=300, blank=True, null = True)  
    org_website_link = models.URLField(max_length=300, blank=True, null = True)  

    
    def __str__(self):
        return self.org_name
        
class CategoryGroup(models.Model):
    name_info = models.TextField(max_length=45, blank=True)
    org = models.TextField(max_length=10, blank=False)
    user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, related_name="username2")

    def __str__(self):
        return self.name_info

class Contact(models.Model):
    #   Creates a model named user, via class
    first_name_info = models.TextField(max_length=20)
    last_name_info = models.TextField(max_length=20)
    phone_number_info = models.TextField(max_length=10, validators=[REGEX_PHONE_NUMBER])
    contact_category = models.ForeignKey(CategoryGroup, on_delete = models.RESTRICT, blank=True)
    contact_notes_info = models.TextField(max_length=300, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT, related_name="usernames")
    org = models.TextField(max_length=10, blank=False)

    def __str__(self):
        return self.first_name_info
    
class OutreachRegistrationForm(models.Model):
    #   Creates a model named Owner, via class.
    outreach_first_name = models.TextField(max_length=20)
    outreach_last_name = models.TextField(max_length=20)
    outreach_phone_number = models.TextField(max_length=10, validators=[REGEX_PHONE_NUMBER])
    outreach_spot = models.TextField(max_length=30)
    outreach_category = models.TextField(max_length=45)
    minister_category = models.TextField(max_length=45)
    outreach_time = models.TextField(max_length=300, blank=True)
    outreach_date = models.TextField(max_length=300, blank=True)
    contact_notes = models.TextField(max_length=300, blank=True)
    outreach_latitude = models.DecimalField(max_digits=22, decimal_places=3, blank=True, null=True)
    outreach_longitude = models.DecimalField(max_digits=22, decimal_places=3, blank=True, null=True)
    user_email = models.EmailField(max_length=254)
    user_id = models.TextField(max_length=20, blank=True)
    org_name = models.TextField(max_length=10, blank=True)

    def __str__(self):
        return self.outreach_first_name


class ImageUpload(models.Model):
    my_image = models.ImageField(upload_to='images/')
    my_image_thumbnail = ImageSpecField(source='my_image', processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 60})


@receiver(post_save, sender=CustomUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
