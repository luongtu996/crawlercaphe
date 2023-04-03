from base import BasePage
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import re
import threading
import CrUtil


class BlogPage(BasePage):
    home_page = 'https://thoidaicoffee.vn/category/blog/'
    posts_page = 'https://thoidaicoffee.vn/category/blog/page/1/'

    # init method or constructor
    def __init__(self):
        super().__init__()

    def get_post_paginate(self):
        temp_driver = self.temp_drive()
        temp_driver.get(self.posts_page)
        links = [self.posts_page]
        pagination_ele = temp_driver.find_elements(
            By.CSS_SELECTOR, ".page-numbers li:not(:first-child) > a[href]")
        links += [elem.get_attribute('href') for elem in pagination_ele]
        return links

    def get_simple_post_paginate(self):
        links = []
        for i in range(1, 13):
            url = 'https://thoidaicoffee.vn/category/blog/page/' + str(i)
            links.append(url)
        return links

    def get_post_urls_in_one_page(self, url, post_urls, sem):
        temp_driver = self.temp_drive()
        temp_driver.get(url)
        elems = temp_driver.find_elements(
            By.CSS_SELECTOR, "h2.entry-title [href]")
        links = [elem.get_attribute('href') for elem in elems]
        post_urls += links
        sem.release()

    def get_all_post_urls(self, paginate_urls):
        post_urls = []
        sem = threading.Semaphore(5)  # limit to 5 concurrent threads
        threads = []
        for url in paginate_urls:
            sem.acquire()
            t = threading.Thread(
                target=self.get_post_urls_in_one_page, args=(url, post_urls, sem))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        return post_urls

    def get_post_detail(self, url):
        temp_driver = self.temp_drive()
        temp_driver.get(url)

        try:
            # get image
            image = ''
            try:
                image_ele = temp_driver.find_element(
                    By.CSS_SELECTOR, '.page-title-bg > .title-bg')
                if (image_ele):
                    background_image = image_ele.value_of_css_property(
                        'background-image')
                    url_match = re.search(r'url\("(.*?)"\)', background_image)
                    if url_match:
                        image = url_match.group(1)
            except:
                self.write_error_log('Loi image: ' + url)

            # get title
            title = ''
            try:
                title_ele = temp_driver.find_element(
                    By.CSS_SELECTOR, 'h1.entry-title')
                if (title_ele):
                    title = title_ele.get_attribute('innerHTML')
            except:
                self.write_error_log('Loi title: ' + url)

            # get content
            content = ''
            try:
                content_ele = temp_driver.find_element(
                    By.CSS_SELECTOR, '.entry-content.single-page')
                if (content_ele):
                    temp_driver.execute_script(
                        "document.querySelector('.entry-content.single-page .blog-share.text-center').remove();")
                    # content = content_ele.get_attribute('outerHTML')
                    content = content_ele.get_attribute('innerHTML')
                    content = CrUtil.simplify_image(content)
                    content = CrUtil.clean_enter(content)
                    content = CrUtil.clean_tab(content)
            except:
                self.write_error_log('Loi content: ' + url)

            # get posted_in
            posted_in = []
            try:
                posted_in_ele = temp_driver.find_elements(
                    By.CSS_SELECTOR, '.entry-meta [href]')
                posted_in = [elem.text for elem in posted_in_ele]
            except:
                self.write_error_log('Loi posted_in: ' + url)

            item_info = {
                "title": title,
                "image": image,
                "content": content,
                "posted_in": posted_in,
            }

            return item_info
        except Exception as e:
            self.write_error_log('Loi: ' + url)
            print(e)
            return {}

    # Luu lai log quet va ca loi exception
