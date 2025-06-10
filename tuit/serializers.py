from rest_framework import serializers
from .models import Contact, Publication , Papers , Requirements 


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message', 'created_at']
        read_only_fields = ['created_at']
       
       
class PublicationSerializer(serializers.ModelSerializer):
    
    image = serializers.ImageField(required=False)  
    
    class Meta:
        model = Publication
        fields = ['id','title', 'content', 'image' , 'author']


class PapersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Papers
        fields = ['id', 'title', 'abstract', 'authors', 'publication_date', 'journal_name', 'keywords', 'view_count', 'publication', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at' , 'view_count']

class RequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirements
        fields = ['id', 'name', 'title', 'description']
        read_only_fields = ['id']