from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("create/", views.EmployeeCreate.as_view(), name="create_emp"),
    path("employees/", views.EmployeeView.as_view(), name="emp_list"),
    path("emp-details/<int:pk>", views.EmployeeDetail.as_view(), name="emp_details"),
    path("empupdate/<int:pk>/", views.EmployeeUpdate.as_view(), name="emp_update"),
    path("empdelete/<int:pk>/", views.EmployeeDelete.as_view(), name="emp_delete"),
    path("home/", views.Home.as_view(), name="home"),
    path("addemp/", views.add_emp, name="addemp"),
    path("", views.upload_file, name="upload_file"),  #home file
    path("upload-csv/", views.upload_csv, name="upload_csv"),
    path("download-csv/", views.export_emp_csv, name="download_csv"),
    path("delete-all", views.delete_all_emp, name="delete_all_emp"),
    path('update/<int:id>/', views.add_emp, name='addemp'),
    path('employee/updatenew/<int:id>/',views.EmpUpdate.as_view(), name="new_update"),
    path('employee/createnew/',views.EmpUpdate.as_view(), name="new_create"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


