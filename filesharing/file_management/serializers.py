from rest_framework import serializers
from django.urls import reverse
from django.core import signing
from .models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('id', 'file', 'uploaded_by', 'uploaded_on', 'download_url')

    download_url = serializers.SerializerMethodField()

    def get_download_url(self, obj):
        request = self.context.get('request')
        # if request and request.user.is_authenticated and not request.user.is_ops_user:
        # Generate a unique, time-limited token for the download link
        token = signing.dumps({'file_id': obj.id, 'user_id': request.user.id})
        # Create the download URL using reverse with the token as a query parameter
        download_url = reverse('download', kwargs={'token': token})
        return request.build_absolute_uri(download_url)
        # return None
