"""product_catalog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.product.urls import urlpatterns as product_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Product Catalog API",
        default_version='v1',
        description="This is simple API for product catalog",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@admin.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),

    # Local apps urls
    path('products/', include((product_urls, 'apps.product'), namespace='product')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
urlpatterns += [
                   # static files (images, css, javascript, etc.)
                   re_path(r'^static/(?P<path>.*)$', serve)] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
