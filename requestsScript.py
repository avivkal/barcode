import requests
import time
import threading
import os
import socket
import pygame
import re
import json 
from lxml import html
import pymongo
import datetime
from bs4 import BeautifulSoup

userEmail = ""
userPassword = ""
currentPrice = 0
client = pymongo.MongoClient('mongodb+srv://avivkal:Avivkalman1@cluster0.muucp.mongodb.net/database?retryWrites=true&w=majority')
productsRef = client.database.products
currentUser= ""

class mydict(dict):
    def __str__(self):
        return json.dumps(self)

def playMusic (fileName):
    if currentUser.get('sound') == True:
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/real/barcode/" + fileName + ".mp3")
        pygame.mixer.music.play()

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
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/real/barcode/wifiUsername.mp3")
    pygame.mixer.music.play()
    ssid = input('enter wifi username')
    pygame.mixer.init()
    pygame.mixer.music.load("/home/pi/real/barcode/wifiPassword.mp3")
    pygame.mixer.music.play()
    wifipw = input('enter wifi password')
    #ssid='Savant@KLM'
   # wifipw='@BCDE38724'
    with open('/etc/network/interfaces', 'w') as netcfg:
        netcfg.write('source-directory /etc/network/interfaces.d\n'
                     'auto wlan0\n'
                     'iface wlan0 inet dhcp\n'
                     '    wpa-ssid {}\n'
                     '    wpa-psk  {}\n'.format(ssid, wifipw))
    with open('/home/pi/wifiInfo.txt', 'w') as netcfg:
        netcfg.write(ssid + ',' + wifipw)
    os.system("dhclient wlan0")
    os.system("sudo reboot")

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



def wholeRami():
    while True:
        if len(array) > 0:
            addToCartRami()
            array.pop(0)
        time.sleep(1)

def whole():
    while True:
        if len(array) > 0:
            addToCart()
            array.pop(0)
        time.sleep(1)
        
def addToCartRami():
    headers = {
        'authority': 'api-prod.rami-levy.co.il',
        'accept': 'application/json, text/plain, */*',
        'locale': 'he',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'ecomtoken': 'faa5dc4c-66db-483c-a767-49ce5becaf93',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://www.rami-levy.co.il',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    dataT = mydict()
    dataT["username"] = userEmail
    dataT["password"] = userPassword
    print(dataT)
    data = '{"username":"avivkalmanson@gmail.com","password":"Avivkalman1"}'
    response = requests.post('https://api-prod.rami-levy.co.il/api/v1/auth/login', headers=headers, data=str(dataT))
    print(response.text)
    token = json.loads(response.text).get('user').get('token')
    print(token)

    headers5 = {
        'authority': 'api-prod.rami-levy.co.il',
        'content-length': '0',
        'accept': 'application/json, text/plain, */*',
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjIxNzE5ZDM2NzI0OGYyZDAwY2RkMThmM2U5ZmJhNGYxYTU1OTRkYjZlYjI3ODY4ZTlmZmJhNWI0YTdmNTc2Y2IwNDg3N2FiNjY1ODMwYWNjIn0.eyJhdWQiOiIzIiwianRpIjoiMjE3MTlkMzY3MjQ4ZjJkMDBjZGQxOGYzZTlmYmE0ZjFhNTU5NGRiNmV$',
        'locale': 'he',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'ecomtoken': token,
        'origin': 'https://www.rami-levy.co.il',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    response = requests.post('https://api-prod.rami-levy.co.il/api/v1/clubs/user', headers=headers5)

    # get items

    response = requests.post('https://api-prod.rami-levy.co.il/api/v1/cart/get-cart', headers=headers5)
    json_data2 = json.loads(response.text).get('items')
    for x in json_data2:
        x["C"] = x["id"]
        del x["id"]
        x["Quantity"] = x["quantity"]
        del x["quantity"]

    print(json_data2)

    # get item id
    headers4 = {
        'authority': 'www.rami-levy.co.il',
        'accept': 'application/json, text/plain, */*',
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjIxNzE5ZDM2NzI0OGYyZDAwY2RkMThmM2U5ZmJhNGYxYTU1OTRkYjZlYjI3ODY4ZTlmZmJhNWI0YTdmNTc2Y2IwNDg3N2FiNjY1ODMwYWNjIn0.eyJhdWQiOiIzIiwianRpIjoiMjE3MTlkMzY3MjQ4ZjJkMDBjZGQxOGYzZTlmYmE0ZjFhNTU5NGRiNmV$',
        'locale': 'he',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'ecomtoken': token,
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://www.rami-levy.co.il',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'auth.strategy=local; visid_incap_2021397=sPFFpK/PS+yAr9pm0NxBfgthvV8AAAAAQUIPAAAAAACG0TuuytzAgRk4nmIM2Grf; nlbi_2021397=xQ8oAoumGwpmuO7x9kJt1wAAAABcQGX8CSG+JykVzN7Ua9S4; i18n_redirected=he; visid_incap_2256378=4sxLhhFyRkm/BXSJuTPTEqFhvV8AAAAAQUIPAAAAAACjvb9h96jNw+uKdS8Mz2Y1; _ga=GA1.3.1561077822.1606246785; _gid=GA1.3.621100251.1606246785; incap_ses_820_2021397=DCz8AnFF9gNkMvSq5jlhC1wtvl8AAAAABk92NFgi5a2ruqG8FjcVVQ==; incap_ses_820_2256378=LO6CDVjbuxIcUvmq5jlhC7M8vl8AAAAAa2Rw5jYxX3iAE69/0pnMJg==; _gat=1; nlbi_2021397_2147483646=ILMkJ4VcjkvIt+Ws9kJt1wAAAAC2uFNzR0L3P6aSNRsR/O1k; reese84=3:/oznrNAzeeagyLr+R25PVQ==:reGYoDLEa29iKN92S0yDCJZNZiPnt154ZzaZwUYYLWrWALbZwxURDfov13cP8jvioYZPnS3/QAlluVnikIJA8YIC+ZwuYfesjNHEpsjPiYo2Lz3VoUUP4skHdk+RYRry3kh7uTS4FQ7oza1pp2PqBcNlJZUptgUGo3LE+s/EA3INWpLDLUipa3D5X3nyWLZbdNisZSf03+jfualxV7aljYbDu54ljcixzkSvlTkpm3SkjQ+oqBUhkPq/O70EDyhneBPndmtWDJlNhRndFbNrFJAN5FJMa9HPp72/m1VDdJ1c8hBZgH6Uc78CfgaEuALfEjAewsQRDIVQV6vFBQLIDvJSq2EAC2JufRpetOFpKyjCs5cDL6Tnr4VAHg9JbpM+JZMN4K93NM+4yoTO09Fd/eiN+pkRgQ6V6uMfytB7KM2oTHP+BEyNq2I7IfJoyjc/3LSohLfYCkhbKdAoAzIb3Q==:E5dgZOiqtWh/7VBMjg3xqeHMIwpfGguLRtwMxp3OpRs=',
    }

    data4 = '{"q":"'+ array[0] +'","store":331,"sort":"relevant","aggs":1}'
    try:
        response4 = requests.post('https://www.rami-levy.co.il/api/catalog', headers=headers4, data=data4)
        json_data = json.loads(response4.text)
        id = json_data.get('data')[0].get('id')

        found = False

        for item in json_data2:
            if item.get('C') == id:
                item["Quantity"] = str(float(item.get('Quantity')) + 1.00)
                found = True
                print('found')

        if not found:
            print('not found')
            json_data2.append({'C': id, 'Quantity': '1.00'})

        myDict = mydict()
        myDict['store'] = 331
        myDict["is_club"] = 0
        myDict['items'] = json_data2

        # add the item
        headers3 = {
            'authority': 'api-prod.rami-levy.co.il',
            'accept': 'application/json, text/plain, */*',
            'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjIxNzE5ZDM2NzI0OGYyZDAwY2RkMThmM2U5ZmJhNGYxYTU1OTRkYjZlYjI3ODY4ZTlmZmJhNWI0YTdmNTc2Y2IwNDg3N2FiNjY1ODMwYWNjIn0.eyJhdWQiOiIzIiwianRpIjoiMjE3MTlkMzY3MjQ4ZjJkMDBjZGQxOGYzZTlmYmE0ZjFhNTU5NGRiNmV$',
            'locale': 'he',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
            'ecomtoken': token,
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://www.rami-levy.co.il',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
        }

        response3 = requests.post('https://api-prod.rami-levy.co.il/api/v1/cart/add-line-to-cart', headers=headers3,data=str(myDict))
        playMusic('added')
        addProductToDB(array[0],True)
    except:
        print('could not add to cart')
        playMusic('addedList')
        addProductToDB(array[0],False)

def addToCart():
    barcode = array[0]
    croppedBarcode = array[0]
    if(barcode.startswith('72900000')):
        croppedBarcode = barcode[8:]
    elif (barcode.startswith('7290000')):
        croppedBarcode = barcode[7:]
    elif (barcode.startswith('729000')):
        croppedBarcode = barcode[6:]
    
    print(croppedBarcode + ' yessss')
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
      'j_username': userEmail,
      'j_password': userPassword,
      'CSRFToken': XSRFTOKEN
    }

    response = session.post('https://www.shufersal.co.il/online/he/j_spring_security_check', headers=headers, cookies=cookies, data=data)
    response5 = session.get('https://www.shufersal.co.il/online/he/A')
    doc = html.fromstring(response5.content)
    try:
        link = doc.xpath('//*[@id="cartContainer"]/div/div/footer/div[2]/div/div/div[1]/span/text()')
        currentPrice = link[1]
        print(currentPrice)
    except IndexError:
        print("No link found")
        
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

    data2 = '{"productCodePost":"P_'+croppedBarcode+'","productCode":"P_'+croppedBarcode+'","sellingMethod":"BY_UNIT","qty":"1","frontQuantity":"1","comment":"","affiliateCode":""}'

    response2 = session.post('https://www.shufersal.co.il/online/he/cart/add', headers=headers9, params=params2, cookies=myList, data=data2)
    responseCheck = session.get('https://www.shufersal.co.il/online/he/A')
    doc = html.fromstring(responseCheck.content)
    try:
        link = doc.xpath('//*[@id="cartContainer"]/div/div/footer/div[2]/div/div/div[1]/span/text()')
        if link[1]!= currentPrice:
            print("Product was added to your cart")
            print(link[1])
            currentPrice = link[1]
            playMusic('added')
            addProductToDB(barcode,True)
        else:
            print("Product could not be added")
            playMusic('addedList')
            addProductToDB(barcode,False)
    except IndexError:
        print("Product could not be added")
        playMusic('addedList')
        addProductToDB(barcode,False)
    
def addProductToDB(barcode,added):
    productsRef.insert_one({"email": currentUser.get('email'),"selection":currentUser.get('selection'),"barcode":barcode,"creationDate": datetime.datetime.now(),"added":added})

def ask():
    barcode = input('enter barcode')
    print('your original barcode is' + barcode)
    response8 = requests.get('https://www.shufersal.co.il/online/he/search?text=' + barcode)
    soup = BeautifulSoup(response8.content, 'html.parser')
    mydivs1 = soup.findAll("span", {"class": "price"})
    mydivs = mydivs1.findAll("span", {"class": "number"})
    print(mydivs)
    #bigRef.child('barcodes').push(barcode)
    #addProductToDB(barcode,true)
    array.append(barcode)
    print(array)
    ask()

if __name__ == '__main__':
    id = 0
    print('holy cow')
    file = open('/home/pi/wifiInfo.txt', "r")
    textArr = file.readline().split(',')
    
    db = client.database.users
    currentUser = db.find_one({"wifiUsername":textArr[0],"wifiPassword":textArr[1]})
    print(currentUser)
      #  print(snapshot.child(val).child('wifi').child('username').val())
    print(textArr[0])
    print('----')
    print(textArr[1])
    userSelect = currentUser.get('selection')
    print(userSelect + ' realllll')
    thread1 = threading.Thread(target=ask).start()
    #if bigRef.child('details').child.
    if userSelect == 'Shufersal':
        userEmail = currentUser.get('shufersalUsername')
        print(userEmail)
        userPassword = currentUser.get('shufersalPassword')
        print(userPassword)
        playMusic('shufersal')
        thread2 = threading.Thread(target=whole).start()
    else:
        userEmail = currentUser.get('ramiLevyUsername')
        print(userEmail)
        userPassword = currentUser.get('ramiLevyPassword')
        print(userPassword)
        playMusic('rami')
        thread2 = threading.Thread(target=wholeRami).start()
