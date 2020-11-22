from django.contrib import admin
from django.urls import path, include

from core.views import AuthorizationView

urlpatterns = [
    path('', AuthorizationView.as_view()),
    path('application/', include('application.urls')),
    path('users/', include('users.urls')),

    path('admin/', admin.site.urls),

]
