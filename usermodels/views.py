from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render,HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from . models import CustomUser
# Create your views here.

def send_activation(request):
    if request.method == "POST":
        username  = request.POST['username']
        if username:
            user_instance = CustomUser.objects.filter(username=username)
            if user_instance.exists():
                user = user_instance.first()
                action_code =user.activate_code
                recipient = user.email
                
                subject = "Activate your account"
                message = f'Hi {username}, kindly see use this to acivate account:\nActivation code:{action_code}'
                
                try:
                    send_mail(
                                subject,
                                message,
                                'danielnjama2015@gmail.com',
                                [recipient],
                                fail_silently=False,
                            )
                    messages.success(request,'Your email has been sent successfully!')
                    # return render(request,'contact.html')
                except Exception as e:
                    messages.error(request,f'An error occured and your email faild: {e}')
                        
                
    return render(request,'email.html')
    
    
    
    
def activate(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username  = request.POST['username']
            activation = request.POST['activation']
            user_instance = CustomUser.objects.filter(username=username)
            if user_instance.exists() and user_instance.first().activate_code == int(activation):
                # user_instance.first().account_active = True
                # print(user_instance.first().account_active)
                user_save_instance = CustomUser.objects.get(username=username)
                user_save_instance.account_active = True
                user_save_instance.save()
                # print(user_instance.first().account_active)
                messages.info(request,'Account activated!')
                return redirect('login')
            messages.warning(request,'Username or activation code incorrect')
            return render(request,'activate.html')
            
    return render(request,'activate.html')

def login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username  = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                if CustomUser.objects.filter(username=username).first().account_active == True:
                    auth.login(request,user)
                    if request.GET.get('next',None):
                        return HttpResponseRedirect(request.GET['next'])
                    return redirect('/')
                return redirect('activate')
                
            messages.warning(request,'Invalid login details')
            return render(request,'login.html')
            
        return render(request,'login.html')
    return redirect('/')


def register(request):
    if request.method =="POST":
        first_name = request.POST['first_name'] #first_name = request.POST.get('first_name')
        username  = request.POST['username']
        email = request.POST['email']
        phonenumber = request.POST['phone']
        gender = request.POST['gender']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            if CustomUser.objects.filter(username=username).exists():
                messages.warning(request,'Username taken!')
                return render(request,'register.html')
            elif CustomUser.objects.filter(email=email).exists():
                messages.warning(request,'Taken taken!')
                return render(request,'register.html')
            else:
                user = CustomUser.objects.create_user(username=username,first_name=first_name,email=email,password=password,gender=gender,phonenumber=phonenumber)
                #Send the activation code to user
                messages.info(request,'User created!')
                return redirect('login')
        messages.warning(request,'Password mismatch!')
        return render(request,'register.html')        
        
        
    return render(request,'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/')