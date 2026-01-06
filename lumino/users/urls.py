from django.urls import path, register_converter
from . import views, converters

app_name = 'users'
register_converter(converters.ProfileConverter, 'user')

urlpatterns = [
    path('<user:user>/', views.user_detail, name='user-detail'),
]
