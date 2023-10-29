from functools import wraps
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
import json
def ajax_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)
        js = json.dumps({ 'authenticated': False, 'login': reverse('account_login') })
        login = reverse("account_login")
        return JsonResponse({'authenticated': False, 'login': login})
    return wrapper