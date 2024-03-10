from django.urls import path
from .views import ProcessResultsView, GetResultsView, DownloadFile

urlpatterns = [
    path('process-results/<str:keyword>/', ProcessResultsView.as_view(), name='process-results'),
    path('get-results/<str:company>/', GetResultsView.as_view(), name='get-results'),
    path('download/core/<str:keyword>/<str:file_path>/', DownloadFile.as_view(), name='download_file'),
]