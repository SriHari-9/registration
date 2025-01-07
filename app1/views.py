from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='login')
def HomePage(request):
    return render(request,'home.html')

def Indexpage(request):
    return render(request,'index.html')

"""def SignupPage(request):
    if request.method == 'POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("your passord and confirm password are not same")
        else:
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')


    return render(request,'signup.html')"""

"""def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is mismatched")


    return render(request,'login.html')"""

def LogoutPage(request):
    logout(request)
    return redirect('index')
# views.py
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages


def SignupPage(request):
    if request.method == "POST":
        username= request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        otp = random.randint(100000, 999999)

        # Store OTP temporarily in the session
        request.session['username']=username
        request.session['signup_email'] = email
        request.session['signup_password'] = password
        request.session['signup_otp'] = otp

        # Send OTP to email
        send_mail(
            'Your OTP Code',
            f'Your OTP is {otp}. Please enter it to complete your registration.',
            'your_email@gmail.com',  # Replace with your email
            [email],
        )

        return redirect('verify_otp')  # Redirect to OTP verification page

    return render(request, 'signup.html')
def verify_otp(request):
    if request.method == "POST":
        entered_otp = int(request.POST['otp'])
        stored_otp = request.session.get('signup_otp')

        if entered_otp == stored_otp:
            # Create user after OTP verification
            username=request.session['username']
            email = request.session['signup_email']
            password = request.session['signup_password']
            user = User.objects.create_user(username=username,email=email, password=password,)
            user.save()

            # Clear session data
            del request.session['username']
            del request.session['signup_email']
            del request.session['signup_password']
            del request.session['signup_otp']

            messages.success(request, "Signup successful!")
            return redirect('home')

        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify_otp.html')
from django.contrib.auth import authenticate, login

def LoginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        request.session['username']=username
        request.session['password'] = password
        if user:
            otp = random.randint(100000, 999999)
            request.session['login_user_id'] = user.id
            request.session['login_otp'] = otp

            # Send OTP to user's email
            email=user.email
            send_mail(
                'Your Login OTP',
                f'Your OTP is {otp}. Please enter it to log in.',
                'your_email@gmail.com',
                [email],
            )

            return redirect('login_verify_otp')  # Redirect to OTP verification page
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'login.html')

def login_verify_otp(request):
    if request.method == "POST":
        # Retrieve entered OTP and stored OTP from session
        entered_otp = int(request.POST['otp'])
        stored_otp = request.session.get('login_otp')

        if entered_otp == stored_otp:
            # User OTP verification passed, now authenticate and login the user
            

            username = request.session['username']
            password = request.session['password']

            # Authenticate and log in the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Clear session data after successful login
                del request.session['login_user_id']
                del request.session['login_otp']
                del request.session['username']
                del request.session['password']

                messages.success(request, "Login successful!")
                return redirect('home')  # Redirect to the home page after login
            else:
                messages.error(request, "Authentication failed. Please try again.")
                return redirect('login')  # Redirect to login if authentication fails
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'login_verify_otp.html')  # Render OTP verification page if POST request failed
