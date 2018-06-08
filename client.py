#!/usr/bin/python                                                # This is client.py file

import socket                                                    # Import socket module
from Tkinter import *                                            # Import Graphics library
import thread                                                    # Import thread library
import time
from ScrolledText import ScrolledText
import pickle
import os

top = Tk()                                                      # Creates a window
top.title("Chat Server")                                        # Set title to the window
frame = Frame( top , width = 1280 , height = 640 )              # Create a frame
frame.pack()
host = "localhost"                                             # Set the Server IP address
port = 8084                                                     # Set the Sert Port number
nickname = "Change your nickname"                               # Set the nickname
message = ''                                                    # Global variable for mesage
s = socket.socket()                                             # Create a socket object
lastx, lasty = 0, 0                                             # global values for drawing on canvas
connect = 0


def send_message():                                             # function or thread to send message on clicking send button
    global message,s,nickname,message,MESSAGE
    message = MESSAGE.get()                                     # Get the text from the Entry widget and assign it to the message
    message = nickname + ": " + message                         # Add nickname to the message
    MESSAGE.delete(0,100)                                       # After sending the message delete the text in the Entry widget
    s.send(message)                                             # Send messsage to the server through the socket created


def create_connection():                                        # Create the connection on clicking the connect button

    global host,port,s,connect

    s.connect((host, port))                                     # Connect to the given host and port
    print s.recv(1024)                                          # Acknowledge from the server
    s.send('2');                                                # Sending Server the Nickname
    s.send(nickname)
    connect = 1
    thread.start_new_thread( see_for_text , () )                # Start a thread for recieving the messages sent by the server

def destroy_connection():                                       # Close the socket on clicking Disconnect Button
        global s
        s.send('1')                                             # Send 1 to say that the connection is closed
        s.close                                                 # Connection Closed


def change_server():                                            # Change the IP Address of the Server from GUI

    global host,port,DETAILS

    def change_IP():                                            # Changes the IP address of the server to connect

        global host , port

        host = E1.get()                                         # Get the value of the IP Address from the Entry Widget and assign it to host
        print "Server Address is " , host
        print "Port is ",port
        DETAILS.delete(0,100)
        DETAILS.insert(1,"SERVER IP               : " + host )
        DETAILS.insert(2,"SERVER PORT        : " + str(port) )
        DETAILS.insert(3,"NICK NAME IS       : " + nickname )
        H.destroy()                                             # Destroy the window

    H = Tk()
    H.title("IP Address")
    L1 = Label( H , text = "Server Address" )                   # Defines the label named Server Address
    L1.pack( side = LEFT )                                      # Put the label on left side
    E1 = Entry( H , bd = 15 )                                   # Define an Entry widget of size 15
    E1.pack()
    B1 = Button( H , text = "Change" , command = change_IP )    # Button to Change the IP Address When clicked the Button
    B1.pack( side = RIGHT )                                     # Pack the button on the RIGHT side

def change_port():                                              # Function to Change the Port number

    global host,port,DETAILS

    def change():                                               # Function

        global host , port

        print "Entering"
        port = int(E1.get())                                    # Get the value of port of the server to be connected
        print "Server Address is ", host
        print "Port is " , port
        DETAILS.delete(0,100)
        DETAILS.insert(1,"SERVER IP               : " + host )
        DETAILS.insert(2,"SERVER PORT        : " + str(port) )
        DETAILS.insert(3,"NICK NAME IS       : " + nickname )
        H.destroy()                                             # Destroy the window

    H = Tk()
    H.title("Port number")
    L1 = Label( H , text = "Port" )                             # Label named Port
    L1.pack( side = LEFT )                                      # Packed on the Left side
    E1 = Entry( H , bd = 15 )                                   # Entry Widget of size 15 to enter Port number
    E1.pack()
    B1 = Button( H , text = "Change" , command = change )       # Button to call the function change() on clicking
    B1.pack( side = RIGHT )                                     # Pack the button on the right side

def change_nickname():                                          # Function to Change the Nickname

    global nickname,s , connect

    def change():                                               # Function which changes and sends the server about the change of the nickname

        global nickname,s,DETAILS

        nickname = E1.get()                                     # Gets the nickname from the Entry Widget
        print "Server Address is ", host
        print "Port is " , port
        print "Nickname is ",nickname
        if connect == 1:                                        # If the client is connected to the server then
            s.send("2")                                         # Send 2
            s.send(nickname)                                    # To show that the next sending statement is the nickname
        DETAILS.delete(0,100)
        DETAILS.insert(1,"SERVER IP               : " + host )
        DETAILS.insert(2,"SERVER PORT        : " + str(port) )
        DETAILS.insert(3,"NICK NAME IS       : " + nickname )
        H.destroy()                                             # Destroy the window

    H = Tk()
    H.title("Nickname")                                  # Change the title bar name
    L1 = Label( H , text = "Nick name" )
    L1.pack( side = LEFT )                                      # Pack the label to the LEFT side
    E1 = Entry( H , bd = 15 )                                   # Entry field of size 15 to enter the nickname
    E1.pack()
    B1 = Button( H , text = "Change" , command = change )       # Click the button to call the change function
    B1.pack( side = RIGHT )                                     # Pack the button to the RIGHT side

def see_for_text():                                             # Thread created for recieving the data continously
    global s,DISPLAY,LIST,CANVAS
    while True:                                                 # Goes infinitely
        msg = s.recv(1024)
        if msg == '1':                                          # If the receieved message is 1 then server is saying it'sclosing the connection
            s.close
        elif msg == '2':                                        # If the msg is 2 we are recieving the list of users that are available online
            i = 1
            online = pickle.loads(s.recv(1024))                 # Pickle converts the bytestream back to dictionary
            LIST.delete(0,100)                                  # Delete the elements in the list box
            LIST.insert(1,"     List of Users    ")
            for j in online:                                    # List the elements in the list box
                LIST.insert(i+1,"\t"+str(i) + ". " + online[j])
                i += 1
        else:
            print msg
            DISPLAY.insert(END,"\n"+msg);                       # If it is the normal message print it in the Srolled Text Widget

def xy(event):                                                  # Locating the x,y position in the canvas
    global lastx, lasty
    lastx, lasty = event.x, event.y

def addLine(event):                                             # Drawing line in the canvas based on mouse drag
    global lastx, lasty,CANVAS
    CANVAS.create_line((lastx, lasty, event.x, event.y))
    lastx, lasty = event.x, event.y

def clear_canvas():                                             # Function used to clear the Canvas fully
    global CANVAS
    CANVAS.delete(ALL)                                          # Clears the canvas and make it white


C_B = Button( top , text = "Connect" , command = create_connection )                    # Button to create connection
HOST = Button( top , text = "Server", command = change_server )                         # Button to change server IP Address
PORT = Button( top , text = "Port", command = change_port )                             # Button to change Port number of the server
NICK = Button( top , text = "Nickname" , command = change_nickname );                   # Button to change the nickname of the client
SEND = Button( top , text = "Send" , command = send_message );                          # Button to send the message to the server
DISCONNECT = Button( top , text = "Disconnect" , command = destroy_connection );        # Button to disconnect from the server
MESSAGE = Entry( top , width = 50 )                                                     # Entry to type the message to send
DISPLAY = ScrolledText(top, height = 15 , width = 50 )                                  # Display the Message recieved in the Scrolled Tet Widget
LIST = Listbox(top)                                                                     # List box to print the people available on the server
CANVAS = Canvas(top , height = 200 , width = 150 , bg = "white" )                       # Canvas to Draw some pictures
LIST.insert(1,"\tList of Users")                                                        # Insert the List of users field in the List Box
RESET = Button( top, text = "RESET" , command = clear_canvas )                          # Button to reset the canvas
DETAILS = Listbox(top)
DETAILS.insert(1,"SERVER IP               : " + host )
DETAILS.insert(2,"SERVER PORT        : " + str(port) )
DETAILS.insert(3,"NICK NAME IS       : " + nickname )

CANVAS.grid(column=0, row=0, sticky=(N, W, E, S))                                       # Declaring the Canvas Grid
CANVAS.bind("<Button-1>", xy)                                                           # Binding mouse click to the xy function
CANVAS.bind("<B1-Motion>", addLine)                                                     # Binding the mouse drag with addLine function


C_B.place(  x = 40 , y = 400 , width = 100)                                             # Placing the widgets properly
HOST.place( x = 140 , y = 400 , width = 100 )
PORT.place( x = 240 , y = 400 , width = 100 )
NICK.place( x = 340 , y = 400 , width = 100 )
SEND.place( x = 440 , y = 300 , width = 100 )
DISCONNECT.place( x = 440 , y = 400 , width = 100 )
MESSAGE.place( x = 40 , y = 300 )
DISPLAY.place( x = 40 , y = 40 )
LIST.place( x = 580 , y = 40 , width = 280 , height = 200)
CANVAS.pack( expand = YES, fill = BOTH )
CANVAS.place( x = 880 , y = 40 , width = 400 , height = 400 )
RESET.place( x = 880 , y = 450 , width = 400)
DETAILS.place( x = 580 , y = 300 , width = 280 , height = 140 )
top.mainloop()                                                                          # Running the window in a loop
