from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from gdstorage.storage import GoogleDriveStorage

gender_choices = [('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')]
member_type_choices = [('Individual', 'Individual'), ('Restaurant', 'Restaurant'), ('NGO', 'NGO')]

def proof_directory_path(instance, filename):
    return 'ID-Proofs/' + '{0}-{1}'.format(instance.reg_number, filename.split('.')[0]) + '.' + str(filename.split('.')[-1])

class Member(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    static_id = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    contact_no = models.BigIntegerField(validators=[MaxValueValidator(9999999999), MinValueValidator(1111111111)], unique=True)
    member_type = models.CharField(max_length=20, choices=member_type_choices)

    def __str__(self):
        return f"{self.auth_user.username} - {self.member_type}"

class Individual(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='individual')
    name = models.CharField(max_length=50)
    reward_points = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=10, choices=gender_choices)
    birth_date = models.DateField(auto_now_add=False)

    def __str__(self):
        return f"{self.name} - {self.member.contact_no}"

class Restaurant(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='restaurant')
    landline_number = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    website = models.URLField(max_length = 200, blank=True, null=True)
    address = models.CharField(max_length=100)

class NGO(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='ngo')
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=20)
    reg_address = models.CharField(max_length=100)
    id_proof = models.ImageField(upload_to=proof_directory_path, blank=True, storage=GoogleDriveStorage)
    

# Create your models here.
