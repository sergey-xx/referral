from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RefCodesViewSet
router = DefaultRouter()

# router.register('code',
#                 RefCodesViewSet,
#                 basename='code')


urlpatterns = [
    path('code/', RefCodesViewSet.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls),),
]
