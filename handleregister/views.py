from django.shortcuts import render
from .models import ProcessedCompany, DownloadedFile, SearchRecord
from .serializers import DownloadedFileSerializer, ProcessedCompanySerializer
from django.http import HttpResponse
from core.settings import BASE_URL
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import views, response
from .tasks import scrape_and_download



class ProcessResultsView(views.APIView):
    """
    API endpoint for processing search results.

    Requires authentication.

    - To initiate scraping and downloading for a keyword.
    - If the keyword is already processed, returns a message.

    URL: /process-results/<str:keyword>/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, keyword, *args, **kwargs):
        """
        Handle GET request.

        Parameters:
        - keyword (str): The search keyword.

        Returns:
        - JSON Response: Message indicating the status of scraping.
        """
        search_record = SearchRecord.objects.filter(keyword=keyword).first()
        if not search_record:
            scrape_and_download.delay(keyword)
            return response.Response({"message": "Scraping and downloading initiated. Check status and results later."})
        else:
            return response.Response({"message": "The keyword is already scrapped."})



class GetResultsView(views.APIView):
    """
    API endpoint for retrieving processed search results.

    Requires authentication.

    - Retrieves processed companies and associated downloaded files for a keyword.

    URL: /get-results/<str:company>/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, company, *args, **kwargs):
        """
        Handle GET request.

        Parameters:
        - company (str): The company name or keyword.

        Returns:
        - JSON Response: Processed companies and associated downloaded files.
        """
        search_record = SearchRecord.objects.filter(keyword=company).first()
        processed_companies = ProcessedCompany.objects.filter(search_record=search_record)

        if processed_companies.exists():
            data = []
            for processed_company in processed_companies:
                downloaded_files = DownloadedFile.objects.filter(company=processed_company)
                company_data = {
                    "name": processed_company.name,
                    "downloaded_files": DownloadedFileSerializer(downloaded_files, many=True).data
                }
                data.append(company_data)

            return response.Response(data)
        else:
            return response.Response({"message": "No results found for the specified keyword."})



class DownloadFile(views.APIView):
    """
    API endpoint for downloading a file.

    Requires authentication.

    - Downloads the specified file for a keyword.

    URL: /download/<str:keyword>/<str:file_path>/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, keyword, file_path):
        """
        Handle GET request.

        Parameters:
        - keyword (str): The search keyword.
        - file_path (str): The path of the file to download.

        Returns:
        - File Response: Downloaded file.
        """
        absolute_path = f"core/{keyword}/{file_path}" 
        with open(absolute_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_path}"'
        return response
