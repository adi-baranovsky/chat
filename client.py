import socket
import threading
import datetime
import time

#varialbes
host = "127.0.0.1"
port = 8000
close_event = threading.Event()  # Event to signal when to close the connection

def listen_for_msg_from_server(client):
    while True:
        message = client.recv(2048).decode("UTF-8")
        #print("got message! " + message)
        if message != "":
            if message == "BAD": 
                print("Bad Credentials, Ended Connection")
                close_event.set()  # Signal to close the connection
                break
            else:
                #print("printing the message!")
                username = message.split("~ ")[0].split("| ")[1]
                content = message.split("~ ")[1]
                print(f"{datetime.datetime.now()} | {username} ~ {content}")
        else:
            print("message from server is empty")

def send_msg_to_server(client):
    while not close_event.is_set():
        time.sleep(0.05)
        message = input("Message: ")
        if message != "":
            client.sendall(message.encode("UTF-8"))
        else: 
            print("Message is empty")
            send_msg_to_server(client)    

def communicate_to_server(client):
    username = input("Enter username: ")
    password = input("Enter Password: ")
    if username != "" and password != "":
        #send username with password
        client.sendall(f"{username}*****{password}".encode("UTF-8"))
    else:
        print("username or password can't be empty!")
        exit(0)
    #listens then sends
    threading.Thread(target=listen_for_msg_from_server, args=(client, )).start()
    send_msg_to_server(client)


    client.close()  # Close the socket when done
    print("Connection closed.")

def main():
    #create socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #try to connect to the server
    try: 
        client.connect((host, port))
        print("Connected!")

    except: print(f"Unable to bind to host {host} in port {port}")
    
    communicate_to_server(client)

    print("Thanks, See You Soon")


if __name__ == '__main__':
    main()