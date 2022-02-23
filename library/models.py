from re import S
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    category = models.CharField(max_length=50)
    volume =  models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=300,null=True)
    availability = models.BooleanField(default=True)
    published_date = models.DateField(auto_now=False,null=True)

    def __str__(self):
        return str(self.name) + " ["+(self.author)+']'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_dob = models.DateField(auto_now_add=False)
    gender= models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=3, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    image = models.ImageField(upload_to="uploads/profile-pic/")

    def __str__(self):
        return str(self.user) + " ["+str(self.branch)+']' + " ["+str(self.roll_no)+']'




class IssuedBook(models.Model):
    student_name= models.ForeignKey(Student, on_delete=models.CASCADE,null=True)
    book_name= models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    author_name = models.CharField(max_length=200,null=True)
    isbn = models.CharField(max_length=13)
    Volume = models.CharField(max_length=50,null=True)
    category = models.CharField(max_length=100,null=True)
    issued_date = models.DateField(auto_now=True)
