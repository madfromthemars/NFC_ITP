# Django
from django.contrib import admin
from django.urls import path, include

# REST
from rest_framework import permissions

# 3rd party
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="NFC-GLOBAL-TECH API",
      default_version='v1',
      # description="Test description",
      # terms_of_service="url",
      # contact=openapi.Contact(email=""),
      # license=openapi.License(name=""),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('main.urls')),
    path('api/v2/', include('v2.urls')),

    # path('api/doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/schema<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
