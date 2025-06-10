from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ContactView,
    PublicationViewSet,
    PapersViewSet,
    RequirementsViewSet,
    main_page
)

router = DefaultRouter()
router.register(r'publications', PublicationViewSet, basename='publication')
router.register(r'papers', PapersViewSet, basename='papers')
router.register(r'requirements', RequirementsViewSet, basename='requirements')

urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),
    path('main/', main_page, name='main_page'),
    path('', include(router.urls)),
]
