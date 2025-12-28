from django.urls import path, register_converter
from . import views, converters

app_name = 'subjects'
register_converter(converters.SubjectConverter, 'subject')
register_converter(converters.LessonConverter, 'lesson')

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('<subject:subject>/', views.subject_detail, name='subject-detail'),
    path('<subject:subject>/lessons/<lesson:lesson>/', views.lesson_detail, name='lesson-detail'),
    path('<subject:subject>/lessons/<lesson:lesson>/edit/', views.edit_lesson, name='edit-lesson'),
    path('<subject:subject>/lessons/<lesson:lesson>/delete/', views.delete_lesson, name='delete-lesson'),
    path('<subject:subject>/marks/', views.mark_list, name='mark-list'),
    path('<subject:subject>/marks/edit', views.edit_marks, name='edit-marks'),
    path('enroll/', views.enroll_subjects, name="enroll-subjects"),
    path('unenroll/', views.unenroll_subjects, name="unenroll-subjects"),
    path('certificate/', views.request_certificate, name="request-certificate"),
]
