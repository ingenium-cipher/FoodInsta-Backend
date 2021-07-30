from django.db import models
from users.models import *
import uuid
from gdstorage.storage import GoogleDriveStorage
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

# Define Google Drive Storage
# gd_storage = GoogleDriveStorage()
order_status_choices = [
    ('Approved', 'Approved'),
    ('Pending', 'Pending'),
    ('Rejected', 'Rejected'),
    ('Completed', 'Completed'),
]

def image_directory_path(instance, filename):
    return 'Products/' + '{0}-{1}'.format(instance.fresh_upto, filename.split('.')[0]) + '.'+str(filename.split('.')[-1])

class Product(models.Model):
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=image_directory_path, blank=True, storage=GoogleDriveStorage)
    weight = models.CharField(max_length=10, null=True, blank=True)
    fresh_upto = models.DateTimeField(auto_now_add=False, blank=True, null=True)

    def __str__(self):
        return f"{self.description} - {self.weight}"

    def save(self, *args, **kwargs):
        if not self.fresh_upto:
            self.fresh_upto = datetime.now() + timedelta(days=2)
        super().save(*args, **kwargs)

    def get_image_url(self):
        if self.image:
            return self.image.url.split('&')[0]
        return None

class Post(models.Model):
    static_id = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='post')
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4)
    is_completed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    contact_no = models.BigIntegerField(validators=[MaxValueValidator(9999999999), MinValueValidator(1111111111)])

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

    def save(self, *args, **kwargs):
        if not self.city:
            self.city = self.member.city
        super().save(*args, **kwargs)

class Order(models.Model):
    ordered_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='ordered_by')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_orders')
    order_status = models.CharField(max_length=30, choices=order_status_choices, default='Pending')
    created_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.post.member == self.ordered_by:
            raise ValidationError("You cannot request your own post!")
        if self.order_status == "Completed":
            self.post.is_completed = True
            self.post.save()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('ordered_by', 'post')

# Create your models here.
