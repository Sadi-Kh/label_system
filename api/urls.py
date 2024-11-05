from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

router = DefaultRouter()
router.register(r'datasets', views.DatasetViewSet, basename='dataset')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'text-entries', views.TextEntryViewSet, basename='text-entry')
router.register(r'operators', views.OperatorViewSet, basename='operator')


urlpatterns = [
    path('api/', include(router.urls)),
    path('auth/login/', ObtainAuthToken.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    
]
