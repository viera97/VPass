import cv2
import pyzbar.pyzbar

def save_key_from_file(f):
    with open('qrcode_aux', 'wb+') as destination: 
        for chunk in f.chunks():
            destination.write(chunk)

def load_otp_file_img():
    img = cv2.imread('qrcode_aux', 0)
    barcodes = str(pyzbar.pyzbar.decode(img)[0][0]).split('secret=')[-1].split("%3D")[0]
    return barcodes

def load_otp_file_text():
    f = open('qrcode_aux', 'r')
    fl = f.readline()
    f.close()
    txt = ''
    for i in range(len(fl)-1):
        txt += fl[i]
    return txt

def load_otp_file():
    try:
        return load_otp_file_img()
    except:
        return load_otp_file_text()