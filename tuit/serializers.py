from rest_framework import serializers
from .models import Contact, Publication, Papers, Requirements


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message', 'created_at']
        read_only_fields = ['created_at']


class PublicationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Publication
        fields = ['id', 'title', 'content', 'image', 'author', 'user']
        read_only_fields = ['user']


class PapersInputSerializer(serializers.ModelSerializer):
    publication_id = serializers.PrimaryKeyRelatedField(
        queryset=Publication.objects.all(),
        source='publication',
        write_only=True
    )
    
    class Meta:
        model = Papers
        fields = [
            'title', 'abstract', 'authors', 'publication_date',
            'journal_name', 'keywords', 'publication_id'
        ]


class PapersSerializer(serializers.ModelSerializer):
    publication = PublicationSerializer(read_only=True)
    publication_id = serializers.PrimaryKeyRelatedField(
        queryset=Publication.objects.all(),
        source='publication',
        write_only=True
    )

    class Meta:
        model = Papers
        fields = [
            'id', 'title', 'abstract', 'authors', 'publication_date',
            'journal_name', 'keywords', 'view_count', 'publication',
            'publication_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'view_count', 'publication']
        
class RequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirements
        fields = ['id', 'name', 'title', 'description', 'user']
        read_only_fields = ['id', 'user']
