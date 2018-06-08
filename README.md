# Simple Chat Server in Python. #

This is a Simple Chat Server in Python that uses TCP to send messages between two clients.

There are 2 files. 

1. server.py - Which is used by the server.
2. client.py - Which is used by the client.

We can start the server in the desired host by using IDLE in Windows or using terminal in Mac/Linux.

$ python server.py

Then we start the client using the command 

$ python client.py

The GUI for the client is developed in Tkinter. Here we can assign the ip address of the server, and the port that is binded by the server program. Then we click the connect button.

Then we change the nickname. If we change the nickname before connecting, it will not reflect in the list of users or show your name in the list of users.

This program also has a canvas in the GUI that allows users to draw in the canvas.

## Future Work Needed. ## 

1. There is no private Chat. All users connected to server can see every message sent by any other user.

2. Canvas is not shared between the users. This will make the chat interactive by creating a doodle like environment shared between the users.

3. Nickname changing before connecting to the server can be implemented.