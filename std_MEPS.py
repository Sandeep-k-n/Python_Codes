
import pandas as pd
import numpy as np
import selenium
from selenium import webdriver
import time
import datetime
from datetime import date, datetime
from selenium.webdriver.common.keys import Keys

#Install Driver
driver = webdriver.Chrome("Chromedriver")

# web address
url ="https://portal.mepsinternational.com/?logout=true"

# credentials
username = "ramesh.s@volvo.com"
password = "Classic123#"

class index_downloader:
   
    def __init__(self,url, username, password):
        self.url=url
        self.username = username
        self.password = password
    
    def scrape(self):
        driver.get(self.url)
        # find username/email field and send the username itself to the input field
        driver.find_element_by_id("Reg_Email").send_keys(self.username)
        # find password input field and insert password as well
        driver.find_element_by_id("Reg_Password").send_keys(self.password)
        # click login button
        driver.find_element_by_xpath("//*[@type='submit']").click()
        time.sleep(2)
        # click view subscriptions
        driver.find_element_by_xpath('//a[@href="/account/subscriptions/"]').click()

        # list_of_hrefs = []
        self.urls=[]
        content_blocks = driver.find_elements_by_class_name("table-primary__body")
        
        for block in content_blocks:
            elements = block.find_elements_by_tag_name("a")
            for el in elements:
                test = el.get_attribute("href")
                if (test != "https://portal.mepsinternational.com/account/single-licence/" ) and (test not in self.urls):
                    self.urls.append(el.get_attribute("href"))
        return self.urls
    
    # def filter_scenarioset(self):
    #     # Search data based on regular expression in the list
    #     self.scenarioset_links=[]
    #     [self.scenarioset_links.append('https://www.dnb.nl'+val) for val in self.urls
    #             if re.search(r'hbt-scenarioset-10k', val)]
    #     return self.scenarioset_links
    
    # def download_file(self, year, quarter):
    #     try:
    #         self.downloadlink=[]
    #         [self.downloadlink.append(val) for val in self.scenarioset_links
    #             if re.search(r'hbt-scenarioset-10k-{}q{}'.format(year,quarter),val)]
    #         filename='hbt-scenarioset-10k-{}q{}.xlsx'.format(year,quarter) 
    #         with requests.get(self.downloadlink[0]) as req:
    #             with open(filename, 'wb') as f:
    #                 for chunk in req.iter_content(chunk_size=8192):
    #                     if chunk:
    #                         f.write(chunk)
    #             return "/dbfs/mnt/fmi-import/DNB Scenariosets/"+filename
    #     except Exception as e:
    #         print(e)
    #         return None

#%% EXECUTE
download = index_downloader(url, username, password)
download.scrape()
# download.filter_scenarioset()
# download.download_file(2020,2)