from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfileInfo(models.Model):
    """ Model class to add additional information that the django.contrib.auth.models.User class
        doesn't have. We don't directly inherit from that User class, as it may cause the DB
        to think that there are multiple instances of the User class. Instead we use a one-to-one
        field relationship.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Additional Details
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)  # Need to create profile_pics under /media

    def __str__(self):
        return self.user.username
