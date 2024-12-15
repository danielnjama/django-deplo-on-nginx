from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render,HttpResponse
from . models import Course, Subjects
from django.db import models
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    
    return render(request,'index.html')


def about(request):
    return render(request,'about.html')

@login_required(login_url='login')
def courses(request):
    all_courses = Course.objects.all()
    # all_subjects = Subjects.objects.all()
    all_subjects = Subjects.objects.annotate(course_count=models.Count('course'))
    
    context = {"allcourses":all_courses,"allsubjects":all_subjects}
    
    
    return render(request,'course.html',context)


def teachers(request):
    return render(request,'teacher.html')


def contacts(request):
    if request.method == "POST":
        name = request.POST["name"] 
        email = request.POST["email"]
        subject = request.POST["subject"]
        message_instance = request.POST["message"]
        
        message = f'Name: {name}\nEmail:{email}\n{message_instance}'
        
        try:
            send_mail(
                        subject,
                        message,
                        email,
                        ['admin@dtechnologys.com'],
                        fail_silently=False,
                    )
            messages.success(request,'Your email has been sent successfully!')
            return render(request,'contact.html')
        except Exception as e:
            messages.error(request,f'An error occured and your email faild: {e}')
        
        # print(name,email,subject,message)
        
    return render(request,'contact.html')

def get_subjects(request):
    all_subjects = Subjects.objects.all().values()
    all_subjects_list =list(all_subjects)
    return JsonResponse({'subjects':all_subjects_list})





    