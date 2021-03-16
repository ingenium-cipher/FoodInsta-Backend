from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

gender_choices = [('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')]
member_type_choices = [('Individual', 'Individual'), ('Restaurant', 'Restaurant'), ('NGO', 'NGO')]

class Member(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    static_id = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    contact_no = models.BigIntegerField(validators=[MaxValueValidator(9999999999), MinValueValidator(1111111111)], unique=True)
    member_type = models.CharField(max_length=20, choices=member_type_choices)

class Individual(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='individual')
    reward_points = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=10, choices=gender_choices)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.member.auth_user.first_name} - {self.member.contact_no}"

class Restaurant(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='restaurant')
    landline_number = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    website = models.URLField(max_length = 200)
    reg_address = models.CharField(max_length=100)

class NGO(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='ngo')
    reg_number = models.CharField(max_length=20)
    reg_address = models.CharField(max_length=100)
    

# Create your models here.
