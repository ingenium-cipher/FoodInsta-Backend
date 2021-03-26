from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from gdstorage.storage import GoogleDriveStorage
from django.core.exceptions import ValidationError

gender_choices = [('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')]
member_type_choices = [('Individual', 'Individual'), ('Restaurant', 'Restaurant'), ('NGO', 'NGO')]

def proof_directory_path(instance, filename):
    return 'ID-Proofs/' + '{0}-{1}'.format(instance.reg_number, filename.split('.')[0]) + '.' + str(filename.split('.')[-1])

def profile_pic_directory_path(instance, filename):
    return 'Profile-Pics/' + '{0}-{1}'.format(instance.auth_user.username, filename.split('.')[0]) + '.' + str(filename.split('.')[-1])

class City(models.Model):
    name = models.CharField('name', max_length=50, unique=True)

    def __str__(self):
        return self.name

class Member(models.Model):
    static_id = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    contact_no = models.BigIntegerField(validators=[MaxValueValidator(9999999999), MinValueValidator(1111111111)], unique=True, null=True, blank=True)
    member_type = models.CharField(max_length=20, choices=member_type_choices)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    address = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(upload_to=profile_pic_directory_path, blank=True, storage=GoogleDriveStorage)
    reg_token = models.CharField(max_length=260, blank=True)

    def __str__(self):
        return f"{self.auth_user.username} - {self.member_type}"

    def get_name(self):
        if self.member_type == 'Individual':
            return self.individual.name
        if self.member_type == 'NGO':
            return self.ngo.name
        if self.member_type == 'Restaurant':
            return self.restaurant.name

    def get_profile_pic_url(self):
        if self.profile_pic:
            print(self.profile_pic.url)
            return self.profile_pic.url.split('&')[0]
        return None

class Individual(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='individual')
    name = models.CharField(max_length=50)
    reward_points = models.PositiveIntegerField(default=0)
    is_volunteer = models.BooleanField(default=False)
    id_number = models.CharField(max_length=50, blank=True, null=True)
    ngo = models.ForeignKey('NGO', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.member.contact_no}"

    def save(self, *args, **kwargs):
        if self.is_volunteer and not self.id_number:
            raise ValidationError("Please provide ID number")
        if self.is_volunteer and not self.ngo:
            raise ValidationError("Please select an NGO")
        super().save(*args, **kwargs)
        

class Restaurant(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='restaurant')
    landline_number = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    website = models.URLField(max_length = 200, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.member.contact_no}"

class NGO(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='ngo')
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=20)
    id_proof = models.ImageField(upload_to=proof_directory_path, blank=True, storage=GoogleDriveStorage)

    def __str__(self):
        return f"{self.name} - {self.member.contact_no}"  

# Create your models here.
