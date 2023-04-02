from base import BasePage
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from threading import Semaphore, Thread


class ProductPage(BasePage):
    home_page = 'https://thoidaicoffee.vn'
    collection_page = 'https://thoidaicoffee.vn/collections/ban-dong-lanh'

    # init method or constructor
    def __init__(self):
        super().__init__()

    def test(self):
        url = "https://thoidaicoffee.vn/products/ca-phe-hat-chat-luong-cao/"
        temp_driver = self.temp_drive()
        temp_driver.get(url)
        # get short desc
        short_desc = ''
        try:
            short_desc_ele = temp_driver.find_element(
                By.CSS_SELECTOR, '.product-short-description')
            if (short_desc_ele):
                short_desc = short_desc_ele.get_attribute('innerHTML')

        except Exception as e:
            print('loi roi')

    def get_collections_url(self):
        temp_driver = self.temp_drive()
        temp_driver.get(self.collection_page)
        elems = temp_driver.find_elements(
            By.CSS_SELECTOR, "#woocommerce_product_categories-13 > ul > li.cat-item > [href]")
        links = [elem.get_attribute('href') for elem in elems]

        return links

    # get all paginate of collection
    def get_all_collection_urls(self, collection_urls):
        # create a semaphore object with a limit of 5 threads
        sema = Semaphore(5)
        links = []

        # define a function that will be used as a target for each thread
        def process_url(url):
            # acquire the semaphore before executing any thread
            sema.acquire()
            try:
                result = self.get_paginate_collection(url)
                # append the result to the links list
                links.extend(result)
            finally:
                # release the semaphore after the thread finishes executing
                sema.release()

        # create a thread for each URL and start it
        threads = [Thread(target=process_url, args=(url,))
                   for url in collection_urls]
        for thread in threads:
            thread.start()

        # wait for all threads to finish
        for thread in threads:
            thread.join()

        # return the final links list
        return links

    def get_paginate_collection(self, url):
        temp_driver = self.temp_drive()
        temp_driver.get(url)

        results = [url]
        try:
            pagination_ele = temp_driver.find_elements(
                By.CSS_SELECTOR, ".page-numbers > li > a.page-number:not(.next)[href]")
            links = [elem.get_attribute('href') for elem in pagination_ele]
        except:
            links = []

        results += links
        return results
        # page-numbers

    def get_all_product_urls(self, collection_urls):
        product_urls = []
        semaphore = Semaphore(5)  # limit the number of threads to 5

        def worker(url):
            # acquire a permit from the semaphore
            semaphore.acquire()
            try:
                result = self.get_product_urls_in_one_collection(url)
                # append the result to the links list
                product_urls.extend(result)
            finally:
                # release the permit when done
                semaphore.release()

        # start a worker thread for each URL in the collection_urls list
        threads = []
        for url in collection_urls:
            t = Thread(target=worker, args=(url,))
            t.start()
            threads.append(t)

        # wait for all threads to finish before returning the results
        for t in threads:
            t.join()

        return product_urls

    def get_product_urls_in_one_collection(self, url):
        temp_driver = self.temp_drive()
        temp_driver.get(url)
        links = []
        try:
            elems = temp_driver.find_elements(
                By.CSS_SELECTOR, "#main div.product-small.box .woocommerce-loop-product__title [href]")
            links = [elem.get_attribute('href') for elem in elems]
        except:
            self.writelog('khong co sp nao trong collecion: ' + url)

        return links

    def get_product_detail(self, url):
        temp_driver = self.temp_drive()
        temp_driver.get(url)
        try:
            # get breadcum
            breadcum = ''
            try:
                breadcum_ele = temp_driver.find_elements(
                    By.CSS_SELECTOR, '.woocommerce-breadcrumb.breadcrumbs [href]:not(:first-child)')
                breadcum = [elem.text for elem in breadcum_ele]
            except:
                self.writelog('Loi breadcum: ' + url)

            # get title
            title = ''
            try:
                title_ele = temp_driver.find_element(
                    By.CSS_SELECTOR, 'h1.product-title.product_title.entry-title')
                if (title_ele):
                    title = title_ele.get_attribute('innerHTML')
            except:
                self.writelog('Loi title: ' + url)

            # get short desc
            short_desc = ''
            try:
                short_desc_ele = temp_driver.find_element(
                    By.CSS_SELECTOR, '.product-short-description')
                if (short_desc_ele):
                    short_desc = short_desc_ele.get_attribute('innerHTML')
            except:
                self.writelog('Loi short_desc: ' + url)

            # get content
            content = ''
            try:
                content_ele = temp_driver.find_element(
                    By.CSS_SELECTOR, '.woocommerce-Tabs-panel--description')
                if (content_ele):
                    content = content_ele.get_attribute('innerHTML')
            except:
                self.writelog('Loi content: ' + url)

            # get images
            images = []
            try:
                images_ele = temp_driver.find_elements(
                    By.CSS_SELECTOR, '.product-images .product-gallery-slider .woocommerce-product-gallery__image [href]')
                if (images_ele):
                    images = [elem.get_attribute('href')
                              for elem in images_ele]
            except:
                self.writelog('Loi images: ' + url)

            # get posted_in
            posted_in = []
            try:
                posted_in_ele = temp_driver.find_elements(
                    By.CSS_SELECTOR, '.product_meta .posted_in [href]')
                posted_in = [elem.text for elem in posted_in_ele]
            except:
                self.writelog('Loi posted_in: ' + url)

            # get tagged_as
            tagged_as = []
            try:
                tagged_as_ele = temp_driver.find_elements(
                    By.CSS_SELECTOR, '.product_meta .tagged_as [href]')
                tagged_as = [elem.text for elem in tagged_as_ele]
            except:
                self.writelog('Loi tagged_as: ' + url)

            # get prices
            has_price = True
            price = 0
            sale_price = 0
            try:
                prices_ele = temp_driver.find_elements(
                    By.CSS_SELECTOR, '.product-page-price .woocommerce-Price-amount bdi')

                price_list = [elem.text for elem in prices_ele]

                if (len(price_list) == 1):
                    price = price_list[0]
                elif (len(price_list) > 1):
                    price = price_list[0],
                    sale_price = price_list[1]
            except Exception as e:
                has_price = False
                self.writelog('Loi price: ' + url)
                print(e)

            item_info = {
                "breadcum": breadcum,
                "title": title,
                "short_desc": short_desc,
                "content": content,
                "images": images,
                "posted_in": posted_in,
                "tagged_as": tagged_as,
                "has_price": has_price,
                "price": price,
                "sale_price": sale_price,
            }

            return item_info
        except Exception as e:
            self.writelog('Loi: ' + url)
            print(e)
            return {}

    def get_categories(self):
        temp_driver = self.temp_drive()
        temp_driver.get(self.home_page)

        cates = []

        elems = temp_driver.find_elements(
            By.CSS_SELECTOR, "#menu-danh-muc-san-pham .menu-item-object-product_cat")
        for el in elems:
            # get menu
            cate_ele = el.find_element(By.CSS_SELECTOR, 'a[href]')
            cate_name = cate_ele.get_attribute('innerHTML')
            cate = {
                "name": cate_name,
                "has_child": False,
                "child": []
            }

            # check if has sub_menu
            if ('menu-item-has-children' in el.get_attribute('class')):
                sub_menu_el = el.find_elements(
                    By.CSS_SELECTOR, ".sub-menu .menu-item-object-product_cat [href]")
                sub_menu = [elem.get_attribute('innerHTML') for elem in sub_menu_el]
                cate['has_child'] = True
                cate['child'] = sub_menu
            
            cates.append(cate)

        return cates

            
                