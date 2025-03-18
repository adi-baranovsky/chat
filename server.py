import socket
import threading
import datetime
import os
import hashlib
import ssl

#variables
host = "127.0.0.1" #host
port = 8000 #port
listener_limit = 5
active_client = [] #all currently connected users
cred_path = r"C:\Users\kyoto\Documents\GitHub\FirstPython\chat\password.txt" #path for credentials file
chats_path = r"C:\Users\kyoto\Documents\GitHub\FirstPython\chat\chats.txt" #path for chat history file

#generate salt for the password
def generate_salt():
    #128 bit salt value
    salt = os.urandom(16)
    return salt

#create secured password with hash and salt
def secure_password(password, salt):
   password_hash = hashlib.sha256(str(salt).encode() + str(password).encode())  #hash with salt
   return password_hash.digest() #returns bytes of salt and hashed password

#check username and password
def check_cred(username, hashed_password):
    while True:
        with open(cred_path, "r") as accounts_file:
            for line in accounts_file:
                file_username, file_password, file_salt = line.replace("\n","").split("*****")
                hashed_password = str(hashed_password)
                if file_username == username and file_password == hashed_password:
                    return True
            return False

#check if username exists
def check_username(username):
    while True:
        try:
            with open(cred_path, "r") as accounts_file:
                for line in accounts_file:
                    file_username, file_password, file_salt = line.replace("\n","").split("*****")
                    if file_username == username:
                        return True
                return False
        except:
            return False

#get the salt that matches the username
def get_salt(username):
    while True:
        with open(cred_path, "r") as accounts_file:
            for line in accounts_file:
                file_username, file_password, file_salt = line.replace("\n","").split("*****")
                if file_username == username:
                    return file_salt
            return False

#keep listens for any new messages
def listen_for_messages(client, username):
    while True:
        message = client.recv(2048).decode("UTF-8")
        #if message is empty
        if message != "": 
            #if the clients quits
            if message.lower() == "exit":
                print(f"Ended Connection With {client.getpeername()[0]}:{client.getpeername()[1]}")
                client.close()
                exit(0)
            #else, continues as usual
            final_msg = f"{datetime.datetime.now()} | {username} ~ {message}"
            send_messages_to_all(final_msg)
            #add to chat file
            with open(chats_path, 'a', encoding='utf-8') as file:
                file.write(final_msg + "\n")

        else:
            #create and send final message
            print(f"the message from {client} is empty")


#send message to a specific client
def send_message_to_client(client, message):
    client.sendall(message.encode("UTF-8"))

#send to all connected users
def send_messages_to_all(message):
    for user in active_client:
        send_message_to_client(user[1], message) #user[1] is the client object in the tuple


def client_handler(client):
    #listen for client message that conatins username
    while True:
        cred = client.recv(2048).decode("UTF-8")

        #dicided by *****
        username = cred.split("*****")[0]
        password = cred.split("*****")[1]

        #username exists
        if check_username(username):
            #a salt exists, we'll get it and then compare
            salt = get_salt(username)
            hashed_password = secure_password(password, salt)

            #check username and password match
            if check_cred(username, hashed_password):
                #add to active clients
                active_client.append((username, client))
                
                #sends message
                welcome_msg = f"{datetime.datetime.now()} | SERVER ~ {username} has entered the chat"
                send_messages_to_all(welcome_msg)
                
                #add to file
                with open(chats_path, 'a', encoding='utf-8') as file:
                    file.write(welcome_msg + "\n")
                break
            
            #username exists but password is wrong
            else:
                print("Bad Password!")
                send_message_to_client(client, "BAD")
                client.close()
                exit(0)
            
        else: #new username and password
            #add to active clients
            active_client.append((username, client))
            #sends message
            welcome_msg = f"{datetime.datetime.now()} | SERVER ~ {username} signed up and has entered the chat"
            send_messages_to_all(welcome_msg)
            #add to file
            with open(chats_path, 'a', encoding='utf-8') as file:
                file.write(welcome_msg + "\n")
            salt = generate_salt()
            hashed_password = secure_password(password, salt)
            #add credentials to file
            with open(cred_path, 'a') as file:
                file.write(f"{username}*****{hashed_password}*****{salt}" + "\n")
            break
    
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

def main():
    #create socket server object and binding
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #try binding
    try: 
        server.bind((host, port))
        print("The server is up!")

    except: 
        print(f"Unable to bind to host {host} in port {port}")

    #to how many we listen
    server.listen(listener_limit)
    
    #create context to wrap the socket
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="certificate.pem", keyfile="private_key.pem")

    #encrypt the socket
    secure_socket = context.wrap_socket(server, server_side=True)

    while True:
        #accept connection
        client, address = secure_socket.accept()
        print(f"Accepted connection from {address[0]}:{address[1]}")

        #create and start thread every time a client connects
        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()