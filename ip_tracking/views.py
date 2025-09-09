from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit


# Create your views here.
# Anonymous users
@ratelimit(key='ip', rate='5/m', method='get', block=True)
# Authenticated users
@ratelimit(key='ip', rate='10/m', method='get', block=True)
def homepage_view(request):
    return HttpResponse("Home page")