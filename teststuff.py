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
import traceback
import pyqrcode

# userEmail = ""
# userPassword = ""
current_price = 0
currentUser = ""


class mydict(dict):
    def __str__(self):
        return json.dumps(self)


def getserial():
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


def job():
    try:
        myData = {"id": getserial()}
        requests.post('https://scanly.net/api/count/inc', data=myData)
    except:
        print('couldn\'t update count')


def scheduleTask():
    os.system("sudo pip3 install schedule")
    import schedule
    schedule.every().day.at("15:00").do(job)
    while 1:
        schedule.run_pending()
        time.sleep(1)


def logError():
    playMusic('error', True)
    time.sleep(5)
    try:
        with open('/home/pi/logErrors.txt', 'a') as netcfg:
            netcfg.write(str(datetime.datetime.now()))
            netcfg.write(str(traceback.format_exc()))
    except:
        print('no file')
    try:
        error_message = json.dumps({"message": traceback.format_exc(), "user": getserial()})
        requests.post('https://68wdquyeue.execute-api.us-east-2.amazonaws.com/beta/try', data=error_message)
    except:
        print('no wifi')


print(getserial())
url = pyqrcode.create(getserial(), version=3)
url.svg('uca-url.svg', scale=8)
url.eps('uca-url.eps', scale=2)


def playMusic(fileName, is_mandatory=False):
    try:
        if is_mandatory or currentUser.get('sound'):
            pygame.mixer.init()
            pygame.mixer.music.load("/home/pi/real/barcode/" + fileName + ".mp3")
            pygame.mixer.music.play()
    except Exception:
        logError()


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


barcodes_array = []

if not internet():
    print('no internet')
    playMusic('noInternet', True)
    os.system('sudo wifi-connect --ui-directory /home/pi/scanly-ui-wifi/build --portal-ssid Scanly')
    playMusic('wifiConnected', True)

if internet():
    try:
        logs = open("/home/pi/logErrors.txt", "r")
        logs_content = logs.read()
        logs_object = json.dumps({"logs": logs_content, "user": getserial()})
        requests.post('https://68wdquyeue.execute-api.us-east-2.amazonaws.com/beta/try', data=logs_object)
    except:
        print('logs problem occured')


def add_to_cart_loop():
    while True:
        if len(barcodes_array) > 0:
            try:
                if currentUser.get('selection') == 'Shufersal':
                    addToCartShufersal()
                elif currentUser.get('selection') == 'Rami Levy':
                    addToCartRami()
                # else:
                #     addToCartGeneric()
            except Exception:
                logError()
            finally:
                barcodes_array.pop(0)
        time.sleep(1)


def addToCartRami():
    items = dict()

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
    dataT["username"] = currentUser.get('ramiLevyUsername')
    dataT["password"] = currentUser.get('ramiLevyPassword')

    response = requests.post('https://api-prod.rami-levy.co.il/api/v2/site/auth/login', headers=headers,
                             data=str(dataT))
    token = json.loads(response.text).get('user').get('token')

    try:
        items = json.loads(response.text).get('cart').get('items')
    except:
        print('couldnt get items')

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

    data4 = '{"q":"' + barcodes_array[0] + '","store":331,"sort":"relevant","aggs":1}'
    try:
        response4 = requests.post('https://www.rami-levy.co.il/api/catalog', headers=headers4, data=data4)
        json_data = json.loads(response4.text)
        id = ""
        for product in json_data.get('data'):
            if str(product.get('barcode')) == str(barcodes_array[0]):
                id = product.get('id')

        if id == "":
            raise Exception("Sorry, product was not found")

        found = False

        for item in items:
            if item == str(id):
                items[item] = items[item] + 1
                found = True
                print('found')

        if not found:
            print('not found')
            items[id] = 1

        for key, value in items.items():
            items[key] = str(value)

        # print(sub)
        myDict = mydict()
        myDict['store'] = "331"
        myDict["is_club"] = 0
        myDict['items'] = items

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

        response3 = requests.post('https://www.rami-levy.co.il/api/cart', headers=headers3, data=str(myDict))
        print(response3.text)
        playMusic('added')
        addProductToDB(barcodes_array[0], True)
    except:
        print('could not add to cart')
        playMusic('addedList')
        addProductToDB(barcodes_array[0], False)

def addToCartShufersal():
    barcode = barcodes_array[0]
    croppedBarcode = barcodes_array[0]
    if (barcode.startswith('72900000')):
        croppedBarcode = barcode[8:]
    elif (barcode.startswith('7290000')):
        croppedBarcode = barcode[7:]
    elif (barcode.startswith('729000')):
        croppedBarcode = barcode[6:]

    session = requests.Session()

    authenticationResponse = session.get('https://www.shufersal.co.il/online/he/A')
    JSESSIONID = authenticationResponse.cookies.get_dict().get('JSESSIONID')
    XSRFTOKEN = authenticationResponse.cookies.get_dict().get('XSRF-TOKEN')

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

    headersTest = {
        'authority': 'www.shufersal.co.il',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'accept': '*/*',
        'content-type': 'application/json',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.shufersal.co.il/online/he/miglog-checkout',
        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    cookiesTest = {
        'blackFriday': 'inTest',
        'XSRF-TOKEN': 'c1d6c23d-1ca8-42e0-93d4-bca552141605',
        'JSESSIONID': '9F16B3F36DC5A18F948E1C26189EB52C',
        'miglogstorefrontRememberMe': 'YXZpdmthbG1hbnNvbkBnbWFpbC5jb206MTY2ODYzMDg2MTExODozOTI4YmM4MDAyNjA1ZTM2NzMyYzI2YjE2YTM5N2M1ZA',
        'TS01585391': '0135176ca7fd5a553e6a1b143df5f288e218e5175223d5fa6a4e4677487e850b80243fedbce3f5c351956fc3f36f42a737e3dd91c7722b812b16a3f670fa7358a48c9f733e5243d47f054c9a10ee30e854b613a37b5ec85e747aa5dfe971b8377570e7e4f4bd4af1f6ae0dcd1c2e0cf9655e632cb0',
        'BIGipServerPool_LandingPages': '862786570.20480.0000',
        '_gaexp': 'GAX1.3.cHB7yKRQSpi8dqq9SfcxqQ.19024.1!tTj0K5qjSfKoc3gZYhoelQ.19028.1!R-a5VKf6Q-e9dRQvxAjbhQ.19039.1',
        '_gid': 'GA1.3.316455999.1637078315',
        '_gcl_au': '1.1.556043702.1637078315',
        'com.silverpop.iMAWebCookie': '9314980a-e059-021b-8656-56bda498de5b',
        'ImcVisitorFlag': '1',
        'BIGipServerPool_ShufersalDirect_Commerce_Servers_HTTP': '1600984074.20480.0000',
        'TS01311fea': '018c1146a4152e3a59a8822903f2c76619d9cad79b1a561889699b7797a60de39bdb79e9cbf1bdfef4e61af49b371c75bcd72d13ec179fd896b229129bd6cdc939c9642dbf',
        'TS3010e44d027': '08ee439653ab2000128794234601215bf21e7514cb670d3519b7fd2360b4895257e73a8fe96232be08123936cb113000ca1a1305824a9759d1ad8697e6ce2b505bd3a661b42e148bf20163949d71350c0c7812281cdbcd3be817111dab592a00',
        'com.silverpop.iMA.session': 'd521749e-a912-a161-8aa7-24c711281d4c',
        'acceleratorSecureGUID': '4e019eabeb704f95bc6325e3d5ea96a0553480a8',
        'com.silverpop.iMA.page_visit': '-185351059:1018363036:819143684:',
        '_gat_UA-27526974-20': '1',
        '_gat_UA-27526974-1': '1',
        'usfu_wPlQK1_f9JTaA3NnH24793Q%3d%3d': 'true',
        'cto_bundle': 'rcU8rV9oeHhMQTZaQkJjYnYwRUxBVUN3RVhNRzNaWkR3UUY4dmNKSWFzZFhoYzFHclpiTCUyQlBpTzF4ejFlNEJvT2JJa0JsTGU4OEt5S0pnaG5lODhaUlJnU1ZTYlZHV3dyMk1uZGhmUGxBZEZ1WWMyU0M5N3U0MWRXMUVwc1BuWTAzOG9EdmtJeiUyRjZRVVNzVjFUTHhHWGlZSllBJTNEJTNE',
        'outbrain_cid_fetch': 'true',
        '_ga': 'GA1.3.997411171.1637078315',
        '_ga_JNGKGQCSJD': 'GS1.1.1637094823.4.1.1637095972.47',
        'AWSALB': '5Ki7O80+4FoVbh5v/CeiyczZ2M+AT2dhB7RctBwKjRyzZn7xMOOCu0y3l7qOp6eTe8ThNGcGwj98hxbRLCQlbRjdliX3X2VQp088lEHHS0pzpbgqAKt0aDaP1h9T',
        'AWSALBCORS': '5Ki7O80+4FoVbh5v/CeiyczZ2M+AT2dhB7RctBwKjRyzZn7xMOOCu0y3l7qOp6eTe8ThNGcGwj98hxbRLCQlbRjdliX3X2VQp088lEHHS0pzpbgqAKt0aDaP1h9T',
        'TS0176b833': '0135176ca7d6bc2bcc925d81b12a08201fef8816cbca28978eef49b09a8f69854e0a252e01b83594d8344680c47b7ba9e5372e4097924437bf608e1f2c99f7087305699df5e70f41a4319b7288557434bb84f264ce',
    }

    login_details = {
        'fail_url': '/login/?error=true',
        'j_username': currentUser.get('shufersalUsername'),
        'j_password': currentUser.get('shufersalPassword'),
        'CSRFToken': XSRFTOKEN
    }

    response = session.post('https://www.shufersal.co.il/online/he/j_spring_security_check', headers=headers,
                            cookies=cookies, data=login_details)


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
        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    params2 = (
        ('cartContext[openFrom]', 'PROMOTION'),
        ('cartContext[recommendationType]', 'REGULAR'),
    )

    headers = {
        'authority': 'www.shufersal.co.il',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.shufersal.co.il/online/he/%D7%A7%D7%98%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%AA/%D7%A1%D7%95%D7%A4%D7%A8%D7%9E%D7%A8%D7%A7%D7%98/%D7%A4%D7%90%D7%A8%D7%9D-%D7%95%D7%AA%D7%99%D7%A0%D7%95%D7%A7%D7%95%D7%AA/%D7%93%D7%90%D7%95%D7%93%D7%95%D7%A8%D7%A0%D7%98/%D7%93%D7%90%D7%95%D7%93%D7%95%D7%A8%D7%A0%D7%98-%D7%A1%D7%A4%D7%A8%D7%99%D7%99-%D7%92%D7%91%D7%A8/%D7%90%D7%A7%D7%A1-%D7%A1%D7%A4%D7%A8%D7%99%D7%99-%D7%92%D7%95%D7%A3-%D7%91%D7%9C%D7%90%D7%A7/p/P_8717163647226',
        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    try:
        cart_response = session.get('https://www.shufersal.co.il/online/he/checkout/costSummary/direct', cookies=myList, headers=headers)
        print(cart_response.text)
        current_price = json.loads(cart_response.text).get('totalAmount')
    except Exception:
        print(traceback.format_exc())


    response = requests.get('https://www.shufersal.co.il/online/he/recommendations/entry-recommendations',
                            headers=headers, cookies=myList)
    print(response.text)
    amount = 1
    cart_products = json.loads(response.text)
    for product in cart_products:
        print(product)
        if str(product.get('productCode')) == "P_" + str(croppedBarcode):
            amount = int(product.get('cartyQty')) + 1
            print(amount)
            # might wanna add a return statement
    strAmount = str(amount)

    data2 = '{"productCodePost":"P_' + croppedBarcode + '","productCode":"P_' + croppedBarcode + '","sellingMethod":"BY_UNIT","qty":"' + strAmount + '","frontQuantity":"' + strAmount + '","comment":"","affiliateCode":""}'

    response2 = session.post('https://www.shufersal.co.il/online/he/cart/add', headers=headers9, params=params2,
                             cookies=myList, data=data2)
    # responseCheck = session.get('https://www.shufersal.co.il/online/he/A')
    # doc = html.fromstring(responseCheck.content)
    print('here')

    try:
        new_cart_response = session.get('https://www.shufersal.co.il/online/he/checkout/costSummary/direct', headers=headers, cookies=myList)
        print(new_cart_response.text)
        updated_price = json.loads(new_cart_response.text).get('totalAmount')
        print(updated_price)
        print(current_price)
        if updated_price != current_price:
            print("Product was added to your cart")
            current_price = updated_price
            playMusic('added')
            addProductToDB(barcode, True)
        else:
            print("Product could not be added")
            playMusic('addedList')
            addProductToDB(barcode, False)
    except IndexError:
        print("Product could not be added")
        playMusic('addedList')
        addProductToDB(barcode, False)


def addProductToDB(barcode, added):
    croppedBarcode = barcode
    shufersal_price = 'לא נמצא'
    rami_levy_price = 'לא נמצא'
    image = ''
    name = ''

    if (barcode.startswith('72900000')):
        croppedBarcode = barcode[8:]
    elif (barcode.startswith('7290000')):
        croppedBarcode = barcode[7:]
    elif (barcode.startswith('729000')):
        croppedBarcode = barcode[6:]
    try:
        shufersal_search_response = requests.get('https://www.shufersal.co.il/online/he/search/results?q={}'.format(croppedBarcode))
        shufersal_price = json.loads(shufersal_search_response.text).get('results')[0].get('price').get('value')
    except:
        print('shufersal not found')
    headers9 = {
        'authority': 'www.rami-levy.co.il',
        'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
        'locale': 'he',
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjIxNzE5ZDM2NzI0OGYyZDAwY2RkMThmM2U5ZmJhNGYxYTU1OTRkYjZlYjI3ODY4ZTlmZmJhNWI0YTdmNTc2Y2IwNDg3N2FiNjY1ODMwYWNjIn0.eyJhdWQiOiIzIiwianRpIjoiMjE3MTlkMzY3MjQ4ZjJkMDBjZGQxOGYzZTlmYmE0ZjFhNTU5NGRiNmV$',
        'content-type': 'application/json;charset=UTF-8',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'sec-ch-ua-mobile': '?0',
        'ecomtoken': '48837ef29656a9678d28e2b08734104e5ac412f505d9eb89bc46eb07fd2794c4',
        'origin': 'https://www.rami-levy.co.il',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.rami-levy.co.il/he/shop/search?q=8717163647226',
        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': 'visid_incap_2021397=nYC3WoN+QvionmgCV/KAuv7Ujl8AAAAAQUIPAAAAAAAWVrDAqj4FIiHmqWNHAXS4; i18n_redirected=he; _ga=GA1.3.652806923.1603196161; visid_incap_2256378=uy5pV0DkRWmN9TDryS1KRQjVjl8AAAAAQUIPAAAAAABvCCZmFxadU5djeOszvRh5; reese84=3:WaqpGFdm3jgYolW4kfPvqQ==:aOidVe3pgJqok3ziQypZq5XGr1jNlDHhXVcrj/UtmEP1YK5scz8DS5SuBJWebq5aUAciBTdZ03ssqHzQMqi/G3tppVyIb1bMn7bZA6qBYLJucdXf2kAZcBjcdICDjVtRUC22KdmTg0VKKMusFS42vk1+X0j3otcu6qlFk1P6FfYOqIu+w0pCGahCRFD2pJk3qPI5x+DzbyUwBH53Mu99gw+eeJk+xEzFCwnoMbdCVFfaKsDAGozqTITUi856ChPskhU8Ovs9AugnQA/7xVu3mKc8xS4YM9IEBZdekQlJlKuGPPItDvUDYBoeVVEexNi2nKc/5bcpueS7Zx0uNz0OPeSyjBarRtFtQypXpKJjjOj4m5duoJiT37pqzjtnJPk4f2liaYFb63FJa9m/Z37fhAve4GDUHePnEDtRpTZimyfcBum7aZd088s8dUELsMAZNN/cH+OvceMMtGJcA5rA7Q==:sbhOCwCaZ7+S+y5BWD44AsNPlwxYg4tstQ3bjra4/kQ=; _gid=GA1.3.618706417.1607465195; auth.strategy=local; _gat=1',
    }
    dataDict = mydict()
    dataDict["q"] = barcode
    dataDict["store"] = 331
    dataDict["sort"] = "relevant"
    dataDict["aggs"] = 1
    try:
        rami_levy_search_response = requests.post('https://www.rami-levy.co.il/api/catalog', headers=headers9, data=str(dataDict))
        rami_levy_price = json.loads(rami_levy_search_response.text).get('data')[0].get('price').get('price')
    except:
        print('rami levy not found')
    try:
        product_details_response = requests.get('https://chp.co.il/autocompletion/product_extended?term=' + barcode)
        name = json.loads(product_details_response.text)[0].get('value')
        image = 'data:image/png;base64,' + json.loads(product_details_response.text)[0].get('parts').get('small_image')
        print(name)
    except:
        print('name/image not found')
    save_data_to_db_response = requests.post('https://scanly.net/api/products/addData',
                                     cookies={'token': currentUser.get('token')},
                                     data={"email": currentUser.get('email'), "selection": currentUser.get('selection'),
                                           "barcode": barcode, "creationDate": datetime.datetime.now(),
                                           "added": str(added), "shufersalPrice": shufersal_price,
                                           "ramiLevyPrice": rami_levy_price, "image": image, "name": name})
    print(save_data_to_db_response)


def wait_for_input():
    barcode = input('enter barcode')
    print('your original barcode is' + barcode)
    barcodes_array.append(barcode)
    print(barcodes_array)
    wait_for_input()


if __name__ == '__main__':
    try:
        device_login_response = requests.post('https://scanly.net/api/login/idValidation', data={"deviceID": getserial()})
        currentUser = json.loads(device_login_response.text)
        currentUser["token"] = device_login_response.cookies.get_dict().get('token')
        input_thread = threading.Thread(target=wait_for_input).start()
        schedule_thread = threading.Thread(target=scheduleTask).start()
        if currentUser.get('selection') == 'Shufersal':
            playMusic('shufersal', True)
        elif currentUser.get('selection') == 'Rami Levy':
            playMusic('rami', True)
        add_to_cart_thread = threading.Thread(target=add_to_cart_loop).start()
    except Exception:
        logError()
