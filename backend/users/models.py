from django.db import models

# Create your models here.
import uuid
from django.db import models

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=10)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)