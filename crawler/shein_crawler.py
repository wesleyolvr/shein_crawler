# shein_crawler.py
import sys
sys.path.append("/usr/src/app")

import time
from logs import CustomLogger
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.firefox.options import Options
from db.db_manager import DatabaseManager


db_manager = DatabaseManager()

class SheinCrawler:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.binary_location = "/usr/bin/chromedriver"
        self.driver = webdriver.Chrome(options=self.options)
        self.log = CustomLogger()
        self.url_base = "https://br.shein.com/"
        self.links_category = []
        self.list_category = []

    def run(self):
        self.driver.get(self.url_base)
        time.sleep(5)
        self.clic_icone()
        self.get_links_category()
        self.extract_category_from_url()
        for url, category in zip(self.links_category, self.list_category):
            self.scrape_shein_clothes_info(url_clothes=url, type_clothes=category)
            time.sleep(10)
        self.driver.quit()
        
    def clic_icone(self):
        try:
            elemento_icone = WebDriverWait(
                self.driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'i.iconfont.icon-close.she-close')))
            elemento_icone.click()
            
        except ElementClickInterceptedException:
            time.sleep(5)
            self.clic_icone()
            
        except Exception as e:
            self.log.error(f'Error on clic_icone {e}')
            print(e)
    
    def has_next_page(self):
        try:
            next_page = self.driver.find_element(By.CLASS_NAME, 'sui-pagination__next')
            if not next_page.get_attribute('disabled') == 'true':
                return True
            return False
        except NoSuchElementException:
            self.log.warning('No next page')
            return False

    def page_down_for_load_all_images(self):
        count = 0
        try:    
            body = self.driver.find_element(By.TAG_NAME, 'body')
            while count < 17:
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
                count += 1
        except Exception as e:
            self.log.error(f'Error on page_down_for_load_all_images {e}')
            print(e)            

    def get_links_category(self):
        try:    
            self.log.info('Extracting links from category')
            self.driver.get(self.url_base)
            category = self.driver.find_element(By.CLASS_NAME, 'ccc-hotzone').find_elements(By.XPATH,'//span/a')
            for cat in category:
                self.links_category.append(cat.get_attribute('href').split('?')[0])
        
        except Exception as e:
            self.log.error(f'Error on get_links_category {e}')
            print(e)

    def extract_category_from_url(self):
        try:
            for url in self.links_category:
                parts = url.split('/')
                if '-c-' in parts[-1]:
                    # Extract category from URL when '-c-' is present
                    category = parts[-1].split('-c-')[0]
                    print(f"URL : {url}, Categoria : {category}")
                if '-sc-' in parts[-1]:
                    # Extract category from URL when '-sc-' is present
                    category = parts[-1].split('-sc-')[0]
                    print(f"URL : {url}, Categoria : {category}")
                self.list_category.append(category)
                
        except Exception as e:
            self.log.error(f'Error on extract_category_from_url {e}')
            print(e)
    
    def check_data(self, new_product_data):
        if ',' in new_product_data['data_price']:
            new_product_data['data_price'] = float(new_product_data['data_price'].replace(',','.'))
            new_product_data['data_us_price'] = float(new_product_data['data_us_price'].replace(',','.'))
            new_product_data['data_us_origin_price'] = float(new_product_data['data_us_origin_price'].replace(',','.'))
        else:
            new_product_data['data_price'] = float(new_product_data['data_price'])
            new_product_data['data_us_price'] = float(new_product_data['data_us_price'])
            new_product_data['data_us_origin_price'] = float(new_product_data['data_us_origin_price'])
            
        if new_product_data['discount']:
            new_product_data['discount'] = float(new_product_data['discount'])
        if not any([new_product_data['data_price'], new_product_data['data_us_price'], new_product_data['data_us_origin_price']]):
            new_product_data['data_price'] = 0.0
            new_product_data['data_us_price'] = 0.0
            new_product_data['data_us_origin_price'] = 0.0
            
        return new_product_data
        
    def scrape_shein_clothes_info(self, url_clothes, type_clothes):
        self.driver.get(url_clothes)
        time.sleep(5)
        count = 1

        while count == 1 or self.has_next_page():
            self.page_down_for_load_all_images()
            itens_in_page = self.driver.find_elements('css selector','section[role="listitem"]')
            self.log.info(f'Extracting {count} page from category {type_clothes} ')
            count += 1
            for secao in itens_in_page:
                tag_a = secao.find_element('css selector', 'a')
                if tag_a.get_attribute('data-price') == '':
                     continue
                product_type = type_clothes.replace('-',' ')
                new_product_data = {
                    'product_id': tag_a.get_attribute('data-id'),
                    'href': tag_a.get_attribute('href'),
                    'data_title': tag_a.get_attribute('data-title'),
                    'data_price': tag_a.get_attribute('data-price'),
                    'data_id_category': tag_a.get_attribute('data-cat_id'),
                    'data_sku': tag_a.get_attribute('data-sku'),
                    'data_spu': tag_a.get_attribute('data-spu'),
                    'data_us_price': tag_a.get_attribute('data-us-price'),
                    'data_us_origin_price': tag_a.get_attribute('data-us-origin-price'),
                    'discount': tag_a.get_attribute('data-discount'),
                    'image_src': secao.find_element('css selector', 'img').get_attribute('src'),
                    'product_type': product_type
                    }
                new_product_data = self.check_data(new_product_data)
                db_manager.create_product_or_update(product_data=new_product_data)
            try:
                next_page = self.driver.find_element(By.CSS_SELECTOR, '.sui-pagination__next.sui-pagination__btn')
                next_page.click()
                time.sleep(9)
            except ElementClickInterceptedException as e:
                self.log.warning(f'warning on next_page')
                body = self.driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.END)
                time.sleep(2)
                next_page = self.driver.find_element(By.CSS_SELECTOR, '.sui-pagination__next.sui-pagination__btn')
                next_page.click()
            except Exception as e:
                self.log.error(f'Error on next_page {e}')
                print(e)



if __name__ == "__main__":

    # Cria uma instância do SheinCrawler
    shein_crawler = SheinCrawler()
    shein_crawler.run()