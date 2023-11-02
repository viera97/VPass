import pyotp

def get(secret):
    myotp = pyotp.totp.TOTP(secret)
    return str(myotp.now())