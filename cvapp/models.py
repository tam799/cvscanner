from django.db import models

class CV(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    document = models.FileField(upload_to='documents/')
    # address = models.TextField()
    # summary = models.TextField()
    # skills = models.TextField()
    # experience = models.TextField()
    # education = models.TextField()
    # projects = models.TextField()
    # certifications = models.TextField()
    # languages = models.TextField()
    # hobbies = models.TextField()
    # references = models.TextField()

    def __str__(self):
        return self.name
# Create your models here.
