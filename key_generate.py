'''
Notice: this file will generate a public and private key
for private key, should only be exist on your trust PC
'''
#import rsa
from Crypto.PublicKey import RSA
import os

PublicKey_path = "./public.pem"
PrivateKey_path = "D:/mykey.pem"


def print_private_key():
    with open(PrivateKey_path, 'r') as f:
        print(f.read())

def print_public_key():
    with open(PublicKey_path, 'r') as f:
        print(f.read())



key = RSA.generate(2048)
public_key_val = key.publickey().exportKey('PEM')
private_key_val = key.exportKey('PEM')

print(public_key_val)
print(private_key_val)

# public key
if False: #os.path.exists(PublicKey_path):
    print("already exist public key")
    print_public_key()
else :
    with open(PublicKey_path,'wb') as f:
        f.write(public_key_val)
        print_public_key()

# private key
if False: #os.path.exists(PrivateKey_path):
    print("already exist public key")
    print_private_key()
else :
    with open(PrivateKey_path,'wb') as f:
        f.write(private_key_val)
        print_private_key()


