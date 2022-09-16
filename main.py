import datetime
import json
import os
import socket
import threading
import time
import traceback
import pygame
import requests

token = ""
array = []

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


def playMusicMandatory(fileName):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("./" + fileName + ".mp3")
        pygame.mixer.music.play()
    except Exception:
        logError()


def logError():
    playMusicMandatory('error')
    time.sleep(5)
    try:
        with open('./logErrors.txt', 'a') as netcfg:
            netcfg.write(str(datetime.datetime.now()))
            netcfg.write(str(traceback.format_exc()))
    except:
        print('Problem writing to error file')
    try:
        myobj = json.dumps(
            {"message": traceback.format_exc(), "user": getserial()})
        log_aws_response = requests.post(
            'https://68wdquyeue.execute-api.us-east-2.amazonaws.com/beta/try', data=myobj)
        print(log_aws_response.text)
    except:
        print('No wifi so couldnt log')


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


def main_loop():
    while True:
        if len(array) > 0:
            try:
                addToCart()
            except Exception:
                logError()
            finally:
                array.pop(0)
        time.sleep(1)


def addToCart():
    barcode = array[0]
    add_product_response = requests.post(
        'https://scanly.net/api/products', data={"barcode": barcode, "amountToAdd": 1},
        headers={'cookie': 'token=' + token}
    )

    if add_product_response == 'true':
        playMusicMandatory('added')
    else:
        playMusicMandatory('addedList')


def ask():
    barcode = input('enter barcode')
    print('your original barcode is' + barcode)
    array.append(barcode)
    print(array)
    ask()

def create_files_if_not_exists():
    try:
        open("../email.txt", "r")
    except Exception:
        os.system("touch ../email.txt")

    try:
        open("../password.txt", "r")
    except Exception:
        os.system("touch ../password.txt")

if __name__ == '__main__':
    try:
        if not internet():
            print('No internet currently')
            playMusicMandatory('noInternet')

            create_files_if_not_exists()

            credentialsEmail = open("../email.txt", "r")
            credentialsPassword = open("../password.txt", "r")
            while(credentialsPassword.read() == "" and credentialsEmail == ""):
                print("waiting for cred")
                credentialsEmail = open("../email.txt", "r")
                credentialsPassword = open("../password.txt", "r")
                time.sleep(1)

            print('Connected Succesfully')
            playMusicMandatory('wifiConnected')

        credentialsEmail = open("../email.txt", "r")
        credentialsPassword = open("../password.txt", "r")

        login_response = requests.post(
            'https://scanly.net/api/login', data={"email": credentialsEmail, "password": credentialsPassword},
        )

        token = login_response.cookies.get_dict().get('token')

        ask_thread = threading.Thread(target=ask).start()
        main_loop_thread = threading.Thread(target=main_loop).start()
    except Exception:
        logError()
        time.sleep(5)
        os.system("sudo reboot")
