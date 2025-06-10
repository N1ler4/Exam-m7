from django.urls import path
from .views import ContactView, puplication_detail , puplication_list , PublicationCreateView


urlpatterns = [
    path('publications/', puplication_list, name='publications'),
    path('contact/', ContactView.as_view(), name='contact'),  
    path('puplication/<int:pk>/', puplication_detail, name='word-detail'), 
    path('publication/', PublicationCreateView.as_view(), name='publication_post'),
]