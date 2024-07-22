from django.db import models

# Create your models here.


class Employee(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    mobile = models.CharField(max_length=10)
    email = models.EmailField()

    class Meta:
        db_table = "employee"

    def __str__(self):
        return f"{self.__dict__}"


class Document(models.Model):
    title = models.CharField(max_length=25)
    uploaded_file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "document"

    def __str__(self):
        return self.title
