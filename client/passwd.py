import random
import os
import string

characters = [list(string.ascii_letters), ['!', '"', '#', '$', '%', '&', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~'], list(string.digits)]

def check_pass(password):
    cont = 0

    if len(password) < 8:
        return False
    else:
        cont += 1

    if password.lower() == password or password.upper() == password:
        return False
    else:
        cont += 1

    for character in password:
        if character in characters[1]:
            cont += 1
            break
    
    for character in password:
        if character in characters[2]:
            cont += 1
            break

    if cont == 4:
        return True
    else:
        return False
    
def generate(n):
    try:
        n = int(n)
    except:
        raise Exception('You are trying to generate a password for not int lenght')
    
    if n<8:
        raise Exception('You are trying to generate a password with lenght < 8')
        
    password = ''
    for i in range(n):
        password += random.choice(random.choice(characters))
    if check_pass(password):
        return password
    else:
       return generate(n)

if __name__ == '__main__':
    print(check_pass('5L1i6n*~6189P666*5)9h{z*.T8583}y]6}'))