from selenium import webdriver
from datetime import datetime


class BasePage:
    def __init__(self):
        # self.setup_method()
        # self.driver.implicitly_wait(10)
        # self.driver.set_window_size(1, 1)
        self.logerror_path = './error_log.txt'
        
    def setup_method(self):
        self.driver = webdriver.Chrome()

    def temp_drive(self): 
        temp_driver = webdriver.Chrome()
        temp_driver.implicitly_wait(10)
        return temp_driver

    def teardown_method(self):
        self.driver.quit()

    def writelog(self, logstring):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        with open(self.logerror_path, 'a', encoding='utf8') as f:
            f.write(current_time + '\t' + logstring+'\n')
        f.close()
