# Simple Twitter Project
# Server side
# Author: Yvette Hernandez

import socket
import sys
from thread import *
import server_help

## Hard-coded Values
## =========================================================================
threads = []
users = {'Yvette': 'nachos', 'abc':'123', 'potato': 'sack', 'Alice':'beep'}
# unread = {'Yvette': 3, 'abc':1, 'potato':0, 'Alice': '5'}
log_status = {'Yvette': 0, 'abc': 0, 'potato': 0, 'Alice': 0}
user_index = {'Yvette': 0, 'abc': 1, 'potato': 2, 'Alice': 3}
usr_msg0 = ['Hello world!', 'My name is Yvette~', 'Nachos!', 'Beep']
usr_msg1 = []
usr_msg2 = ['POtaTOEs']
usr_msg3 = ['Hello Bob', 'I am cool.']
subs0 = ['potato', 'Alice']	# Yvette's subscriptions
subs1 = ['potato']	# abc's subs
subs2 = ['abc']	# potato's subs
subs3 = ['Yvette', 'potato', 'abc']	# Alice's subs
## =========================================================================

HOST = '' 	# Symbolic name meaning all available interfaces
PORT = 8888	# Arbitrary non-priveleged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

# 'bind' can be used to bind a socket to a particular address and port
#	it needs a sockaddr in structure similar to connect func
try:
	s.bind((HOST, PORT))
except socket.error, msg:
	print 'Bind failed. Error Code: ' + str(msg[0]) + 'Message ' + msg[1]
	sys.exit()

print 'Socket bind complete'

s.listen(10)	# puts socket in listening mode
print 'Socket now listening'

list_of_subs = []       # list of lists
list_of_usr_mssgs = []  # list of lists
offl_mssgs = []         # list of lists
realtime_mssgs = []     # list of lists
all_mssgs = []          # list

for i in range(4):
    offl_mssgs.append([])
    realtime_mssgs.append([])

list_of_subs.append(subs0)
list_of_subs.append(subs1)
list_of_subs.append(subs2)
list_of_subs.append(subs3)
list_of_usr_mssgs.append(usr_msg0)	
list_of_usr_mssgs.append(usr_msg1)	
list_of_usr_mssgs.append(usr_msg2)	
list_of_usr_mssgs.append(usr_msg3)	


for u, p in users.items():
    # print 'user: ', u
    load_offl_mssgs(u)

    
# Function for handling connections. This will be used to create threads
def clientthread(conn):
	# Sending message to connected client
	#  send only takes string
    conn.send('Welcome to the server.\n')

    # infinite loop so that func does not terminate and thread does not end
    while True:
		# Receiving from client
        data = conn.recv(1024)
        reply = get_reply(data)
        if not data:
            break
        conn.sendall(reply)

    # came out of loop
    conn.close()

# now keep talking with the client
while 1:
	# wait to accept a connection - blocking call
	#  conn is a new socket usable on send and receive data
    conn, addr = s.accept()

	# add conn to list of threads
    threads.append(conn)

	# display client information
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

	# start new thread takes 1st arg as a func name to be run,
	#  second is the tuple of args to the func
    start_new_thread(clientthread, (conn,))

s.close()


