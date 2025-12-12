from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
import shared.views

urlpatterns = (
    [
        path('i18n/', include('django.conf.urls.i18n')),
        path('setlang/<str:langcode>/', shared.views.setlang, name='setlang'),
    ]
    + i18n_patterns(
        path('admin/', admin.site.urls),
        path('', shared.views.index, name="index"),
        path('', include('accounts.urls')),
        path('subjects', include('subjects.urls')),
    )
)