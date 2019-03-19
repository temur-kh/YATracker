from django.shortcuts import render
from django.urls import reverse
from django.http import (
    HttpResponseRedirect,
)
from django.contrib.auth import (
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
    get_user_model,
)


from .forms import (
    AuthorizationForm,
    RegistrationForm,
)

from user_manager.models import (
    Student,
    Instructor,
    Admin,
)

User = get_user_model()



def redirect_if_authorized(function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return function(request, *args, **kwargs)
    return wrapper


@redirect_if_authorized
def login(request):
    if request.method == 'POST':
        form = AuthorizationForm(request.POST)
        if form.is_valid():
            user = django_authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                django_login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                form.add_error(None, "User doesn't exist")
    else:
        form = AuthorizationForm()

    return render(request, 'authentication/login.html', {'form': form})


def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('login'))


@redirect_if_authorized
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            user_type = form.cleaned_data['user_type']
            if User.objects.filter(email=email).exists():
                form.add_error('email', "Email already in use")
            else:
                is_superuser = False
                is_staff = False

                if user_type == 'Student':
                    Model = Student
                elif user_type == 'Instructor':
                    Model = Instructor
                elif user_type == 'Admin':
                    Model = Admin
                    is_staff = True
                    is_superuser = True
                user = Model.objects.create_user(email=email,
                                                 password=password,
                                                 name=name,
                                                 surname=surname,
                                                 is_staff=is_staff,
                                                 is_superuser=is_superuser,
                                                 user_type=user_type)
                user.save()
                return HttpResponseRedirect(reverse('login'))
    else:
        form = RegistrationForm()

    return render(request, 'authentication/registration.html', {'form': form})
