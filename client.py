import socket
import threading
import datetime
import time
import ssl

#varialbes
host = "127.0.0.1"
port = 8000
close_event = threading.Event()  # Event to signal when to close the connection

#listening to the server
def listen_for_msg_from_server(client):
    #while connected
    while not close_event.is_set():
        message = client.recv(2048).decode("UTF-8")
        #if message is empty
        if message != "":
            #if the credentials are wrong
            if message == "BAD": 
                print("Bad Credentials, Ended Connection")
                close_event.set()  #signal to close the connection
                client.close()
                break  #exit the function to stop receiving further messages
            else:
                username = message.split("~ ")[0].split("| ")[1]
                content = message.split("~ ")[1]
                print(f"{datetime.datetime.now()} | {username} ~ {content}")
        else:
            print("Ending Connection... ")
            close_event.set()  #signal to close the connection
            client.close()
            break  #exit the function to stop receiving further messages

def send_msg_to_server(client):
    while not close_event.is_set():
        time.sleep(0.05)
        if close_event.is_set(): break
        message = input("Message: ")
        if message != "":
            client.sendall(message.encode("UTF-8"))
        else: 
            print("Message is empty")

def communicate_to_server(client):
    username = input("Enter username: ")
    password = input("Enter Password: ")
    if username != "" and password != "":
        #send username with password
        client.sendall(f"{username}*****{password}".encode("UTF-8"))
    else:
        print("username or password can't be empty!")
        client.close()
        exit(0)
    #listens then sends
    threading.Thread(target=listen_for_msg_from_server, args=(client, )).start()
    send_msg_to_server(client)


    client.close()  # Close the socket when done
    print("Connection closed.")

def main():
    #create socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #create context
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  
    secure_socket = context.wrap_socket(client, server_side=False, server_hostname="localhost")

    #try to connect to the server
    try: 
        secure_socket.connect((host, port))
        print("Connected!")

    except: print(f"Unable to bind to host {host} in port {port}")
    
    communicate_to_server(secure_socket)

    print("Thanks, See You Soon!")


if __name__ == '__main__':
    main()