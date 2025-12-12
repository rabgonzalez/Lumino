from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from . import views 
app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='subject-list'),
]
