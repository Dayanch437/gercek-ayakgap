from django.urls import path
from rest_framework.routers import DefaultRouter

from .viewsets import Contact, ContactViewSet

urlpatterns = []



router = DefaultRouter()
router.register('contanct',ContactViewSet)

urlpatterns+=router.urls
