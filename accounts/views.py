from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Profile
from django.contrib.auth.models import User
import random
import http.client
from django.contrib.auth import login
from pwless import settings


def send_otp(mobile,otp):
    conn = http.client.HTTPConnection("2factor.in")
    apikey =settings.api_key
    headers = headers = { 'content-type': "application/x-www-form-urlencoded" }
    template = f"your otp is {otp}"
    url = f"https://2factor.in/API/V1/{apikey}/SMS/{mobile}/{otp}/{template}"   
    url = url.replace(" ","")
    conn.request("GET",url,headers=headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    return None
def registerview(request):
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        check_user = User.objects.filter(email = email).first()
        check_profile = Profile.objects.filter(mobile = mobile).first()
        if check_user or check_profile:
            return render(request,'register.html',{'message':'User assosiated with this Email-ID is already exists'})
        
        user = User(email = email,username = name)
        user.save()
        otp = str(random.randint(1000,9999))
        profile = Profile(user = user,mobile = mobile,otp = otp)
        profile.save()
        send_otp(mobile,otp)
        request.session['mobile'] = mobile
        return redirect('otp')

    return render(request,'register.html')

def loginview(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        user = Profile.objects.filter(mobile = mobile).first()
        if not user:
            return render(request,'register.html',{'message':'User is not found'})
        
        request.session['mobile'] = mobile
        otp = str(random.randint(1000,9999))
        user.otp = otp
        user.save()
        send_otp(mobile,otp)
        return redirect('login_otp')
    return render(request,'login.html')


def login_otp(request):
    mobile = request.session['mobile']
    
    if request.method == "POST":
        otp = request.POST.get('otp')        
        profile = Profile.objects.filter(mobile=mobile).first()      
        if otp == profile.otp:
            user = User.objects.get(id = profile.user_id)
            login(request,user)
            return redirect('home')
        else:
            return render(request,'login_otp.html',{'message':'Please Enter correct OTP'})
    return render(request,'login_otp.html',{'mobile':mobile})
        


def otpview(request):
    mobile = request.session['mobile']
    
    if request.method == "POST":
        otp = request.POST.get('otp')        
        profile = Profile.objects.filter(mobile=mobile).first()        
        if otp == profile.otp:
            return redirect('home')
        else:
            return render(request,'otp.html',{'message':'Please Enter correct OTP'})
    return render(request,'otp.html',{'mobile':mobile})

def home(request):    
    return HttpResponse('Welcome to home page')