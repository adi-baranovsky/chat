
cred_path = r"C:\Users\kyoto\Documents\GitHub\FirstPython\chat\password.txt"
import datetime

"""
def check_password(username, password):
    while True:
        with open(cred_path, "r") as accounts_file:
            for line in accounts_file:
                file_username, file_password = line.replace("\n","").split("|")
                if file_username == username and file_password == password:
                    return True
            return False
print()
print()
if check_password("adi", "34"):
    print("yes!")
else:
    print("oof")
"""
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
#haneling client
def client_handler(username, password):
    #listen for client message that conatins username
    while True:
        #cred = client.recv(2048).decode("UTF-8")

#        username = cred.split("|")[0]
#        password = cred.split("|")[1]

        #if usernameand password are right
        if check_cred(username, password):
            active_client.append((username))
            print("printing active client")
            print(active_client)
            welcome_msg = f"{datetime.datetime.now()} | SERVER ~ {username} has entered the chat"
            print("send_messages_to_all welcome")
            break

        #if only password incorrect
        elif check_username(username):
            print("Bad Password!")
            print("send_message_to_client of bad pass")
            exit(0)
        
        #nothing is right - sign up
        else:
            #send_messages_to_all(client, f"{datetime.datetime.now()} | SERVER ~ {username} signed up and has entered the chat")
            print("send_message signup")
            active_client.append((username))
            with open(cred_path, 'a') as file:
                file.write(username + "\n")
            break
    
    print("create thread")


#server:
active_client = []
user="adi"
password="34"
client_handler(user, password)




