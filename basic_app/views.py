from django.shortcuts import render
from basic_app.models import UserProfileInfo
from basic_app.forms import UserForm, UserProfileInfoForm
from django.http import HttpResponse, HttpResponseRedirect

# Helpful Django imports for login etc
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required  # add to views where user is required to be logged in


# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')


# Want to make sure that only users who are logged in can log out
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/basic_app/user_login/')
def special(request):
    return HttpResponse("You're logged in. Niiiice.")


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)  # hashes and saves the password
            user.save()

            profile = profile_form.save(commit=False)  # don't save yet to avoid clashing
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html', context={
        "user_form": user_form,
        "profile_form": profile_form,
        "registered": registered,
    })


def user_login(request):

    if request.method == "POST":

        # Grab the username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))  # returns them to the "index" page after successful login

            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")

        else:
            print("Someone tried to login and failed")
            print("Username: {} and Password: {}".format(username, password))
            return HttpResponse("Invalid login details supplied!")

    else:
        return render(request, "basic_app/login.html", {})
