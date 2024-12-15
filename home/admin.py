from django.contrib import admin
from . models import Course, Subjects


class CourseAdmin(admin.ModelAdmin):
    list_display = ["courseName","coursePrice","courseDuration"]
    list_editable = ["coursePrice"]
    

admin.site.register(Course,CourseAdmin)
admin.site.register(Subjects)
