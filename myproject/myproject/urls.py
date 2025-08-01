from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),              # HTML pages
    path('store/api/', include('store.api.urls')),      # API endpoints
]
