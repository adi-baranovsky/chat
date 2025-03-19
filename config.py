import threading

#variables
host = "127.0.0.1" #host
port = 8000 #port
listener_limit = 5
active_client = [] #all currently connected users
cred_path = r"C:\Users\kyoto\Documents\GitHub\FirstPython\chat\password.txt" #path for credentials file
chats_path = r"C:\Users\kyoto\Documents\GitHub\FirstPython\chat\chats.txt" #path for chat history file
close_event = threading.Event()  # Event to signal when to close the connection
