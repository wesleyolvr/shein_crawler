import json

from selenium import webdriver
from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from db.database import DATABASE_URL
from db.manager import DatabaseManager
from kafka.producer import KafkaProducer
from logs.logger import logger
from utils.utils import disable_element_by_class, wait_for


class SheinCrawler:
    def __init__(self):
        self.options = Options()
        self.db_manager = DatabaseManager(database_url=DATABASE_URL)
        # self.options.add_argument("--headless")
        # self.options.binary_location = "/usr/bin/chromedriver"
        self.driver = webdriver.Chrome(options=self.options)
        self.url_base = 'https://br.shein.com/'
        self.kafka_producer = KafkaProducer()
        self.links_category = []
        self.list_category = []

    def run(self):
        self.driver.get(self.url_base)
        wait_for(5)
        self.clic_icone()
        self.get_links_category()
        self.extract_category_from_url()
        for url, category in zip(self.links_category, self.list_category):
            self.scrape_shein_clothes_info(
                url_clothes=url, type_clothes=category
            )
            wait_for(10)
        self.driver.quit()

    def clic_icone(self):
        try:
            elemento_icone = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'i.iconfont.icon-close.she-close')
                )
            )
            elemento_icone.click()

        except ElementClickInterceptedException:
            wait_for(5)
            self.clic_icone()

        except Exception as e:
            logger.error(f'Error on clic_icone {e}')

    # def has_next_page(self):
    #     try:
    #         next_page = self.driver.find_element(By.CLASS_NAME, 'sui-pagination__next')
    #         if not next_page.get_attribute('disabled') == 'true':
    #             return True
    #         return False
    #     except NoSuchElementException:
    #         logger.warning('No next page')
    #         return False

    def has_next_page(self):
        try:
            next_page = self.driver.find_element(
                By.CLASS_NAME, 'sui-pagination__next'
            )
            return next_page.get_attribute('disabled') != 'true'
        except NoSuchElementException:
            logger.warning('No next page')
            return False

    def page_down_for_load_all_images(self):
        count = 0
        try:
            body = self.driver.find_element(By.TAG_NAME, 'body')
            while count < 17:
                body.send_keys(Keys.PAGE_DOWN)
                wait_for(1)
                count += 1
        except Exception as e:
            logger.error(f'Error on page_down_for_load_all_images {e}')

    def get_links_category(self):
        try:
            logger.info('Extracting links from category')
            self.driver.get(self.url_base)
            category = self.driver.find_element(
                By.CLASS_NAME, 'ccc-hotzone'
            ).find_elements(By.XPATH, '//span/a')
            for cat in category:
                self.links_category.append(
                    cat.get_attribute('href').split('?')[0]
                )

        except Exception as e:
            logger.error(f'Error on get_links_category {e}')

    # def extract_category_from_url(self):
    #     try:
    #         for url in self.links_category:
    #             parts = url.split('/')
    #             if '-c-' in parts[-1]:
    #                 # Extract category from URL when '-c-' is present
    #                 category = parts[-1].split('-c-')[0]
    #                 logger.info(f"URL : {url}, Categoria : {category}")
    #             if '-sc-' in parts[-1]:
    #                 # Extract category from URL when '-sc-' is present
    #                 category = parts[-1].split('-sc-')[0]
    #                 logger.info(f"URL : {url}, Categoria : {category}")
    #             self.list_category.append(category)
    # except Exception as e:
    #         logger.error(f'Error on extract_category_from_url {e}')

    def extract_category_from_url(self):
        try:
            for url in self.links_category:
                parts = url.split('/')
                for part in parts:
                    if '-c-' in part or '-sc-' in part:
                        category = part.split('-')[0]
                        logger.info(f'URL : {url}, Categoria : {category}')
                        self.list_category.append(category)
                        break
        except Exception as e:
            logger.error(f'Error on extract_category_from_url {e}')

    def scrape_shein_clothes_info(self, url_clothes, type_clothes):
        self.driver.get(url_clothes)
        wait_for(5)
        disable_element_by_class(self.driver, 'j-optimize-category')
        count = 1

        while self.has_next_page():
            self.page_down_for_load_all_images()
            itens_in_page = self.driver.find_elements(
                'css selector', 'section[role="listitem"]'
            )
            logger.info(
                f'Extracting {count} page from category {type_clothes} '
            )
            count += 1
            for secao in itens_in_page:
                tag_a = secao.find_element('css selector', 'a')
                imgs_src = [
                    img.get_attribute('data-src')
                    for img in secao.find_elements(
                        'css selector', '.product-card__top-wrapper img'
                    )
                ]
                if len(imgs_src) == 0:
                    imgs_src = [
                        img.get_attribute('data-src')
                        for img in secao.find_elements(
                            'css selector', '.crop-image-container img'
                        )
                    ]
                imgs_serializada = json.dumps(imgs_src)
                new_product_data = {
                    'product_id': tag_a.get_attribute('data-id'),
                    'href': tag_a.get_attribute('href'),
                    'data_title': tag_a.get_attribute('data-title'),
                    'data_price': tag_a.get_attribute('data-price'),
                    'data_id_category': tag_a.get_attribute('data-cat_id'),
                    'data_sku': tag_a.get_attribute('data-sku'),
                    'data_spu': tag_a.get_attribute('data-spu'),
                    'data_us_price': tag_a.get_attribute('data-us-price'),
                    'data_us_origin_price': tag_a.get_attribute(
                        'data-us-origin-price'
                    ),
                    'discount': tag_a.get_attribute('data-discount'),
                    'image_src': imgs_serializada,
                    'product_type': type_clothes,
                }
                self.enviar_dados_para_kafka(new_product_data)
            try:
                next_page = self.driver.find_element(
                    By.CSS_SELECTOR,
                    '.sui-pagination__next.sui-pagination__btn',
                )
                next_page.click()
                wait_for(9)
            except ElementClickInterceptedException:
                logger.warning('warning on next_page')
                body = self.driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.END)
                wait_for(2)
                next_page = self.driver.find_element(
                    By.CSS_SELECTOR,
                    '.sui-pagination__next.sui-pagination__btn',
                )
                next_page.click()
            except Exception as e:
                logger.error(f'Error on next_page {e}')

    # def send_data_to_products_topic(self, dados_json):
    #     try:
    #         dados_json = json.dumps(dados_json)
    #         dados_bytes = dados_json.encode('utf-8')
    #         self.kafka_producer.produce(topic='produtos', value=dados_bytes)
    #         logger.info("Mensagem enviada com sucesso para o tópico 'produtos'.")
    #     except Exception as e:
    #         logger.error(f"Erro ao enviar mensagem para o Kafka: {e}")

    def enviar_dados_para_kafka(self, dados_json):
        try:
            dados_json = json.dumps(dados_json)
            self.kafka_producer.produce(topic='produtos', value=dados_json)
            print("Mensagem enviada com sucesso para o tópico 'produtos'.")
        except Exception as e:
            print(f'Erro ao enviar mensagem para o Kafka: {e}')


if __name__ == '__main__':

    # Cria uma instância do SheinCrawler
    shein_crawler = SheinCrawler()
    shein_crawler.run()
