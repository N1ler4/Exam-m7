from django.urls import path
from .views import (ContactView,
                    puplication_detail,
                    puplication_list,
                    PublicationCreateView,
                    papers_detail,
                    papers_list,
                    PaperCreateView,
                    requirements_detail,
                    RequirementsView,)


urlpatterns = [
    path('contact/', ContactView.as_view(), name='contact'),  
    
    path('publications/', puplication_list, name='publications'),
    path('puplication/<int:pk>/', puplication_detail, name='word-detail'), 
    path('publication/', PublicationCreateView.as_view(), name='publication_post'),
    
    path('papers/', papers_list, name='papers'),
    path('papers/<int:pk>/', papers_detail, name='paper-detail'),
    path('paper/', PaperCreateView.as_view(), name='papers-viewset'),
    
    path('requirements/', RequirementsView.as_view(), name='requirements'),
    path('requirements/<int:pk>/', requirements_detail, name='requirement-detail'),
    path('requirement/', RequirementsView.as_view(), name='requirement-viewset'),
]