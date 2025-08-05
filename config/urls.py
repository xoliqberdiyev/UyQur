from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from config.conf.drf_yasg import schema_view


urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Api V1 
    path('api/v1/', include(
        [
            path('accounts/', include('core.apps.accounts.urls')),
            path('company/', include('core.apps.company.urls')),
            path('shared/', include('core.apps.shared.urls')),
            path('wherehouses/', include('core.apps.wherehouse.urls')),
            path('projects/', include('core.apps.projects.urls')),
            path('products/', include('core.apps.products.urls')),
            path('orders/', include('core.apps.orders.urls')),
            path('finance/', include('core.apps.finance.urls')),
        ]
    )),

    # Swagger and Redoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

# Media and Static Files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
