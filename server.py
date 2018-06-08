#!/usr/bin/python                                                        # This is server.py file

import socket                                                           # Import Socket Module
import thread                                                           # Import Thread Module
import threading
import time
import pickle

def nicknames(c, address):                                              # This thread is used to send the list of all clients in the server every five seconds
        global online
        while True:                                                     # This is a continous loop
                time.sleep(2)                                           # Repeat the process for every 2 seconds
                with lock:                                              # locking mechanism for global variable
                        c.send('2')                                     # Send 2 to say to the client that it sends the nickname next
                        c.send(pickle.dumps(online))                    # Send online dictionary in the form of bytestream

def send(c, address):                                                   # Thread used for sending the data to the clients
        global msg, lock, online
        with lock:
                count = len(msg)                                        # Count is the length of the chat history initially
        while True:
                with lock:
                        for i in range(count, len(msg)):                # Then at each step check the length of the chat history and the count of chat send to the client
                                c.send(msg[i])                          # if not same send the message to the client
                                count += 1                              # Increase the count by 1

def receive(c, address):                                                # Thread created to recieve the messages send by the client
        global msg, lock, canvas
        count = len(msg)                                                # Count initialized to the length of the chat history
        print 'Got connection from', address
        c.send('Thank you for connecting')                              # After getting connected send to the client ACK that it got connected
        while True:
                newmsg = c.recv(1024)                                   # newmsg is the message recieved by the server
                if newmsg != '1' and newmsg != '2':                     # if it is a regular message
                        with lock:
                                msg.append(newmsg)                      # then append ot the server
                                print msg                               # Print the message in the server
                if newmsg == '1':                                       # If the message is 1 then close the connection
                        with lock:
                                del online[address]                     # delete the client from the list of clients
                        c.close()                                       # close the connection
                        break                                           # Break out of the while loop
                if newmsg == '2':                                       # if the newmsg = 2 then the nickname is recieved by the server
                        nickname = c.recv(1024)
                        with lock:
                                online[address] = nickname              # add the client to the list of available clients
                                for i in online:
                                        print i, online[i]              # Print the list of clients in the server

noofConnections = 0                                                     # Vriable for number of clients in the server
listofclients = []                                                      # list of clients in the server
msg = []                                                                # List for storing the Chat History
lock = threading.RLock()                                                # Locking mechanism for synchronizing threads
sock = socket.socket()                                                  # Create a socket
sock.bind(('localhost', 8084))                                         # Bind the socket to the Host address and the Port number
sock.listen(5)                                                          # Listen for incoming connections
online = {}                                                             # Dictionary for the list of clients in the server

while True:
        c, address = sock.accept()                                      # Accept a connection from the client
        listofclients.append(address)                                   # Append the address to the list of clients
        noofConnections+=1                                              # Increase the number of connections by 1
        thread.start_new_thread(receive, (c, address, ))                # Start a new thread for recieving messages
        thread.start_new_thread(send, (c, address, ))                   # Start a new thread for sending messages
        thread.start_new_thread(nicknames, (c, address, ))              # Start a new thread for sending clients names
