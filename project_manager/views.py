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
    user = {'id': request.user.id, 'name': request.user.get_full_name()}
    projects = [
            {
            'title': project.title,
            'description': project.description,
            'instructor': project.instructor.get_full_name(),
            }
            for project in projects
    ]
    return render(request, 'project_manager/dashboard.html',
                  {'projects': projects, 'user': user})


#TODO
@require_authorized
def add_student(request):
    user = User.objects.get(pk=request.user.id)
    try:
        doc = Document.objects.get(pk=id)
    except Document.DoesNotExist:
        return HttpResponse('No such book')
    else:
        if doc.return_doc(user):
            return HttpResponseRedirect(reverse('my_books'))
        else:
            return HttpResponse('You do not have this doc')
