from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(template_name='login.html')),
    path('area_id/<int:area_id>/', views.area_id, name="area_id"),
    path('area_id/<int:area_id>/monthly/', views.area_id_monthly, name="area_id_monthly"),
    path('area_id/<int:area_id>/monthly/<str:yyyymm>/', views.area_id_monthly, name="area_id_monthly"),
]