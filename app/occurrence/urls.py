from django.urls import path, include
from rest_framework.routers import DefaultRouter

from occurrence import views


router = DefaultRouter()
router.register('', views.OccurrenceViewSet)

app_name = 'occurrence'

urlpatterns = [
    path('', include(router.urls))
]
