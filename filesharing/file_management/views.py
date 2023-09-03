import os

from django.core import signing
from django.http import FileResponse, Http404
from django.core.exceptions import ValidationError
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST
from . import models, serializers
from .utils import IsClientUser


class FileUploadView(APIView):
    """
    This API View is used for upload file. only Admin user can upload the file
    """

    parser_classes = (MultiPartParser,)
    permission_classes = [IsAdminUser]

    EMPTY_FILE_ERROR_MESSAGE = "File is not attached. Please upload file"
    FILE_SIZE_LIMIT = 500 * 1024 * 1024  # 500MD
    FILE_EXTENSION_ALLOWED = ['.pptx', '.docx', '.xlsx']

    def validate_file_extension(self, file_obj):

        ext = os.path.splitext(file_obj.name)[1]
        if ext.lower() not in self.FILE_EXTENSION_ALLOWED:
            raise ValidationError(f"Unsupported file type. Only PPTX, DOCX, and XLSX files are allowed.")

    def post(self, request):
        if not request.data.get('file'):
            return Response({'error': self.EMPTY_FILE_ERROR_MESSAGE}, status=HTTP_400_BAD_REQUEST)

        file_obj = request.data['file']

        # Validate file extension
        try:
            self.validate_file_extension(file_obj)
        except ValidationError as e:
            return Response({'error': str(e)}, status=HTTP_400_BAD_REQUEST)

        if file_obj and file_obj.size > self.FILE_SIZE_LIMIT:  # Check if file size is greater than 500MB
            return Response({'error': 'File size exceeds 500MB limit.'}, status=HTTP_400_BAD_REQUEST)

        # Save the uploaded file
        uploaded_file = models.UploadedFile(file=file_obj, uploaded_by=request.user)
        uploaded_file.save()

        return Response({'message': 'File uploaded successfully'})


class FileListView(generics.ListAPIView):
    queryset = models.UploadedFile.objects.all()
    permission_classes = [IsClientUser]
    serializer_class = serializers.UploadedFileSerializer


class FileDownloadView(APIView):
    permission_classes = [IsClientUser]

    def get(self, request, token):
        try:
            # Verify the token and get the file_id from it
            data = signing.loads(token)
            file_id = data['file_id']

            # Fetch the UploadedFile instance
            uploaded_file = models.UploadedFile.objects.get(id=file_id)

            # Ensure that the file exists in system
            if not os.path.isfile(uploaded_file.file.path):
                raise Http404("File not found")

            # Serve the file using FileResponse
            response = FileResponse(open(uploaded_file.file.path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
            return response
        except signing.BadSignature:
            raise Http404("Invalid token")
