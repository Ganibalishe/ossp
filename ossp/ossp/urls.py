from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from ossp import settings

from django.conf.urls.static import static
from core.views import AuthorizationView

urlpatterns = [
    path('', AuthorizationView.as_view()),
    path('application/', include('application.urls')),
    path('users/', include('users.urls')),

    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

