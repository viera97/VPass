from cryptography.fernet import Fernet
import base64

def encrypt(txt, key):
    txt = str(txt)
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
    encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode('ascii')
    return encrypted_text
    
def decrypt(txt, key):
    txt = base64.urlsafe_b64decode(txt)
    cipher_suite = Fernet(key)
    decoded_text = cipher_suite.decrypt(txt).decode("ascii")
    return decoded_text

def write_key(name):
	key = Fernet.generate_key()
	with open(name, "wb") as key_file:
		key_file.write(key)

def write_key_paste(name, key):
	with open(name, "w") as key_file:
		key_file.write(key)

def write_final_key(key):
	with open("secure_key", "wb") as key_file:
		key_file.write(key)

def load_key(name):
	return open(name, "rb").read()

def save_key_from_file(f):
    with open('secure_key_aux', 'wb+') as destination: 
        for chunk in f.chunks():
            destination.write(chunk)