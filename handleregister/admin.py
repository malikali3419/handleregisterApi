from django.contrib import admin
from .models import ProcessedCompany, SearchRecord, DownloadedFile

admin.site.register(ProcessedCompany)
admin.site.register(SearchRecord)
admin.site.register(DownloadedFile)

