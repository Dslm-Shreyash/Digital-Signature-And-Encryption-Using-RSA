import socket
import Encryption_Methods as ae
import rsa

public , private = rsa.newkeys(1024)
port = 1234


joh = int(input("1 : Host \n2 : Join \nInput : "))    
if joh == 1:
      #!Server Part
    name = input("Enter Your Name : ")
    with open (f"{name}_key.pem","wb") as f:
        f.write(public.save_pkcs1("PEM"))

    s = socket.socket()
    host = socket.gethostname()

    print('server will start on host : ',host)

    s.bind((host,port))
    print("server is bound successfully\n")

    s.listen(5)
   
    co,ad = s.accept()
    name = name.encode()
    co.send(name)
    
    client_name = co.recv(1024).decode()
   
    print(f'{client_name} Has Joined')
    
    with open(f"{client_name}_key.pem","rb") as f:
        pk = f.read()
        
    public_key = rsa.PublicKey.load_pkcs1(pk)
    
    while True :
        responce = input("\nYou : ")
        
        cipher , siganture = ae.RSA_Encrypt_and_Sign(message=responce,privatekey=private,publickey=public_key,hashmethod="SHA-256")
        
        co.send(cipher)
        co.send(siganture)
        print(f'" {responce} " Is Encrypted To : {cipher} \n')
        
        cipher_msg = co.recv(1024)
        siganture = co.recv(1024)
        print(f"Received  Cipher From ' {client_name} ' Is : ",cipher_msg)
        
        decrypted_msg,verify_status = ae.RSA_Decrypt_and_Verify(ciphermessage=cipher_msg,privatekey=private,publickey=public_key,signature=siganture)
        print(f"Decrypted Cipher From ' {client_name} ' Is : ",decrypted_msg)
        print(verify_status)
        print("Signature Verified")if verify_status else print("Signature not Verified")
else:
     name = input("Enter Your Name : ")
     with open (f"{name}_key.pem","wb") as f:
        f.write(public.save_pkcs1("PEM"))
        
     client = input("Enter host name : ")

     s = socket.socket()
     s.connect((client,port))
     
     client_name = s.recv(1024).decode()
     with open(f"{client_name}_key.pem","rb") as f:
        pk = f.read()
    
     public_key = rsa.PublicKey.load_pkcs1(pk)
     name = name.encode()
    
     print("\nconnected to server\n")
     s.send(name)
     
     while True:
         cipher_msg = s.recv(1024)
         siganture = s.recv(1024)
         print(f"Received  Cipher From ' {client_name} ' Is : ",cipher_msg)

         decrypted_msg,verify_status = ae.RSA_Decrypt_and_Verify(ciphermessage=cipher_msg,privatekey=private,publickey=public_key,signature=siganture)
         print(f"Decrypted Cipher From ' {client_name} ' Is : ",decrypted_msg)
         print(verify_status)
         print("Signature Verified") if verify_status else print("Signature not Verified")
         
         responce = input("\nYou : ")
         cipher , siganture = ae.RSA_Encrypt_and_Sign(message=responce,privatekey=private,publickey=public_key,hashmethod="SHA-256")
        
         s.send(cipher)
         s.send(siganture)
         print(f'" {responce} " Is Encrypted To : {cipher} \n')