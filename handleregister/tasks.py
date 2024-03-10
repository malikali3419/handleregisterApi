from celery import shared_task
from .models import ProcessedCompany, DownloadedFile
from .scraper import HandelsregisterScraper 
import os

@shared_task
def scrape_and_download(keyword):
    os.makedirs(f"core/{keyword}", exist_ok=True)
    scraper = HandelsregisterScraper(url='https://www.handelsregister.de/rp_web/normalesuche.xhtml', download_directory=f'core/{keyword}', serach_key_word=keyword)
    scraper.navigate_and_search()
    scraper.process_results()
    scraper.quit_driver()