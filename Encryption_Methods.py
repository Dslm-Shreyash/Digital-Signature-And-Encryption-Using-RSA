from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import rsa

# key = b'\x10/\xce\xd1\x87BP\x81\x9b\x0e(\xa5\x99g\xd4\x8f'
key = get_random_bytes(16)
# key = b"This is the keyy"

def AES_Encrypt(msg):
    ecip = AES.new(key,AES.MODE_EAX)
    nonce = ecip.nonce
    ct = ecip.encrypt(msg)
    return key,nonce,ct 

def AES_Decrypt(key,obj,ct):
    dcip = AES.new(key, AES.MODE_EAX,obj)
    cd = dcip.decrypt(ct).decode()
    return cd

def RSA_Encrypt(message,publickey):
    cip = rsa.encrypt(message=message.encode(),pub_key=publickey)
    return cip

def RSA_Decrypt(ciphermessage,privatekey):
    dcip = rsa.decrypt(crypto=ciphermessage,priv_key=privatekey)
    return dcip.decode()

def RSA_Encrypt_and_Sign(message,privatekey,publickey,hashmethod):
    signature=rsa.sign(message=message.encode(),priv_key=privatekey,hash_method=hashmethod)
    cip = rsa.encrypt(message=message.encode(),pub_key=publickey)
    return cip,signature

def RSA_Decrypt_and_Verify(ciphermessage,privatekey,publickey,signature):
    dcip = rsa.decrypt(crypto=ciphermessage,priv_key=privatekey)
    try:
     Verify_Status=rsa.verify(message=dcip,signature=signature,pub_key=publickey)
    except:
        Verify_Status = 0
    return dcip.decode(),Verify_Status

def sign(message,privatekey,hashmethod):
    signature=rsa.sign(message=message.encode(),priv_key=privatekey,hash_method=hashmethod)
    return signature

def verify(dcip,signature,public):
    try:
     ver=rsa.verify(message=dcip,signature=signature,pub_key=public)
    except:
        ver =0
    return ver