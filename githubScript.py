from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
import sys
import requests
import json
import serial
import time
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import threading
from selenium.webdriver.common.keys import Keys
import pygame

pygame.mixer.init()
pygame.mixer.music.load("/home/pi/Downloads/juice.mp3")
pygame.mixer.music.play()


array = []
disp = Display(visible=0, size=(1920,1080)).start()

#import nexmo

email = "avivkalmanson@gmail.com"
password = "Avivkalman1"
customerName="Aviv"

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--start-maximized')

def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"

  return cpuserial

def addToCart(driver):
    if (array[0].startswith('72900000')):
        driver.get("https://www.shufersal.co.il/online/he/search?text=" + array[0][8:])
    elif (array[0].startswith('7290000')):
        driver.get("https://www.shufersal.co.il/online/he/search?text=" + array[0][7:])
    elif (array[0].startswith('729000')):
        driver.get("https://www.shufersal.co.il/online/he/search?text=" + array[0][6:])
    else:
        try:
            driver.get("https://www.shufersal.co.il/online/he/search?text=" + array[0])
            try1 = driver.find_element(By.XPATH, '//*[@id="mainProductGrid"]/li[1]/div[1]/div[4]/button[1]')
        except:
            print('another')
            try:
                try2 = driver.find_element(By.XPATH, '//*[@id="mainProductGrid"]/li[1]/div[1]/div[5]/button[1]')
            except:
                driver.get("https://www.shufersal.co.il/online/he/search?text=" + array[0][1:])

    # add to cart / +1
    try:
        elem5 = driver.find_element(By.XPATH, '//*[@id="mainProductGrid"]/li[1]/div[1]/div[4]/button[1]')
        elem5.click()
    except:
        print('another try')
        try:
            elem99 = driver.find_element(By.XPATH, '//*[@id="mainProductGrid"]/li[1]/div[1]/div[5]/button[1]')
            elem99.click()
        except:
            print('hi')
            try:
                elem6 = driver.find_element(By.XPATH,'//*[@id="mainProductGrid"]/li[1]/div[1]/div[4]/div[3]/div[1]/span[1]/button')
                elem6.click()
                elem7 = driver.find_element(By.XPATH, '//*[@id="mainProductGrid"]/li[1]/div[1]/div[4]/button[2]')
                elem7.click()
            except:
                print('last')
                try:
                    elem6 = driver.find_element(By.XPATH,'//*[@id="mainProductGrid"]/li[1]/div[1]/div[5]/div[3]/div[1]/span[1]/button')
                    elem6.click()
                    elem7 = driver.find_element(By.XPATH, '//*[@id="mainProductGrid"]/li[1]/div[1]/div[5]/button[2]')
                    elem7.click()
                except:
                    print('failed')


def logIn(driver):
    loginEmail = driver.find_element_by_id('j_username')
    loginEmail.send_keys(email)
    loginPassword = driver.find_element_by_id('j_password')
    loginPassword.send_keys(password)
    submit = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[3]/button')
    submit.click()

def priceCheck(driver):
    elem8 = driver.find_element(By.XPATH, '//*[@id="cartContainer"]/div/div/footer/div[2]/div/div/div[1]/span')
    price = elem8.text
    elem20 = driver.find_element(By.XPATH, '//*[@id="cartTotalItems"]')
    quantity = elem20.text
    print(''.join(map(str,re.findall("\d+", price)))[0:-2] + "₪")
    if ((len(re.findall("\d+", price))> 1 or int(re.findall("\d+", price)[0])>250) and int(quantity)>5):
        print("order! price is " + ''.join(map(str,re.findall("\d+", price)))[0:-2] + "₪")

def whole():
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1920, 1080)
    driver.get("https://www.shufersal.co.il/online/he/login")
    logIn(driver)
    while True:
        if len(array)>0:
            # driver = webdriver.Chrome()
            addToCart(driver)
            time.sleep(5)
            priceCheck(driver)
            array.pop(0)
        time.sleep(1)


def ask():
    barcode = input('enter barcode')
    print('your barcode is' + barcode)
    array.append(barcode)
    print(array)
    ask()

def addToCartRami(driver):
    try:
        try312 = driver.find_element(By.XPATH, '//*[@id="destination"]')
        try312.send_keys(array[0])
        try312.send_keys(Keys.ENTER)
        time.sleep(3)
        hover = ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '//*[@id="product-' + array[0] + '"]'))
        hover.perform()
    except:
        print('failed')
   
    print('proceed')
    try:
        try313 = driver.find_element(By.XPATH, '//*[@id="product-'+array[0]+'"]/div/div[1]/div[3]/div/div/div/div/button')
        try313.click()
    except:
        print('proceed')
        try:
          try3155 = driver.find_element(By.XPATH, '//*[@id="product-'+array[0]+'"]/div[2]/div[1]/div[4]/div/div/div/div/button')
          try3155.click()
        except:
          print('failed')


def logInRami(driver):
    elem81 = driver.find_element(By.XPATH, '//*[@id="cart"]/div/div/div[1]/div/div/div/div[1]/div/div/div/span[2]/div/button[1]')
    elem81.click()
    time.sleep(1)
    loginEmail = driver.find_element_by_id('email')
    loginEmail.send_keys(email)
    loginPassword = driver.find_element_by_id('password')
    loginPassword.send_keys(password)
    submit = driver.find_element_by_class_name('login-btn')
    submit.click()

def priceCheckRami(driver):
    elem8 = driver.find_element(By.XPATH, '//*[@id="cart"]/div/div/div[2]/div[2]/div[2]/div/div/span/span')
    price = elem8.text
    print(price)

def wholeRami():
    while True:
        if len(array) > 0:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_window_size(1920, 1080)
            driver.get("https://www.rami-levy.co.il/he/shop")
            logInRami(driver)
            time.sleep(5)
            # driver = webdriver.Chrome()
            addToCartRami(driver)
            time.sleep(1)
            priceCheckRami(driver)
            time.sleep(1)
            array.pop(0)
            driver.quit()
        time.sleep(1)
        
if __name__ == '__main__':
    print('holy cow')
    print(getserial())
    thread1 = threading.Thread(target=ask).start()
    thread2 = threading.Thread(target=whole).start()


# 
# filled = False
# while not filled:
#     try:
#         loginPassword2 = driver.find_element_by_id('j_password')
#         loginPassword2.send_keys(password)
#         filled = True
#     except:
#         filled = False
# 
# print(filled)


# SEND MESSAGES TO CLIENT WHEN ORDER IS READY
# client = nexmo.Client('9e1e8401', 'SMhVNa22gcIHp3gt')
#
# client.send_message({
#     'from': 'Aviv\'s app',
#     'to': '972546448801',
#     'text': 'Your order is ready! Please open the following link: https://www.shufersal.co.il/online/he/A (:',
# })
