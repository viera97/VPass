import pyotp
import datetime

def get(secret, type):
    myotp = pyotp.totp.TOTP(secret)
    return str(myotp.now())

def geth(secret, at):
    myotp = pyotp.hotp.HOTP(secret)
    return str(myotp.at(at))

def gettime(secret, type):
    if type == "TOTP":
        myotp = pyotp.totp.TOTP(secret)
    else:
        myotp = pyotp.hotp.HOTP(secret)
    time_remaining = myotp.interval - datetime.datetime.now().timestamp() % myotp.interval
    return time_remaining