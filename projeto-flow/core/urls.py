from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('institution/', include('institution.urls')),
    path('proposals/', include('proposals.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
