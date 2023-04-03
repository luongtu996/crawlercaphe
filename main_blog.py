import CrUtil
import threading
import concurrent.futures

from blog import BlogPage


class MainBlog:

    def __init__(self):
        self.dumpfolder = './dumpfile/'
        self.downloadfolder = './download'
        self.blog = BlogPage()
        CrUtil.mkdir(self.dumpfolder)
        CrUtil.mkdir(self.downloadfolder)

        self.collections = []
        self.num_collections = 0

    # lấy tất cả link paginate của post
    def save_post_paginate(self):
        file_name = 'dumpfile/blog_paginate_urls.json'
        urls = self.blog.get_simple_post_paginate()
        CrUtil.save_json_data(file_name, urls)

    # lưu tất cả link chi tiết bài viết
    def save_post_urls(self):
        file_name = 'dumpfile/blog_paginate_urls.json'
        paginate_urls = CrUtil.load_json_data(file_name)
        post_urls = self.blog.get_all_post_urls(paginate_urls)
        file_name_posts = 'dumpfile/blog_post_urls.json'
        CrUtil.save_json_data(file_name_posts, post_urls)

    # lưu tất bài viết
    def save_posts(self):
        # create a semaphore with a limit of 5
        semaphore = threading.Semaphore(5)
        posts = []

        # get from file
        file_name = 'dumpfile/blog_post_urls.json'
        post_urls = []
        if (CrUtil.check_file_exists(file_name)):
            post_urls = CrUtil.load_json_data(file_name)

        def worker(url):
            # acquire a permit from the semaphore
            semaphore.acquire()
            try:
                result = self.blog.get_post_detail(url)
                # append the result to the links list
                posts.append(result)
            finally:
                # release the permit when done
                semaphore.release()

        # start a worker thread for each URL in the post_urls list
        threads = []
        for url in post_urls:
            t = threading.Thread(target=worker, args=(url,))
            t.start()
            threads.append(t)

        # wait for all threads to finish before returning the results
        for t in threads:
            t.join()

        # write product to file
        posts_file_name = 'dumpfile/posts.json'
        CrUtil.save_json_data(posts_file_name, posts)


main = MainBlog()
# main.save_post_paginate()
# main.save_post_urls()
main.save_posts()
