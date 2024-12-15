from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about-us/',views.about,name='about'),
    path('courses/',views.courses,name='courses'),
    path("teachers/",views.teachers,name="teachers"),
    path("contacts/",views.contacts,name="contacts"),
    path("get_subjects/",views.get_subjects,name='get_subjects')
]
