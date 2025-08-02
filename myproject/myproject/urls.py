from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),                    # Store URLs at the root
    path('api/', include('store.api.urls')),            # API endpoints
    # Keep the old URLs for backward compatibility
    path('store/', include('store.urls')),              # HTML pages
    path('store/api/', include('store.api.urls')),      # API endpoints
]
