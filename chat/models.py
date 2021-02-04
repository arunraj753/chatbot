from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Inquiry(models.Model):

  name = models.CharField(max_length=256,blank=True)
  mobile = models.CharField(max_length=256,blank=True,null=True)
  email = models.EmailField(blank=True,null=True)
  app_type = models.EmailField(max_length=256,blank=True,null=True)
  business = models.CharField(max_length=256,blank=True,null=True)
  budget = models.CharField(max_length=256,null=True,blank=True)
  

  def __str__(self):
    return self.email

class Career(models.Model):

  title       = models.CharField(max_length=256)
  experiance  = models.IntegerField(null=True,blank=True,default=0)
  vaccany     = models.IntegerField(null=True,blank=True)
  job_status  = models.BooleanField(default=False)

  def __str__(self):
    return self.title

class Leave(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  available = models.IntegerField(default=14)

  def __str__(self):
    return (f"{self.user} - {self.available}")

class LeaveApplication(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  date = models.DateField()
  status = models.BooleanField(blank=True,null=True)

  def __str__(self):
    return (f"Leave applied by {self.user} for {self.date}")

class Project(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  title = models.CharField(max_length=256,null=True,blank=True)
  deadline = models.DateField(null=True,blank=True)

  def __str__(self):
    return (f"Project for {self.user}")

class News(models.Model):
  date = models.DateField()
  news = models.CharField(max_length=256)
  
  def __str__(self):
    return f"Ciruclar added on {self.date}"

class ResetCode(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  code = models.IntegerField()
  
  def __str__(self):
    return f"Reset code for {self.user} is {self.code}"