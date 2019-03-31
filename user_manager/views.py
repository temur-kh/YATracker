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
def personal(request):
    user = User.objects.get(pk=request.user.id)
    return render(request, 'user_manager/account.html', {'user': user})
