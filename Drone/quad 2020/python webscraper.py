from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep
################################################################
target = "https://zehn.ramanapp.com/login/"

f1 =  "username"
f2 = "password"
subkey = "loginbtn"

f1val = "Mohsen_cactus"
f2val = "PAAAAASSSSSSWOORD"
################################################################
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(target)
sleep(5)
################################################################
while True:
    

    field1 = browser.find_element_by_id(f1)
    field2 = browser.find_element_by_id(f2)

    field1.send_keys(f1val)
    field2.send_keys(f2val)

    browser.find_element_by_id(subkey).click()
    sleep(1)
