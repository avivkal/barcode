import requests
import time
import threading
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
import socket
#from wifi import Cell, Scheme
import pygame
import re
import json


import requests


class mydict(dict):
    def __str__(self):
        return json.dumps(self)

#log in
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

data = '{"username":"avivkalmanson@gmail.com","password":"Avivkalman1"}'

response = requests.post('https://api-prod.rami-levy.co.il/api/v1/auth/login', headers=headers, data=data)
print(response)
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


#get items
headers2 = {
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

response = requests.post('https://api-prod.rami-levy.co.il/api/v1/cart/get-cart', headers=headers2)
json_data2 = json.loads(response.text).get('items')
print(json_data2)
for x in json_data2:
    x["C"] = x["id"]
    del x["id"]
    x["Quantity"] = x["quantity"]
    del x["quantity"]
    print(x)

print(json_data2)


#get item id
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

data4 = '{"q":"8410128768294","store":331,"sort":"relevant","aggs":1}'

response4 = requests.post('https://www.rami-levy.co.il/api/catalog', headers=headers4, data=data4)
json_data = json.loads(response4.text)
id = json_data.get('data')[0].get('id')
print(type(id))

found = False

for item in json_data2:
    if item.get('C') == id:
        item["Quantity"] = str(float(item.get('Quantity')) + 1.00)
        found = True
        print('found')

if not found:
    print('not found')
    json_data2.append({'C': id, 'Quantity': '1.00'})

print(json_data2)
myDict = mydict()
myDict['store'] = 331
myDict["is_club"] = 0
myDict['items'] = json_data2
print(myDict)

#add item to list

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.get('https://www.rami-levy.co.il/api/search?q=7290112348159&store=331', headers=headers)

#add the item
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

data3 = '{"store":331,"is_club":0,"items":[{"C":21,"Quantity":"3.00"},{"C":15,"Quantity":"0.50"},{"C":353814,"Quantity":"3.00"},{"C":6345,"Quantity":"2.00"},{"C":267163,"Quantity":"1.00"}]}'
print('-------------')
print(data3)
print(str(myDict))
print('-------------')
response3 = requests.post('https://api-prod.rami-levy.co.il/api/v1/cart/add-line-to-cart', headers=headers3, data=str(myDict))
print(response3)
print(response3.text)