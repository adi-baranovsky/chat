import socket
import threading
import datetime

#variables
host = "127.0.0.1"
port = 8000
listener_limit = 5
active_client = [] #all currently connected users
cred_path = r"C:\Users\kyoto\Documents\GitHub\FirstPython\chat\password.txt"
chats_path = r"C:\Users\kyoto\Documents\GitHub\FirstPython\chat\chats.txt"

#check password
def check_cred(username, password):
    while True:
        with open(cred_path, "r") as accounts_file:
            for line in accounts_file:
                file_username, file_password = line.replace("\n","").split("|")
                if file_username == username and file_password == password:
                    return True
            return False
        
def check_username(username):
    while True:
        with open(cred_path, "r") as accounts_file:
            for line in accounts_file:
                file_username, file_password = line.replace("\n","").split("|")
                if file_username == username:
                    return True
            return False

#keep listens for any new messages
def listen_for_messages(client, username):
    while True:
        message = client.recv(2048).decode("UTF-8")

        #if message is empty
        if message != "": 
            final_msg = f"{datetime.datetime.now()} | {username} ~ {message}"
            #print(final_msg)
            send_messages_to_all(final_msg)

            with open(chats_path, 'a') as file:
                file.write(final_msg + "\n")

        else:
            #create and send final message
            print(f"the message from {client} is empty")


#send message to a specific client
def send_message_to_client(client, message):
    client.sendall(message.encode("UTF-8"))

#send to all connected users
def send_messages_to_all(message):
    print()
    for user in active_client:
        send_message_to_client(user[1], message) #user[1] is the client object in the tuple


def client_handler(client):
    #listen for client message that conatins username
    while True:
        cred = client.recv(2048).decode("UTF-8")

        username = cred.split("|")[0]
        password = cred.split("|")[1]
        
        if check_cred(username, password):
            active_client.append((username, client))
            welcome_msg = f"{datetime.datetime.now()} | SERVER ~ {username} has entered the chat"
            with open(chats_path, 'a') as file:
                file.write(welcome_msg + "\n")
            send_messages_to_all(welcome_msg)
            break

        #if only password incorrect
        elif check_username(username):
            print("Bad Password!")
            send_message_to_client(client, "BAD")
            exit(0)
        
        #nothing is right - sign up
        else:
            active_client.append((username, client))
            welcome_msg = f"{datetime.datetime.now()} | SERVER ~ {username} signed up and has entered the chat"
            with open(chats_path, 'a') as file:
                file.write(welcome_msg + "\n")
            send_messages_to_all(welcome_msg)
            with open(cred_path, 'a') as file:
                file.write(username + "|" + password + "\n")
            break


    
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

def main():
    print("go")
    #create socket server object and binding
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try: 
        server.bind((host, port))
        print("The server is up!")

    except: print(f"Unable to bind to host {host} in port {port}")
    
    #to how many we listen
    server.listen(listener_limit)

    while True:
        #accept connection
        client, address = server.accept()
        print(f"Accepted connection from {address[0]}:{address[1]}")

        #create and start thread every time a client connects
        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()