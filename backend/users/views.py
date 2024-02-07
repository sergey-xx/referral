from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User Not Found....")
            return redirect("home")

        if user is not None:
            login(request, user)
            return redirect("admin")
        else:
            messages.error(request, "Username or Password does not match...")

    return render(request, "login.html")
