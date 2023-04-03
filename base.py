from selenium import webdriver
from datetime import datetime


class BasePage:
    def __init__(self):
        # self.setup_method()
        # self.driver.implicitly_wait(10)
        # self.driver.set_window_size(1, 1)
        self.logerror_path = '.logs/error_log.txt'
        self.loginfo_path = '.logs/info_log.txt'
        
    def setup_method(self):
        self.driver = webdriver.Chrome()

    def temp_drive(self): 
        temp_driver = webdriver.Chrome()
        temp_driver.implicitly_wait(10)
        return temp_driver

    def teardown_method(self):
        self.driver.quit()

    def write_error_log(self, log_str):
        self.writelog(log_str, 'error')

    def write_info_log(self, log_str):
        self.writelog(log_str, 'info')

    def writelog(self, logstring, type):
        now = datetime.now()
        current_time = now.strftime("%d%m%y ,%H:%M:%S")
        log_path = self.loginfo_path
        if(type == 'error'):
            log_path = self.logerror_path

        with open(log_path, 'a', encoding='utf8') as f:
            f.write(current_time + '\t' + logstring+'\n')
        f.close()
