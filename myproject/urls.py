from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    url(r'^users/', include('users.urls')),
    url(r'^feed/', include('feed.urls')),
    url(r'^admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
