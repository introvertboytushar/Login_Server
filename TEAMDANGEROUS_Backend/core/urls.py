from django.urls import path, include

urlpatterns = [
    path('api/', include('authentication.urls')),
]
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
]
