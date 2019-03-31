from django.db.models import Q
from .models import Project
from django.shortcuts import render
from django.urls import reverse
from django.http import (
    HttpResponseRedirect,
    HttpResponse,
)

from django.contrib.auth import get_user_model

User = get_user_model()


def require_authorized(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        return function(request, *args, **kwargs)

    return wrapper


@require_authorized
def index(request):
    user = User.objects.get(pk=request.user.id)

    projects = Project.objects.filter(
        Q(students__pk=user.pk) |
        Q(instructor__pk=user.pk)
    ).distinct()
    return render(request, 'project_manager/dashboard.html',
                  {'projects': projects, 'user': user})


@require_authorized
def project_view(request, id):
    user = User.objects.get(pk=request.user.id)
    project = Project.objects.get(pk=id)
    if project.students.filter(pk=user.id).exists() or project.instructor.filter(pk=user.id).exists():
        return render(request, 'project_manager/project_page.html',
                      {'project': project})  # waiting for project.html implementation
    else:
        return HttpResponseRedirect(reverse('dashboard'))
