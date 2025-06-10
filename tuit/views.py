from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from .models import Contact, Papers, Publication, Requirements
from .serializers import ContactSerializer, PapersInputSerializer, PapersSerializer, PublicationSerializer, RequirementsSerializer
from .permissions import IsOwnerOrReadOnly


# --- Contact View ---
class ContactView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=ContactSerializer, tags=['Contact'])
    def post(self, request, *args, **kwargs):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()

        send_mail(
            subject=f'Contact from {contact.name}',
            message=f'Email: {contact.email}\n\n{contact.message}\n\n{contact.created_at}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['bahtiyorov.nozim@gmail.com'],
        )

        return Response({"message": "Сообщение успешно отправлено"}, status=status.HTTP_201_CREATED)


# --- Publication ViewSet ---
class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    swagger_tags = ['Publications']

    @swagger_auto_schema(request_body=PublicationSerializer, tags=['Publications'])
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --- Papers ViewSet ---
class PapersViewSet(viewsets.ModelViewSet):
    queryset = Papers.objects.all()
    serializer_class = PapersSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        request_body=PapersInputSerializer,
        responses={200: PapersSerializer},
        tags=['Papers']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=PapersInputSerializer,
        responses={200: PapersSerializer},
        tags=['Papers']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Papers'])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Papers'])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Papers'])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(tags=['Papers'])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# --- Requirements ViewSet ---
class RequirementsViewSet(viewsets.ModelViewSet):
    queryset = Requirements.objects.all()
    serializer_class = RequirementsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    swagger_tags = ['Requirements']

    @swagger_auto_schema(request_body=RequirementsSerializer, tags=['Requirements'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
