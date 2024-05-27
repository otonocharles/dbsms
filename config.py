import mysql.connector as conn
from mysql.connector import Error
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time
import json
from datetime import datetime

class Config:
    def  get_config(self):
       
        with open(os.path.join(".","myenv","config.json"),"r") as json_file:
            config = json.load(json_file)
        return config

    

class Db_Config(Config):
    
    def __init__(self):
    
       self.config = self.get_config()

    def get_connection(self):
        try:
            connection = conn.connect(
                        host = self.config["database"]["host"],
                        database = self.config["database"]["database"],
                        username = self.config["database"]["username"],
                        password = self.config["database"]["password"]
        )

            print(f"Successfully connected to the database: {self.config['database']['database']}")
            return connection

        except Error as e:
            print(f"Error connecting to database: {e}")
            return None
    

    def  get_config(self):
       
        return super().get_config()

class Message(Config):

    def __init__(self):
        
        self.config = self.get_config()
        self.service = Service(r'C:\chromedriver.exe')
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("headless")
        
        
        


    def send_message(self, datas):
        #initialize the browser
        self.browser = webdriver.Chrome(service=self.service,options=self.options)
       
        
        # loop through the dataframe as send each row
        for _, data in datas.iterrows():
            self.browser.get(self.config['Message']['url'])
            time.sleep(.3)
            self.browser.find_element(By.XPATH, "//input[@name ='userId']").send_keys(self.config['Message']['username'])
            time.sleep(.3)
            self.browser.find_element(By.XPATH, "//input[@name ='password']").send_keys(self.config['Message']['password'])
            time.sleep(.3)
            self.browser.find_element(By.XPATH, "//input[@name ='submit']").click()
            time.sleep(.3)

            self.browser.find_element(By.XPATH, "//input[@name ='sender']").send_keys(f'RCA@{datetime.now().time().strftime("%#I%p")}')
            time.sleep(.3)
            self.browser.find_element(By.NAME,'mtype').send_keys('Text Message')
            time.sleep(.3)
            self.browser.find_element(By.XPATH, "//input[@name ='userfile']").send_keys(
                    f"C:\\Users\\Noc\\Desktop\\RCA\\myenv\\TECHNICAL_STATE\\{data['TechRegion'].strip()}.txt")
            time.sleep(.3)
            self.browser.find_element(By.XPATH,"//textarea[@id = 'msg']").send_keys(
                        f"{data['TechRegion']}:\nSiteCount: {data['SiteCount']}\nSiteDown: {data['SiteDown']}\nNoTechRca2: {data['NoTechRca2']}\nNoEmcRca3: {data['NoEmcRca3']}\nlog into {self.config['Message']['portal']} to update.\nThanks.")
            time.sleep(.3)
            self.browser.find_element(By.XPATH, "//input[@name ='btn1']").click()
            time.sleep(.5)
        self.browser.quit()
        

    def get_config(self):
       
        return super().get_config()