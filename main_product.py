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
        if(CrUtil.check_file_exists(file_name)):
            collection_urls = CrUtil.load_json_data(file_name)
        results = self.product.get_all_collection_urls(collection_urls)
        file_name_save = 'dumpfile/all_collection_urls.json'
        CrUtil.save_json_data(file_name_save, results)

    def save_all_products_url(self):
        #get collection urls
        file_name = 'dumpfile/all_collection_urls.json'
        collection_urls=[]
        if(CrUtil.check_file_exists(file_name)):
            collection_urls = CrUtil.load_json_data(file_name)
        product_urls = self.product.get_all_product_urls(collection_urls)
        file_name_save = 'dumpfile/all_product_urls.json'
        CrUtil.save_json_data(file_name_save, product_urls)

    def save_products(self):
        file_name = 'dumpfile/all_product_urls.json'
        products = []
        product_urls = []
        semaphore = Semaphore(5)  # limit the number of threads to 5

        if(CrUtil.check_file_exists(file_name)):
            product_urls = CrUtil.load_json_data(file_name)

        def worker(url):
            # acquire a permit from the semaphore
            semaphore.acquire()
            try:
                result = self.product.get_product_detail(url)
                # append the result to the links list
                products.append(result)
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
        product_file_name = 'dumpfile/all_products.json'
        CrUtil.save_json_data(product_file_name, products)
        print('get_products success')

    def save_categories(self):
        file_name = 'dumpfile/all_categories.json'
        categories = self.product.get_categories()
        CrUtil.save_json_data(file_name, categories)

    def save_product_tags(self):
       file_name = 'dumpfile/all_product_tags.json'
       tags = self.product.get_product_tags()
       CrUtil.save_json_data(file_name, tags)

main = MainProduct()
# main.save_collection_urls()
# main.save_all_collection_urls()
# main.save_all_products_url()
# main.get_products()

# main.save_categories()
main.save_product_tags()
