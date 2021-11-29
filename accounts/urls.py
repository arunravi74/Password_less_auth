from django.urls import path
from .views import login_otp, loginview, otpview, registerview,home
urlpatterns = [
    path("register/",registerview,name='register'),
    path('otp/',otpview,name='otp'),
    path('home/',home,name='home'),
    path('',loginview,name = 'login'),
    path('login_otp',login_otp,name='login_otp')
]