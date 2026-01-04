from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
import shared.views
import django.views.i18n

urlpatterns = (
    [
        path('i18n/', include('django.conf.urls.i18n')),
        path('setlang/<str:langcode>/', django.views.i18n.set_language, name='setlang'),
        path('django-rq/', include('django_rq.urls')),
    ]
    + i18n_patterns(
        path('admin/', admin.site.urls),
        path('', shared.views.index, name='index'),
        path('', include('accounts.urls')),
        path('subjects/', include('subjects.urls')),
        path('users/', include('users.urls')),
    )
)