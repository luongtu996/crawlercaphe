from product import ProductPage
import json
import os
import CrUtil
from threading import Semaphore, Thread


class MainProduct:

    def __init__(self):
        self.dumpfolder = './dumpfile/'
        self.downloadfolder = './download'
        self.product = ProductPage()
        CrUtil.mkdir(self.dumpfolder)
        CrUtil.mkdir(self.downloadfolder)

        self.collections = []
        self.num_collections = 0

    def save_collection_urls(self):
        collection_urls = self.product.get_collections_url()
        file_name = 'dumpfile/collection_url.json'
        CrUtil.save_json_data(file_name, collection_urls)

    def save_all_collection_urls(self):
        file_name = 'dumpfile/collection_url.json'
        collection_urls = []
        if (CrUtil.check_file_exists(file_name)):
            collection_urls = CrUtil.load_json_data(file_name)
        results = self.product.get_all_collection_urls(collection_urls)
        file_name_save = 'dumpfile/all_collection_urls.json'
        CrUtil.save_json_data(file_name_save, results)

    def save_all_products_url(self):
        # get collection urls
        file_name = 'dumpfile/all_collection_urls.json'
        collection_urls = []
        if (CrUtil.check_file_exists(file_name)):
            collection_urls = CrUtil.load_json_data(file_name)
        product_urls = self.product.get_all_product_urls(collection_urls)
        file_name_save = 'dumpfile/all_product_urls.json'
        CrUtil.save_json_data(file_name_save, product_urls)

    def save_products(self):
        file_name = 'dumpfile/all_product_urls.json'
        product_file_name = 'dumpfile/all_products.json'
        products = []
        product_urls = []
        semaphore = Semaphore(5)  # limit the number of threads to 5

        if (CrUtil.check_file_exists(file_name)):
            product_urls = CrUtil.load_json_data(file_name)

        def worker(url):
            # acquire a permit from the semaphore
            semaphore.acquire()
            try:
                result = self.product.get_product_detail(url)
                # append the result to the links list
                products.append(result)

                if (len(products) % 10 == 0):
                    CrUtil.save_json_data(product_file_name, products)
            finally:
                # release the permit when done
                semaphore.release()

        # start a worker thread for each URL in the collection_urls list
        threads = []
        for url in product_urls:
            t = Thread(target=worker, args=(url,))
            t.start()
            threads.append(t)

        # wait for all threads to finish before returning the results
        for t in threads:
            t.join()

        # write product to file

        CrUtil.save_json_data(product_file_name, products)
        print('get_products success')

    def save_categories(self):
        file_name = 'dumpfile/all_categories.json'
        categories = self.product.get_categories()
        CrUtil.save_json_data(file_name, categories)

    def save_brands_image(self):
        file_name = 'dumpfile/all_brands_image.json'
        brands = self.product.get_brands_image()
        CrUtil.save_json_data(file_name, brands)

    def save_products_tags(self):
        file_name = 'dumpfile/all_products.json'
        file_name_save = 'dumpfile/all_products_tags.json'
        products = CrUtil.load_json_data(file_name)
        products_tags = CrUtil.get_unique_tagged_as(products)
        CrUtil.save_json_data(file_name_save, products_tags)

    def save_products_collectionss(self):
        file_name = 'dumpfile/all_products.json'
        file_name_save = 'dumpfile/all_products_collections.json'
        products = CrUtil.load_json_data(file_name)
        products_collections = CrUtil.get_unique_posted_in(products)
        CrUtil.save_json_data(file_name_save, products_collections)

main = MainProduct()
# main.save_collection_urls()
# main.save_all_collection_urls()
# main.save_all_products_url()
# main.save_products()
# main.save_brands_image()

main.save_categories()
# main.save_products_tags()
# main.save_products_collectionss()
