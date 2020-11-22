import requests
import time
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import socket
from wifi import Cell, Scheme
import pygame
import re


def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(ex)
        return False
#git ignore - ServiceAccountKey.json !!!!
array = []

if not internet():
    print('no internet')
    #wifiUsername = input('enter username')
    os.system('sudo ifconfig wlan0 up')	
    ssid='Savant@KLM'
    wifipw='@BCDE38724'
    myfile = "/etc/network/interfaces"

    with open(myfile, "r+") as f:
        data = f.read()
        f.seek(0)
        f.write(re.sub( 'source-directory /etc/network/interface.d\n'
                        'iface wlan0 inet dhcp\n'
                         '    wpa-ssid {}\n'
                         '    wpa-psk  {}\n'.format(ssid, wifipw), data))
        f.truncate()
    #with open('/etc/network/interfaces', 'a') as netcfg:
    #    netcfg.write('iface wlan0 inet dhcp\n'
   #                  '    wpa-ssid {}\n'
  #                   '    wpa-psk  {}\n'.format(ssid, wifipw))
    os.system("dhclient wlan0")
    os.system("sudo reboot")


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./ServiceAccountKey.json"
cred = credentials.Certificate('/home/pi/real/barcode/ServiceAccountKey.json')    
default_app = firebase_admin.initialize_app(cred, {'databaseURL': 'https://pyscan-a5e3e.firebaseio.com/'})
ref = db.reference('users/')
snapshot = ref.get()
print(snapshot)

def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial


#for snap, val in snapshot.items():
   # if getserial() == val.get('serial'):
 #       ref = db.reference('users/' + snap + '/barcodes')
    # print(snap)
    # print(val.get('serial'))





def whole():
    while True:
        if len(array) > 0:
            addToCart()
            array.pop(0)
        time.sleep(1)

def addToCart():
    session = requests.Session()

    response3 = session.get('https://www.shufersal.co.il/online/he/A')
    JSESSIONID = response3.cookies.get_dict().get('JSESSIONID')
    XSRFTOKEN = response3.cookies.get_dict().get('XSRF-TOKEN')
    print(XSRFTOKEN)
    print(JSESSIONID)

    cookies = {
        'miglog-cart': '20b6b657-d481-4991-b431-c0f6876b49f8',
        'XSRF-TOKEN': XSRFTOKEN,
        'JSESSIONID': JSESSIONID,
    }

    headers = {
        'authority': 'www.shufersal.co.il',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://www.shufersal.co.il',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.shufersal.co.il/online/he/login',
        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
      'fail_url': '/login/?error=true',
      'j_username': 'avivkalmanson@gmail.com',
      'j_password': 'Avivkalman1',
      'CSRFToken': XSRFTOKEN
    }

    response = session.post('https://www.shufersal.co.il/online/he/j_spring_security_check', headers=headers, cookies=cookies, data=data)
    response5 = session.get('https://www.shufersal.co.il/online/he/A')

    JSESSIONID2 = session.cookies.get_dict().get('JSESSIONID')
    XSRFTOKEN2 = session.cookies.get_dict().get('XSRF-TOKEN')
    AWSALB = session.cookies.get_dict().get('AWSALB')
    AWSALBCORS = session.cookies.get_dict().get('AWSALBCORS')
    list = response.cookies.get_dict()
    myList = {}
    for x in list:
        if x[0:2] == 'TS':
            myList[x] = list[x]
    myList["AWSALB"] = AWSALB
    myList["AWSALBCORS"] = AWSALBCORS

    myList["XSRF-TOKEN"] = XSRFTOKEN2
    myList["JSESSIONID"] = JSESSIONID2
    myList["miglog-cart"] = '20b6b657-d481-4991-b431-c0f6876b49f8'


    headers9 = {
        'authority': 'www.shufersal.co.il',
        'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
        'accept': '*/*',
        'csrftoken': XSRFTOKEN2,
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozill   a/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'content-type': 'application/json',
        'origin': 'https://www.shufersal.co.il',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        # 'referer': 'https://www.shufersal.co.il/online/he/promo/A?utm_source=google&utm_medium=search&utm_campaign=online_july&utm_content=brand&gclid=Cj0KCQiAhs79BRD0ARIsAC6XpaVfCi8XrCqiYqcCasNWN3IWzsunDlOZZ4S1ntk1cjcN-uIptY47ahgaAuCuEALw_wcB',
        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params2 = (
        ('cartContext[openFrom]', 'PROMOTION'),
        ('cartContext[recommendationType]', 'REGULAR'),
    )

    data2 = '{"productCodePost":"P_'+array[0]+'","productCode":"P_'+array[0]+'","sellingMethod":"BY_UNIT","qty":"1","frontQuantity":"1","comment":"","affiliateCode":""}'

    response2 = session.post('https://www.shufersal.co.il/online/he/cart/add', headers=headers9, params=params2, cookies=myList, data=data2)
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/real/barcode/added.mp3")
    pygame.mixer.music.play()
    

def ask():
    barcode = input('enter barcode')
    if(barcode.startswith('72900000')):
        barcode = barcode[8:]
    if (barcode.startswith('7290000')):
        barcode = barcode[7:]
    if (barcode.startswith('729000')):
        barcode = barcode[6:]
    print('your barcode is' + barcode)
    ref.push(barcode)
    array.append(barcode)
    print(array)
    ask()

if __name__ == '__main__':
    print('holy cow')
    thread1 = threading.Thread(target=ask).start()
    thread2 = threading.Thread(target=whole).start()
