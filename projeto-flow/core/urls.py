from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('proposals/', include('proposals.urls')),
                  path('pesquisador/', include('pesquisador.urls')),
                  path('', include('user.urls')),
                  path('evaluations/', include('evaluations.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
