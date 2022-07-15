# flask-socketio

An authenticated feed system using Flask and Socket.IO  

## NOTE:

The Socket IO implementaion won't work on the deployed URL as Deta does not support web sockets and socket io.
This is mentioned in their [documentation](https://docs.deta.sh/docs/micros/about#important-notes) (point no.12) this can be run locally using the below steps. 

## Installation

1. Run `pip install requirements.txt` to install the dependencies  
2. Run `python main.py` to start the server

## Steps to test out

1. Go to /register to register an account
2. Go to /login to login as the user
3. You will be redirected to the chat area! 
