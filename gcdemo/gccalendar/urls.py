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
    path('admin/area/list/', views_admin.area_list, name="admin_area_list"),
    path('admin/area/new/', views_admin.area_new, name="admin_area_new"),
    path('admin/area/edit/<int:area_id>/', views_admin.area_edit, name="admin_area_edit"),
    path('admin/area/delete/<int:area_id>/', views_admin.area_delete, name="admin_area_delete"),
    path('admin/gcday/new/', views_admin.gcday_new, name="admin_gcday_new"),
    path('admin/gctype/list/', views_admin.gctype_list, name="admin_gctype_list"),
    path('admin/gctype/new/', views_admin.gctype_new, name="admin_gctype_new"),
    path('admin/gctype/edit/<int:gctype_id>/', views_admin.gctype_edit, name="admin_gctype_edit"),
    path('admin/gctype/delete/<int:gctype_id>/', views_admin.gctype_delete, name="admin_gctype_delete"),
    path('admin/gcdaysbulksetting/', views_admin.gcdays_bulk_setting, name="admin_gcdays_bulk_setting"),
 ]