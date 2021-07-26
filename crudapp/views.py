
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from .models import ProfileData
from django.shortcuts import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
# Create your views here.


@csrf_exempt
def user_login(request):
    context = {}
    if request.method == "POST":
        '''getting user data from form'''
        username = request.POST['username']
        password = request.POST['password']
        ''' verifying user with the database'''
        user1 = authenticate(request, username=username, password=password)

        if user1:
            login(request, user1)
            '''redirecting to profile_data page'''
            return HttpResponseRedirect(reverse("profile_data"))

        else:
            ''' user provide wrong credentials sending error msg'''
            context["error"] = "provide valid credentials"
            return render(request, "crudapp/login.html", context)

    else:
        return render(request, "crudapp/login.html")


@csrf_exempt
def profile_create(request):
    if request.method == "POST":
        ''' getting data from user form'''
        name = request.POST['name']
        past_address = request.POST['past_address']
        current_address = request.POST['present_address']
        phone_number = request.POST['phone_number']
        print(name, past_address, current_address, phone_number)
        ''' storing data into database'''
        profileData = ProfileData.objects.create(
            name=name,
            past_address=past_address,
            present_address=current_address,
            phone_number=phone_number,
            created_user = request.user
        )
        profileData.save()
        return HttpResponseRedirect(reverse("profile_data"))
    else:
        return render(request, "crudapp/profile_create.html")


@csrf_exempt
def profile_data(request):
    created_user_id = request.user.id
    '''filtering data based on user_login'''
    data = ProfileData.objects.filter(created_user_id=created_user_id)
    return render(request, "crudapp/profile_view.html", {"data":data})


@csrf_exempt
def profile_update(request):
    if request.method == "POST":
        username = request.POST['username']
        past = request.POST['past']
        address = request.POST['address']
        phone = request.POST['phone']
        print(username,past,address,phone)
    else:
        return render(request, "crudapp/profile_update.html")


@csrf_exempt
def profile_delete(request, pk):
    data = ProfileData.objects.get(pk=pk)
    data.delete()
    return HttpResponseRedirect(reverse("profile_data"))