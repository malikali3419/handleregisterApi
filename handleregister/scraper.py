from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from .models import SearchRecord, ProcessedCompany, DownloadedFile
from core.settings import BASE_URL

class HandelsregisterScraper:
    def __init__(self, url, download_directory, serach_key_word):
        self.url = url
        self.download_directory = download_directory
        self.initialize_driver()
        self.search_keyword = serach_key_word
        self.processed_ads = set()
        self.processed_cds = set()
        self.processed_hds = set()
        self.processed_sis = set()
        self.processed_elements = set()

    def initialize_driver(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-notifications")

        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_directory,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False
        })

        self.driver = webdriver.Chrome(options=chrome_options)

    def navigate_and_search(self):
        self.driver.get(self.url)

        text_area_id = 'form:schlagwoerter'
        text_area_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, text_area_id)))
        text_area_element.send_keys(self.search_keyword)

        button_id = 'form:btnSuche'
        button_element = self.driver.find_element(By.ID, button_id)
        self.driver.execute_script("arguments[0].click();", button_element)

        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.url_changes("https://www.handelsregister.de/rp_web/ergebnisse.xhtml"))
        search_record = SearchRecord.objects.create(keyword=self.search_keyword)
        search_record.save()

    def process_results(self, num_results=100):
        dropdown_css_selector = "select[name='ergebnissForm:selectedSuchErgebnisFormTable_rppDD']"
        dropdown = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, dropdown_css_selector)))

        select = Select(dropdown)
        select.select_by_value(str(num_results))
        time.sleep(20)
        for i in range(5):
            try:
                table = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.ID, 'ergebnissForm:selectedSuchErgebnisFormTable_data'))
                    )
                company_rows = table.find_elements(By.TAG_NAME, 'tr')
                for company_row in company_rows:
                    try:
                        
                        company_td = company_row.find_elements(By.TAG_NAME, 'td')
                        if len(company_td) >= 1:
                            company_tab = company_td[0].find_elements(By.TAG_NAME, 'table')
                            if len(company_tab) >= 1:
                                company_tr = company_tab[0].find_elements(By.TAG_NAME, 'tr')
                                if len(company_tr) >= 2:
                                    company_name = company_tr[1].find_element(By.TAG_NAME, 'td').text
                                    company_name = company_tr[1].find_element(By.TAG_NAME, 'td').text
                                    search_record = SearchRecord.objects.filter(keyword=self.search_keyword).first()
                                    print(search_record.keyword)
                                    if search_record:
                                        processed_company, created = ProcessedCompany.objects.get_or_create(search_record=search_record, name=company_name)
                                        if created:
                                            print(f"Processed company {company_name} created.")
                                        else:
                                            print(f"Processed company {company_name} already exists.")
                                    company_ad = company_tr[1].find_elements(By.TAG_NAME, "td")
                                    if len(company_ad) >= 1:
                                        tds = company_ad[3].find_elements(By.TAG_NAME, 'div')
                                        if len(tds) >= 1:
                                            documents = tds[0].find_elements(By.TAG_NAME, 'a')
                                            if len(documents) >= 1:
                                                for document in documents:
                                                    try:     
                                                        if document.text == "AD":
                                                            if company_name in self.processed_ads:
                                                                print(f"Skipping previously processed company: {company_name}")
                                                                continue
                                                            self.processed_ads.add(company_name)
                                                            file_path = self.click_and_download(document)
                                                            download_link = BASE_URL + "download/"  + file_path
                                                            company = ProcessedCompany.objects.filter(id=processed_company.id).first()
                                                            if company:
                                                                downloaded_file = DownloadedFile.objects.create(company=company, file_path=download_link)
                                                                downloaded_file.save()
                                                        elif document.text == "CD":
                                                            if company_name in self.processed_cds:
                                                                print(f"Skipping previously processed company: {company_name}")
                                                                continue
                                                            self.processed_cds.add(company_name)
                                                            file_path = self.click_and_download(document)
                                                            download_link = BASE_URL + "download/"  + file_path
                                                            company = ProcessedCompany.objects.filter(id=processed_company.id).first()
                                                            if company:
                                                                downloaded_file = DownloadedFile.objects.create(company=company, file_path=download_link)
                                                                downloaded_file.save()
                                                        elif document.text == "HD":
                                                            if company_name in self.processed_hds:
                                                                print(f"Skipping previously processed company: {company_name}")
                                                                continue
                                                            file_path = self.click_and_download(document)
                                                            download_link = BASE_URL + "download/"  + file_path
                                                            company = ProcessedCompany.objects.filter(id=processed_company.id).first()
                                                            if company:
                                                                downloaded_file = DownloadedFile.objects.create(company=company, file_path=download_link)
                                                                downloaded_file.save()
                                                        elif document.text == "SI":
                                                            if company_name in self.processed_sis:
                                                                print(f"Skipping previously processed company: {company_name}")
                                                                continue
                                                            self.processed_sis.add(company_name)
                                                            file_path = self.click_and_download(document)
                                                            download_link = BASE_URL + "download/"  + file_path
                                                            company = ProcessedCompany.objects.filter(id=processed_company.id).first()
                                                            if company:
                                                                downloaded_file = DownloadedFile.objects.create(company=company, file_path=download_link)
                                                                downloaded_file.save()
                                                    except Exception as e:
                                                        self.driver.back()
                                                        continue
                                            else:
                                                print("No 'a' elements found within the div")
                                        else:
                                            print("No div elements found within the fourth td")
                                    else:
                                        print("Not enough td elements within the fifth tr")
                                else:
                                    print("Not enough tr elements within the first table")
                            else:
                                print("Not enough table elements within the first td")
                        else:
                            print("Not enough td elements within the row")

                    except Exception as e:
                        print("ERROR", e)
                        break
                
            except Exception as e:
                print("Stale element reference, retrying...")
                self.driver.get("https://www.handelsregister.de/rp_web/ergebnisse.xhtml")
                continue
    def click_and_download(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth' });", element)
        self.driver.execute_script("arguments[0].click();", element)
        wait = WebDriverWait(self.driver, 30)
        wait.until(lambda driver: len(os.listdir(self.download_directory)) > 0)
        time.sleep(10)
        files = os.listdir(self.download_directory)
        files = [os.path.join(self.download_directory, file) for file in files]
        latest_file = max(files, key=os.path.getmtime)
        print("Latest downloaded file:", latest_file)
        return latest_file

    def quit_driver(self):
        self.driver.quit()

