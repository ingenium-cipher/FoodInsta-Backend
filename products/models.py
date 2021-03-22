from django.db import models
from users.models import *
import uuid
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
# gd_storage = GoogleDriveStorage()

def image_directory_path(instance, filename):
    return 'Products/' + '{0}-{1}'.format(instance.name, filename.split('.')[0]) + '_UID' \
        + str(instance.static_id)[3:27].replace('-', '81') + '.'+str(filename.split('.')[-1])

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=image_directory_path, blank=True, storage=GoogleDriveStorage)
    cost = models.PositiveIntegerField(default=0)
    fresh_upto = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - Rs. {self.cost}"

class Post(models.Model):
    static_id = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product} posted by {self.member} at {self.created_at}"

    def refresh_qr_code(self):
        while True:
            new_code = uuid.uuid4()
            self.qr_code = new_code
            try:
                self.save(update_fields=["qr_code"])
                break
            except:
                pass
        return new_code

# Create your models here.
