from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home(request):
    return redirect(to='expenses')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('expenses/', include('expenses.urls')),
    path('authentication/', include('authentication.urls')),
    path('userpreferences/', include('userpreferences.urls')),
]
