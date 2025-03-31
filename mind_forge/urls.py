from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from tasks.views import TestCaseViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="MindForge API",
        default_version='v1',
        description="Документация для API",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
router = DefaultRouter()
router.register('test-cases', TestCaseViewSet)
urlpatterns = [

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/v1/users/', include('users.urls')),
    path('api/v1/tasks/', include('tasks.urls')),
    path('api/v1/submissions', include('submissions.urls')),
    path(r'api/v1/', include(router.urls)),

]
