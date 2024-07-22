from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View

from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.base import TemplateView

from .models import Employee, Document
from .forms import EmployeeForm

from django.urls import reverse, reverse_lazy

from django.core.files.storage import FileSystemStorage
import csv

# Create your views here.


class AddEmp(TemplateView):
    model = Employee
    template_name = "new_form.html"


class Home(ListView):
    model = Employee
    template_name = "index.html"
    context_object_name = "employees"


class EmployeeCreate(CreateView):
    model = Employee
    fields = "__all__"
    success_url = reverse_lazy("home")


class EmployeeView(ListView):
    model = Employee
    template_name = "employee_list.html"
    context_object_name = "employees"


class EmployeeDetail(DetailView):
    model = Employee
    template_name = "employee_details.html"
    context_object_name = "employee"


class EmployeeUpdate(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = "employee_update.html"
    success_url = reverse_lazy("home")


class EmployeeDelete(DeleteView):
    model = Employee
    template_name = "employee_delete.html"
    success_url = reverse_lazy("home")


def upload_file(request):
    if request.method == "POST" and request.FILES["document"]:
        file = request.FILES["document"]
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)

        # save to database
        document = Document(title=request.POST["title"], uploaded_file=filename)
        document.save()

        return render(
            request, "app/upload_success.html", {"uploaded_file_url": uploaded_file_url}
        )
    return render(request, "app/upload.html")


def upload_csv(request):
    if request.method == "POST" and request.FILES["csv_file"]:
        csv_file = request.FILES["csv_file"]
        fs = FileSystemStorage()
        filename = fs.save(csv_file.name, csv_file)
        # uploaded_file_url = fs.url(filename)

        # process the csv file
        with open(fs.path(filename), newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # to skip the header row
            for row in reader:
                Employee.objects.create(
                    first_name=row[0], last_name=row[1], mobile=row[2], email=row[3]
                )

        # return render(request, 'upload_success.html', {'uploaded_file_url' : uploaded_file_url})
        return redirect("home")
        # return success_url = reverse_lazy("home")
    return render(request, "upload.html")


# to download Employee Data in CSV format.


def export_emp_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="employee.csv"'

    writer = csv.writer(response)

    writer.writerow(["ID", "First Name", "Last Name", "Mobile num", "Email"])

    employees = Employee.objects.all()

    for emp in employees:
        writer.writerow([emp.id, emp.first_name, emp.last_name, emp.mobile, emp.email])

    return response


# delete all employees


def delete_all_emp(request):
    Employee.objects.all().delete()
    return redirect("home")


# to add emp


def add_emp(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")

        # Create and save the Employee object
        Employee.objects.create(
            first_name=first_name, last_name=last_name, mobile=mobile, email=email
        )

        return redirect("home")
    return render(request, "upload.html")


# ------------------update mix------------------


# def add_emp(request, id=None):
#     if request.method == "POST":
#         first_name = request.POST.get("first_name")
#         last_name = request.POST.get("last_name")
#         mobile = request.POST.get("mobile")
#         email = request.POST.get("email")

#         if not request.POST.get("id"):
#             # Create and save the Employee object
#             Employee.objects.create(
#                 first_name=first_name, last_name=last_name, mobile=mobile, email=email
#             )
#         else:
#             emp = Employee.objects.get(id=request.POST.get("id"))
#             emp.first_name = first_name
#             emp.last_name = last_name
#             emp.mobile = mobile
#             emp.email = email
#             emp.save()

#         return redirect("home")
#     elif request.method == "GET":
#         return render(request=request, template_name="upload.html")


# def get_employee(request, eid):
#     emp = Employee.objects.get(id=eid)
#     return render(
#         request=request,
#         template_name="upload.html",
#         context={"employee": emp},
#     )

class EmpUpdate(View):
    template_name = "upload.html"

    def get(self, request, id=None):
        employee = get_object_or_404(Employee, id=id) if id else None
        return render(request, self.template_name, {'employee': employee})
    
    def post(self, request, id=None):
        employee = get_object_or_404(Employee, id=id) if id else Employee()
        employee.first_name = request.POST.get('first_name')
        employee.last_name = request.POST.get('last_name')
        employee.email = request.POST.get('email')
        employee.mobile = request.POST.get('mobile')
        employee.save()
        return redirect('home')