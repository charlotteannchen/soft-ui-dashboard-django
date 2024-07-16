from django.db import models

class Upload(models.Model):
    image = models.ImageField(upload_to='uploads/')
    message = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
