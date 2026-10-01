from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Sectors(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Company(models.Model):
    name=models.CharField(max_length=50,unique=True)
    address=models.CharField(max_length=300)
    website=models.URLField()

    def __str__(self):
        return self.name


class Jobs(models.Model):
    title=models.CharField(max_length=100)
    sector=models.ForeignKey(Sectors,on_delete=models.CASCADE)
    company=models.ForeignKey(Company,on_delete=models.CASCADE)
    location=models.CharField(max_length=50)
    description=models.TextField()
    salary=models.CharField(max_length=50)
    post_date=models.DateField(auto_now_add=True)
    slug=models.SlugField(blank=True)
    is_active=models.BooleanField(default=True)
    end_date=models.DateField()

    def __str__(self):
        return self.title

    def save(self):
        super().save()
        self.slug=f"{self.company.name}-{self.title}-{self.id}".lower()
        return super().save(update_fields=['slug'])

class Applications(models.Model):
    job=models.ForeignKey(Jobs,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    resume=models.FileField(blank=True,upload_to='resume')
    date=models.DateField(auto_now_add=True)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, related_name='user')
    dob=models.DateField(null=True,blank=True)
    phone=models.CharField(max_length=12,blank=True)
    place=models.CharField(max_length=50,blank=True)
    qualification=models.CharField(max_length=50,blank=True)
    headline=models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.user.first_name

class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message}"
    








