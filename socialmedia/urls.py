from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),
    path('social/', include('social.urls')),
    path('', RedirectView.as_view(url='social/'))
]

if settings.DEBUG == True:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
