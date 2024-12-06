from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from core.views import BuildingViewSet, RoomViewSet, ResidentViewSet, EventViewSet
from management.auth_view import login_view
from django.contrib import admin

schema_view = get_schema_view(
    openapi.Info(
        title="UniResMan API",
        default_version='v1',
        description="API documentation for UniResMan",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auth/login', login_view, name='login'),
    path('auth/logout', login_view, name='logout'),

    # Building API endpoints
    path('api/buildings/', BuildingViewSet.as_view({'get': 'list', 'post': 'create'}), name='building-list-create'),
    path('api/buildings/<int:pk>/', BuildingViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='building-detail'),

    # Room API endpoints
    path('api/rooms/', RoomViewSet.as_view({'get': 'list', 'post': 'create'}), name='room-list-create'),
    path('api/rooms/<int:pk>/', RoomViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='room-detail'),

    # # Resident API endpoints
    # path('api/residents/', ResidentViewSet.as_view({'get': 'list', 'post': 'create'}), name='resident-list-create'),
    # path('api/residents/<int:pk>/', ResidentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='resident-detail'),

    # # Event API endpoints
    path('api/events/', EventViewSet.as_view({'get': 'list', 'post': 'create'}), name='event-list-create'),
    path('api/events/<int:pk>/', EventViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='event-detail'),
]
