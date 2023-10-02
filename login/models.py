from django.db import models
from django.contrib.auth.models import User

class ProjectImage(models.Model):
    image = models.ImageField(upload_to="projectimages")



class Education(models.Model):
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    startYear = models.IntegerField(blank=True)
    endYear = models.IntegerField(blank=True)


    
class Project(models.Model):
    projectname = models.CharField(max_length=100)
    projectimages = models.ManyToManyField(ProjectImage, blank=True)
    projectdesc = models.CharField(max_length=500)
    projectlinks = models.CharField(max_length=2000)



class Portfolio(models.Model):
    username =  models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    jobrole = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    socialmedia = models.CharField(max_length=2000)
    skills = models.CharField(max_length=500)
    educations = models.ManyToManyField(Education, default=None)
    projects = models.ManyToManyField(Project)



