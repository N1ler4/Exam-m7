from rest_framework import generics, permissions, status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes , permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema

from .models import Contact, Papers, Publication, Requirements
from .serializers import ContactSerializer, PapersSerializer, PublicationSerializer, RequirementsSerializer
from .permissions import IsOwnerOrReadOnly

# --- Contact ---

class ContactView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["Contact"], request_body=ContactSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()

        send_mail(
            subject=f'Contact from {contact.name}',
            message=f'Email: {contact.email}\n\n{contact.message}\n\n{contact.created_at}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['bahtiyorov.nozim@gmail.com'],
        )

        return Response({"message": "Сообщение успешно отправлено"}, status=status.HTTP_201_CREATED)


# --- Publication ---

class PublicationCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["Publication"], request_body=PublicationSerializer)
    def post(self, request, *args, **kwargs):
        serializer = PublicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', tags=['Publication'], responses={200: PublicationSerializer(many=True)})
@api_view(['GET'])
def puplication_list(request):
    publications = Publication.objects.all()
    serializer = PublicationSerializer(publications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', tags=['Publication'], responses={200: PublicationSerializer()})
@swagger_auto_schema(method='put', tags=['Publication'], request_body=PublicationSerializer)
@swagger_auto_schema(method='delete', tags=['Publication'])
@parser_classes([MultiPartParser, FormParser])
@api_view(['GET', 'PUT', 'DELETE'])
def puplication_detail(request, pk):
    try:
        pub_pk = Publication.objects.get(pk=pk)
    except Publication.DoesNotExist:
        return Response({"error": "Publication not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PublicationSerializer(pub_pk)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = PublicationSerializer(pub_pk, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        pub_pk.delete()
        return Response({"message": "Publication deleted"}, status=status.HTTP_204_NO_CONTENT)


# ----- Papers ------

class PaperCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["Papers"], request_body=PapersSerializer)
    def post(self, request, *args, **kwargs):
        serializer = PapersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', tags=['Papers'], responses={200: PapersSerializer(many=True)})
@api_view(['GET'])
def papers_list(request):
    papers = Papers.objects.all()
    serializer = PapersSerializer(papers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', tags=['Papers'], responses={200: PapersSerializer()})
@swagger_auto_schema(method='put', tags=['Papers'], request_body=PapersSerializer)
@swagger_auto_schema(method='delete', tags=['Papers'])
@api_view(['GET', 'PUT', 'DELETE'])
def papers_detail(request, pk):
    try:
        paper = Papers.objects.get(pk=pk)
    except Papers.DoesNotExist:
        return Response({"error": "Paper not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        paper.view_count += 1
        paper.save()
        serializer = PapersSerializer(paper)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = PapersSerializer(paper, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        paper.delete()
        return Response({"message": "Paper deleted"}, status=status.HTTP_204_NO_CONTENT)


# --- Requirements ---

class RequirementsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["Requirements"], request_body=RequirementsSerializer)
    def post(self, request, *args, **kwargs):
        serializer = RequirementsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='get', tags=['Requirements'], responses={200: RequirementsSerializer(many=True)})
@api_view(['GET'])
def requirements_list(request):
    requirements = Requirements.objects.all()
    serializer = RequirementsSerializer(requirements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', tags=['Requirements'], responses={200: RequirementsSerializer()})
@swagger_auto_schema(method='put', tags=['Requirements'], request_body=RequirementsSerializer)
@swagger_auto_schema(method='delete', tags=['Requirements'])
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsOwnerOrReadOnly])
def requirements_detail(request, pk):
    try:
        requirement = Requirements.objects.get(pk=pk)
    except Requirements.DoesNotExist:
        return Response({"error": "Requirement not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RequirementsSerializer(requirement)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = RequirementsSerializer(requirement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        requirement.delete()
        return Response({"message": "Requirement deleted"}, status=status.HTTP_204_NO_CONTENT)
