from django.db import models
from users.models import User


class UploadedFile(models.Model):
    file = models.FileField(upload_to='docs/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.uploaded_by} - {self.uploaded_on}'
