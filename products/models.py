from django.db import models
from users.models import *
import uuid

def image_directory_path(instance, filename):
    print(instance)
    return 'Products/' + '{0}-{1}'.format(instance.name, filename.split('.')[0]) + '_UID' \
        + str(instance.static_id)[3:27].replace('-', '81') + '.'+str(filename.split('.')[-1])

class Product(models.Model):
    static_id = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to=image_directory_path, blank=True)
    cost = models.PositiveIntegerField(blank=True, null=True)

class Post(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)


# Create your models here.
