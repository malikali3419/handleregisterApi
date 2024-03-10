from rest_framework import serializers
from .models import ProcessedCompany, DownloadedFile

class DownloadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadedFile
        fields = ['file_path']

class ProcessedCompanySerializer(serializers.ModelSerializer):
    downloaded_files = DownloadedFileSerializer(many=True, read_only=True)

    class Meta:
        model = ProcessedCompany
        fields = ['name', 'downloaded_files']