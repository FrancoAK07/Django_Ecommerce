from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=250)
    image = models.ImageField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    department = models.CharField(max_length=80)
    slug = models.SlugField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    addres1 = models.CharField(max_length=200, blank=True)
    addres2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)
