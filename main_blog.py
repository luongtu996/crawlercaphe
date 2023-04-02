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

    def save_post_paginate(self):
        file_name = 'dumpfile/blog_paginate_urls.json'
        urls = self.blog.get_simple_post_paginate()
        CrUtil.save_json_data(file_name, urls)

    def save_post_urls(self):
        file_name = 'dumpfile/blog_paginate_urls.json'
        paginate_urls = CrUtil.load_json_data(file_name)
        post_urls = self.blog.get_all_post_urls(paginate_urls)
        file_name_posts = 'dumpfile/blog_post_urls.json'
        CrUtil.save_json_data(file_name_posts, post_urls)

    def save_posts_json(self):
        # create a semaphore with a limit of 5
        sem = threading.Semaphore(5)

        # get from file
        file_name = 'dumpfile/blog_post_urls.json'
        post_urls = []
        if (CrUtil.check_file_exists(file_name)):
            post_urls = CrUtil.load_json_data(file_name)

        # define a helper function to retrieve the details of a single blog post
        def retrieve_post(url):
            # acquire the semaphore
            with sem:
                post = self.blog.get_post_detail(url)
                return post

        # create a thread for each URL and retrieve the details of the blog post in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_post = {executor.submit(
                retrieve_post, url): url for url in post_urls}
            posts = [future.result()
                     for future in concurrent.futures.as_completed(future_to_post)]

        # write product to file
        posts_file_name = 'dumpfile/posts.json'
        CrUtil.save_json_data(posts_file_name, posts)


main = MainBlog()
# main.save_post_paginate()
# main.save_post_urls()
main.save_posts_json()
