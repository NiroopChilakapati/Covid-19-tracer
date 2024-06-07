import datetime

from django.db import models


# Create your models here.
class RandRdetails(models.Model):
    heading = models.TextField(max_length=220 , null= False)
    content = models.TextField(null=False)

    def __str__(self):
        return  self.heading


class Contact(models.Model):
    date = models.DateField()
    time = models.TimeField(default=datetime.datetime.now().time())
    name = models.CharField(max_length=220)
    email = models.EmailField()
    phnum = models.CharField(max_length=16)
    feedback = models.TextField()

    def __str__(self):
        return self.name + "   |  " + self.email + "  |  " +self.phnum


class Country(models.Model):
    country = models.CharField(max_length=220)


    def __str__(self):
        return self.country