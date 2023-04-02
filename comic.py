from lib2to3.pgen2 import driver
import os
from pickle import FALSE
from tempfile import tempdir
from bs4 import BeautifulSoup
import json
from datetime import datetime
import cloudscraper
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import threading
import subprocess

options = webdriver.ChromeOptions()
options.add_argument("--window-size=1,1")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomation Extension', False)


home_path = './src/models/comiccrawler'
os.chdir(home_path)
chromedrive_path = r'C:\\chromedriver_win32\\chromedriver.exe'


class NettruyenComic:
    def __init__(self):
        # self.driver = webdriver.Chrome (options=options, executable_path=chromedrive_path)

        self.homepage = 'http://www.nettruyenmoi.com/'
        self.root_path = './src/comiccrawler/dest'
        self.logerror_path = './error_log.txt'
        self.datajson_path = './nettruyengo.json'
        self.MAX_PAGE = 554
        self.dumpfolder = './dumpcomic/'
        self.downloadfolder = './downloadcomic'
        self.scraper = cloudscraper.create_scraper()
        self.comics = []
        self.num_comics = 0
        # comic info folder
        if os. path.isdir(self.dumpfolder) == False:
            os.mkdir(self.dumpfolder)
        else:
            # TODO: lấy thông tin comic trong thư mục dump:
            comics = os.listdir(self.dumpfolder)
            for comic in comics:
                # read json file
                with open(self.dumpfolder + "/" + comic) as f:
                    self.comics.append(json.load(f))
            self.num_comics = len(self.comics)

        # comic download image folder
        if os.path.isdir(self.downloadfolder) == False:
            os.mkdir(self.downloadfolder)

    # lấy thông tin tất cả comic trong 1 page
    def get_comics_info_in_page(self, index):
        address_sub = self.homepage+"tim-truyen?page={page_index}"

        if index == 1:
            address = self.homepage+"tim-truyen"
        else:
            address = address_sub.format(page_index=index)

        items = []
        try:
            temp_driver = webdriver.Chrome(
                options=options, executable_path=chromedrive_path)
            temp_driver.get(address)
            time.sleep(3)
            main_content = temp_driver.execute_script(
                "return document.body.querySelector('main')")
            page = BeautifulSoup(main_content.get_attribute('innerHTML'))
        except Exception as e:
            self.writelog("Network Unavailable - " + address)
            time.sleep(300)
            print(e)
            return []
        try:
            items_content = page.find('div', {"class": "items"}).find_all(
                'div', {"class": "item"})
            for item in items_content:
                try:
                    item_info = {
                        "link": item.find('div', {"class": "image"}).find('a').attrs['href'],
                        "image": item.find('div', {"class": "image"}).find("img").attrs['data-original'],
                        "title": item.find('div', {"class": "title"}).text.strip(),
                        "message_main": {
                            "genres": item.find('div', {"class": "message_main"}).findAll('p')[0].text.split(":")[1],
                            "status": item.find('div', {"class": "message_main"}).findAll('p')[1].text.split(":")[1],
                            "view": item.find('div', {"class": "message_main"}).findAll('p')[2].text.split(":")[1],
                            "comment": item.find('div', {"class": "message_main"}).findAll('p')[3].text.split(":")[1],
                            "subscriber": item.find('div', {"class": "message_main"}).findAll('p')[4].text.split(":")[1],
                            "update_time": item.find('div', {"class": "message_main"}).findAll('p')[5].text.split(":")[1],
                        },
                        "description": item.find('div', {"class": "box_text"}).text.strip()
                    }
                    item_info["detail"] = self.get_comic_info(
                        item_info["link"])

                    if item_info["detail"] == {}:
                        self.writelog(address)
                        continue

                    # dump data here
                    dumpfilename = "".join(x for x in item_info['title'] if (
                        x.isalnum() or x == '_' or x == ' '))
                    json_object = json.dumps(item_info, indent=4)

                    # Writing to sample.json
                    if os.path.isfile(self.dumpfolder + '/' + dumpfilename) == False:
                        with open(self.dumpfolder + '/' + dumpfilename, "w") as outfile:
                            outfile.write(json_object)

                    items.append(item_info)
                    time.sleep(1)
                except Exception as e:
                    self.writelog("Network Unavailable - " + address)
                    time.sleep(300)
                    print(e)
                    continue
        except Exception as e:
            self.writelog(address)
            temp_driver.close()
            print(e)

        try:
            temp_driver.close()
        except:
            return items
        return items


    # lầy thông tin tất cả comic
    # lấy danh sách comics

    def get_list_comics(self):
        start_index = 378
        max_index = self.MAX_PAGE
        for index in range(start_index, max_index+1):
            self.get_comics_info_in_page(index)  # 1 page
        print("ScanDone!")

    # lấy thông tin comic
    def get_comic_info(self, address):
        print("Address: ", address)
        temp_driver = webdriver.Chrome(
            options=options, executable_path=chromedrive_path)
        try:
            temp_driver.get(address)
            time.sleep(1)
            main_content = temp_driver.execute_script(
                "return document.body.querySelector('main').querySelectorAll('div.container')[1]")
            page = BeautifulSoup(main_content.get_attribute('innerHTML'))
        except:
            self.writelog("Network Unavailable" + address)
            time.sleep(300)
            temp_driver.close()
            return {}
        try:
            detail = {
                "title": page.find('h1').text.strip(),
                "image": page.find('div', {"class": "col-image"}).find("img").attrs['src'],
                "author": page.find('li', {"class": "author row"}).findAll('p')[1].text.strip(),
                "status": page.find('li', {"class": "status row"}).findAll('p')[1].text.strip(),
                "genres": [x.text for x in page.find('li', {"class": "kind row"}).findAll('a')],
            }

            episode_list = page.find(
                'div', {"class": "list-chapter"}).findAll('li')[1:]
            episode_links = []
            for episode in episode_list:
                episode_links.append({
                    "name": episode.find('a').text.strip(),
                    "link": episode.find('a').attrs['href']
                })

            detail["episodes"] = episode_links
        except Exception as e:
            self.writelog(address)
            temp_driver.close()
            return {}

        temp_driver.close()
        return detail

# download ảnh
    def download_image(self, namefile, url, folder, logfolder):
        fixed_name = folder+"/" + \
            ("".join(x for x in namefile if (x.isalnum() or x == '_' or x == ''))).strip()
        with open(fixed_name + '.jpg', 'wb') as handle:
            try:
                response = self.scraper.get(
                    url, headers={'referer': self.homepage})
                if not response.ok:
                    pass

                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)
                handle.close()
            except Exception as e:
                self.writelogdownloadcomic(logfolder, fixed_name)
                handle.close()

#  download 1 tập: 1 tập chứa nhiều file ảnh, cần duyệt lấy link các ảnh, thông tin các ảnh
    def download_episode(self, address, dest_folder, log_folder):
        temp_driver = webdriver.Chrome(
            options=options, executable_path=chromedrive_path)
        try:
            temp_driver.get(address)
            time.sleep(1)
            main_content = temp_driver.execute_script(
                "return document.body.querySelector('main').querySelectorAll( 'div.container')[1]")
            page = BeautifulSoup(main_content.get_attribute('innerHTML'))
        except Exception as e:
            self.writelogdownloadcomic(log_folder, address)
            time.sleep(1)
            temp_driver.close()
            return {}

        image_list = page.find('div', {
                               "class": "reading-detail box_doc"}).findAll('div', {"class": "page-chapter"})
        images = []
        for image in image_list:
            item = {
                "alt": image.find('img').attrs['alt'],
                "data-original": image.find('img').attrs['data-original'],
                "src": image.find('img').attrs['src'],
                "data-index": image.find('img').attrs['data-index'],
            }
            images .append(item)

            # download to folder:
            if "http" in item['src'][:5]:
                self.download_image(
                    item['alt'], item['src'], dest_folder, log_folder)
            else:
                self.download_image(
                    item['alt'], "http: "+item['src'], dest_folder, log_folder)

        return images

    # Download 1 comic gồm nhiều tập, load từ thư mục dump comic để lấy thông tin link đến các tập
    def download_comic(self, comic):
        # make folder
        episodes = comic['detail']['episodes']
        comic_folder = self.downloadfolder + '/' + \
            ("".join(x for x in comic['title'] if (
                x.isalnum() or x == '_' or x == ''))).strip()
        if not os.path.isdir(comic_folder):
            os.mkdir(comic_folder)
        else:  # Nếu tồn tại thư mục, tồn tại comic rồi thì thôi
            print("-----Tồn tại thư mục này r!----")
            print("-------------------------------")
            return

        for episode in episodes:
            episode_folder = comic_folder + '/' + \
                ("".join(x for x in episode['name'] if (
                    x.isalnum() or x == '_' or x == ''))).strip()
            if not os.path.isdir(episode_folder):
                os.mkdir(episode_folder)
            try:
                self.download_episode(
                    episode['link'], episode_folder, comic_folder)
            except Exception as e:
                self.writelogdownloadcomic(comic_folder, episode['name'])

    def download_comics_1thread(self):
        if self.num_comics > 0:
            for comic in self.comics:
                self.download_comic(comic)
            print("Download comics done!")

    def download_comics_multithread(self):
        scanned_comics = os.listdir(self.downloadfolder)
        pointer = 1000
        threads = []
        MAX_THREADS = 5

        if self.num_comics > 8:
            threads = []
            MAX_THREADS = 5
            pointer = 6000

        while True:
            if pointer >= self.num_comics:
                break
            while len(threads) < MAX_THREADS:
                comic_folder = ("".join(x for x in self.comics[pointer]['title'] if (
                    x.isalnum() or x == '_' or x == ''))).strip()
                if comic_folder not in scanned_comics:
                    thread = threading.Thread(
                        target=self.download_comic, args=(self.comics[pointer],))
                    thread.start()
                    threads.append(thread)
                pointer += 1
                if pointer >= self.num_comics:
                    break
            threads = [t for t in threads if t.is_alive()]
            if pointer >= self.num_comics:
                for thread in threads:
                    thread.join(timeout=5*60)
                    threads = [t for t in threads if t.is_alive()]
                break

    # Luu lai log quet va ca loi exception
    def writelog(self, logstring):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        with open(self.logerror_path, 'a', encoding='utf8') as f:
            f.write(current_time + '\t' + logstring+'\n')
        f.close()

    def writelogdownloadcomic(self, path, content):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        filelog = path + "/exception.txt"
        with open(filelog, 'a', encoding='utf8') as f:
            f.write(current_time + '\t' + content + '\n')
        f.close()

# Kiểm tra số lượng episode, số lượng trang trên mỗi tập xem đủ chưa, nếu chưa download tiếp
    def verifycomic(self):
        pass


crawler = NettruyenComic()
# crawler.get_list_comics ()
# crawler.download_comics()
crawler.download_comics_multithread()
