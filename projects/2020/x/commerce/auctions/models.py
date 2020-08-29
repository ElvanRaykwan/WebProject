from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    url = models.CharField(max_length=20480, blank=True)
    description = models.TextField(max_length=512)
    price = models.IntegerField()
    date = models.DateTimeField()
    category = models.CharField(max_length=32)    
    user = models.ForeignKey(User, null=True , on_delete=models.CASCADE, related_name="owner")
    winner = models.ForeignKey(User, blank=True, null=True , on_delete=models.CASCADE, related_name="winner")
    watch_list = models.ManyToManyField(User, blank=True, related_name="watchers")
    active = models.BooleanField(default=True)
        
class Bids(models.Model):
    bid = models.FloatField()
    user = models.ForeignKey(User, null=True , on_delete=models.CASCADE, related_name="bidder")
    item = models.ForeignKey(Listing, null=True , on_delete=models.CASCADE, related_name="bidon")

class Comments(models.Model):
    content = models.TextField(max_length=1028)
    date_comment = models.DateTimeField()
    user = models.ForeignKey(User, null=True , on_delete=models.CASCADE, related_name="commenter")
    item = models.ForeignKey(Listing, null=True , on_delete=models.CASCADE, related_name="commenton")
    