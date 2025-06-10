from rest_framework import generics, permissions
from .models import Contact, Publication
from .serializers import ContactSerializer, PublicationSerializer
from rest_framework.response import Response
from rest_framework import status , viewsets, filters
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView


class ContactView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

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


class PublicationCreateView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(request_body=PublicationSerializer)
    def post(self, request, *args, **kwargs):
        serializer = PublicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def puplication_list(request):
    if request.method == 'GET':
        publications = Publication.objects.all()
        serializer = PublicationSerializer(publications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def puplication_detail(request , pk):
    try:
        pub_pk = Publication.objects.get(pk=pk)
    except Publication.DoesNotExist:
        return Response({"error": "Publication not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PublicationSerializer(pub_pk)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = PublicationSerializer(pub_pk, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        pub_pk.delete()
        return Response({"message": "Publication deleted"}, status=status.HTTP_204_NO_CONTENT)
         