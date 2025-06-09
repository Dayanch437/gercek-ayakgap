from rest_framework.routers import DefaultRouter

from .viewsets import ContactViewSet

urlpatterns = []


router = DefaultRouter()
router.register("contanct", ContactViewSet)

urlpatterns += router.urls
