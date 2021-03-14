from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

class Member(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    static_id = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contact_no = models.IntegerField(validators=[MaxValueValidator(9999999999), MinValueValidator(1111111111)])

# Create your models here.
