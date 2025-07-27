from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


def home(request):
    records = Record.objects.all()

    # Check to see if logging in
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect("home")
        else:
            messages.success(request, "Invalid username or password.")
            return redirect("home")
    else:
        return render(request, "home.html", {"records": records})


def login_user(request):
    pass


def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Automatically log in the user after registration
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            # Show success message
            messages.success(request, "You have successfully registered.")
            return redirect("home")
    else:
        form = SignUpForm()
        return render(request, "register.html", {"form": form})

    return render(request, "register.html", {"form": form})


def customer_record(request, user_id):
    if request.user.is_authenticated:
        # Lookup record
        customer_record = Record.objects.get(id=user_id)

        return render(request, "record.html", {"customer_record": customer_record})
    else:
        messages.error(request, "You must be logged in to view this page.")
        return redirect("home")


def delete_record(request, user_id):
    if request.user.is_authenticated:
        delete_record = Record.objects.get(id=user_id)
        delete_record.delete()
        messages.success(request, "Record deleted successfully.")
        return redirect("home")
    else:
        messages.error(request, "You must be logged in to Delete this record.")
        return redirect("home")


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record added successfully.")
                return redirect("home")
        return render(request, "add_record.html", {"form": form})
    else:
        messages.error(request, "You must be logged in to add a record.")
        return redirect("home")
