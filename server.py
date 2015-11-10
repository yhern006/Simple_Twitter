# Simple Twitter Project
# Server side
# Author: Yvette Hernandez

import socket
import sys
from thread import *
from helper import get_reply

HOST = '' 	        # Symbolic name meaning all available interfaces
PORT = 8000         # Arbitrary non-priveleged port

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


def clientthread(conn):
    ''' Function for handling connections. This will be used
        to create threads
    '''

	# Sending message to connected client
    conn.send('Welcome to the server.\n')

    # infinite loop so that func does not terminate and thread does not end
    while True:
		# Receiving from client
        data = conn.recv(1024)
        reply = get_reply(data)     # get reply from helper functions
        if not data:
            break
        conn.sendall(reply)

    # came out of loop
    conn.close()

threads =[]
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
