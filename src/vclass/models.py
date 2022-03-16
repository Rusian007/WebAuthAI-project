from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.urls import reverse
import os
# Create your models here.

def update_filename(instance, filename):
    path = "avatar/"
    ext = "jpg"
    #print(type(ext))
    name = '{}.{}'.format(instance.pk, ext)
    return os.path.join(path, name)
class User(AbstractUser):
    is_Teacher = models.BooleanField(default=False)
    is_Student = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.username)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    First_name = models.CharField(max_length=20,null=True)
    Last_name = models.CharField(max_length=20,null=True)
    image = models.ImageField(upload_to = update_filename ,default=None,null=False)
    Email_address = models.EmailField(default=None, null=True)


class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    First_name = models.CharField(max_length=20,null=True)
    Last_name = models.CharField(max_length=20,null=True)
    Email_address = models.EmailField(default=None, null=True)


# class table
class Classroom (models.Model):
    Class_name = models.CharField(max_length=49, default=None,null=False)
    Subject = models.CharField(max_length=30,default=None,null=False)
    section = models.IntegerField(default=None,null=False)
    Invitation_Code = models.CharField(max_length=6,default=None,null=False)
    Teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE)
    Student = models.ManyToManyField(Student)

    def get_absolute_url(self):
        return reverse("portf:student-class-view", kwargs={"my_id": self.id})
    def get_absolute_url_t(self):
        return reverse("portf:teacher-class-view", kwargs={"my_id": self.id})

class image_verify(models.Model):
    image = models.ImageField(upload_to = "check/", null=True)
    

# class metarials table
class Class_Metarials (models.Model):
    title = models.CharField(max_length=80, default=None, null=True)
    Description = models.TextField(default=None)
    Submit_Date = models.DateField(default=None)
    Pdf = models.FileField(null=False,upload_to = "pdfs/" )
    Classroom = models.ForeignKey(to=Classroom, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("portf:task-detail", kwargs={"my_id": self.id})



# Questions table
class Questions (models.Model):
    Tag = models.CharField(max_length=45,null=True)
    Written = models.TextField(null=True)
    Voice = models.FileField(null=True,upload_to = "voice/")
    Check = models.CharField(null=True, max_length=15)
    Class_Metarials = models.ForeignKey(to=Class_Metarials, on_delete=models.CASCADE)
    Student = models.ForeignKey(to=Student, on_delete=models.CASCADE)
