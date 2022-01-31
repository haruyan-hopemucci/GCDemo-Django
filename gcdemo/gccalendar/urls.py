from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import views_admin

urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(template_name='gccalendar/login.html'), name="login"),
    path('logout', auth_views.LogoutView.as_view(template_name='gccalendar/logout.html'), name="logout"),
    path('area_id/<int:area_id>/', views.area_id, name="area_id_weekly"),
    path('area_id/<int:area_id>/monthly/', views.area_id_monthly, name="area_id_monthly"),
    path('area_id/<int:area_id>/monthly/<str:yyyymm>/', views.area_id_monthly, name="area_id_monthly_ym"),
    path('admin/', views_admin.index, name="admin_index"),
]