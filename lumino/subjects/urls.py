from django.urls import path, register_converter
from . import views, converters

app_name = 'subjects'
register_converter(converters.SubjectConverter, 'subject')

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('<subject:subject>/', views.subject_detail, name='subject-detail'),
    path('unenroll/', views.unenroll_subjects, name="unenroll-subjects"),
]
