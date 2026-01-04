from django.urls import path, register_converter
from . import views, converters

app_name = 'users'
register_converter(converters.ProfileConverter, 'user')

urlpatterns = [
    path('<user:user>/', views.user_detail, name='user-detail'),
    path('<user:user>/edit/', views.edit_profile, name='edit-profile'),
    path('<user:user>/leave/', views.leave, name='leave'),
]
