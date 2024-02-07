from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RefCodesViewSet, send_code, UserViewSet
router = DefaultRouter()

router.register('users',
                UserViewSet,
                basename='users')


urlpatterns = [
    path('sendcode/',
         send_code,
         name='send_code'),
    path('code/', RefCodesViewSet.as_view()),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('', include(router.urls),),
]
