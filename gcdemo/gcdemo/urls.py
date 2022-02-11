from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index),
    path('accounts/profile/', views.profile),
    path('gccalendar/', include('gccalendar.urls')),
    path('admin/', admin.site.urls),
]