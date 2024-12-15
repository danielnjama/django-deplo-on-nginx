from django.db import models
from datetime import timedelta








# Create your models here.

class Subjects(models.Model):
    subjectname = models.CharField(max_length=50)
    subjectImage = models.ImageField(upload_to='subectimages')
    
    def __str__(self):
        return self.subjectname
    
    class Meta:
        verbose_name = "Subjects"
        verbose_name_plural = "Subjects"
    
    


class Course(models.Model):
    courseSubject = models.ForeignKey(Subjects,on_delete=models.CASCADE,related_name="course",verbose_name="Course Subject")
    courseImage = models.ImageField(upload_to='subectimages',help_text="image size 100 by 100",verbose_name="Course Image")
    courseName = models.CharField(max_length=100,verbose_name="Course Name")
    coursePrice = models.PositiveIntegerField(help_text="Enter price in dollars",verbose_name="Course Price")
    courseDuration = models.DurationField(default=timedelta(hours=5,minutes=20),verbose_name="Course Duration")
    
    def __str__(self):
        return self.courseName








# genderInstance = (
#     ('Male','Male'),
#     ('Female','Female'),
#     ('Any other','Any other')
# )

# class userInformation(models.Model):
#     first_name = models.CharField(max_length=30)
#     user_story = models.TextField(null=True, blank=True)
#     profilePic = models.ImageField(upload_to='profile')
#     DateofBirth = models.DateField()
#     # age = models.PositiveIntegerField()
#     DateofRegistration = models.DateTimeField(auto_now_add=True)
#     email = models.EmailField(max_length=50)
#     useResume = models.FileField(upload_to="cvs")
#     salary = models.PositiveIntegerField()
#     height = models.FloatField()
#     gender = models.CharField(choices=genderInstance,max_length=30)
#     isActive = models.BooleanField(default=True)
    
    

#Model relationships
#1. OneToField
#2. One to Many relation
#3. many to many
