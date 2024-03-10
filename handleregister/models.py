from django.db import models

class SearchRecord(models.Model):
    keyword = models.CharField(max_length=255, default=None)

class ProcessedCompany(models.Model):
    search_record = models.ForeignKey(SearchRecord, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255, default=None)

class DownloadedFile(models.Model):
    company = models.ForeignKey(ProcessedCompany, on_delete=models.CASCADE, default=None)
    file_path = models.CharField(max_length=255, default=None)
