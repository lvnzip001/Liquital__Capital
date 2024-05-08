from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages

def register_client(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        form = CreateUserForm()

        if request.method == "POST":
            form = CreateUserForm(request.POST)
            # breakpoint()
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get("username")

                messages.success(
                    request, "Account was created for " + username)
                return redirect("login")

        context = {"form": form}
        return render(request, "register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


def login_client(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    else:
        
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
          
            if user is not None:
                login(request, user)
                return redirect("dashboard")

            else:
                messages.info(request, "USERNAME OR PASSWORD IS INCORRECT")
                return render(request, "login_client.html")

        return render(request, "login_client.html")


