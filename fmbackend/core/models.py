from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    username = models.CharField(max_length=20, blank=True, null=True)  
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('family_member', 'Family Member'), ('accountant', 'Accountant')])
    email = models.EmailField(unique=True)
    profile_img = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email

class FamilyGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_groups')
    created_at = models.DateTimeField(auto_now_add=True)

# User-Group Permissions
class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE)
    permissions = models.JSONField()  # e.g., {"assets": "read", "transactions": "none"}
    class Meta:
        unique_together = ('user', 'group')

# Assets
class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=[('bank_account', 'Bank Account'), ('property', 'Property'), ('business', 'Business'), ('security', 'Security')])
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)
    api_source = models.CharField(max_length=255, null=True, blank=True)

# Transactions
class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    date = models.DateTimeField()
    is_unusual = models.BooleanField(default=False)

# Documents (Using Filesystem)
class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')  # Stores in /media/documents/
    type = models.CharField(max_length=20, choices=[('will', 'Will'), ('policy', 'Policy'), ('tax_form', 'Tax Form')])
    expiry_date = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Notifications
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=[('reminder', 'Reminder'), ('alert', 'Alert')])
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)