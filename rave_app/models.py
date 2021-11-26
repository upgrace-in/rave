from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.base import ModelState

from django.db.models.fields import BigAutoField

class nfts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer_id = models.CharField(max_length=200, blank=True, null=True)
    wallet_address = models.CharField(max_length=200)
    transaction_id = models.CharField(max_length=1000, blank=True, null=True)
    file = models.FileField(upload_to='nfts/')
    title = models.CharField(max_length=1000)
    desc = models.TextField()
    price = models.FloatField()
    approved = models.BooleanField(default=False)
    applied_for_purchasing = models.BooleanField(default=False)
    purchased = models.BooleanField(default=False)