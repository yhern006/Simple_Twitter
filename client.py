# Simple Twitter Project
# Socket client
# Author: Yvette Hernandez

import socket	# for sockets
import sys	# for exit

# create an AF_INET, STREAM socket (TCP)
#  socket.socket creates a socket & returns a socket descriptor which can be
#  used in other socket related funcs
try: 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
	sys.exit();

print 'Socket Created'

host = ''
port = 8888

# Connect to remote server
s.connect((host, port))
print 'Socket Connected'


def send_and_receive(data):
	try:
		# Set the whole string
		s.sendall(data)
	except socket.error:
		# Send failed
		print 'Send failed'
		sys.exit()

	# Now receive data
	response = s.recv(4096)
	return response

def offl_mssgs(user):
    while 1:
        print '\n----------------------'
        print '   OFFLINE MESSAGES   '
        print '----------------------'
        print '0. Go Back to Main Menu'
        print '1. See All Messages'
        print '2. See Messages From a Chosen Subscription' 
        menu_choice = raw_input('Enter Choice: ') 
        if menu_choice == '0':
            return
        elif menu_choice == '1':
            to_send = 'OFFL:' + user
            response = send_and_receive(to_send)
            if response == 'None':
                print 'No Offline Messages.\n'
            else:
                print '\nOffline Messages:'
                mssg_list = response.split(':')
                for m in mssg_list:
                    print '  ', m
        elif menu_choice == '2':
            to_send = 'SEE_SUBS:' + user
            response = send_and_receive(to_send)
            current_subs = response.split(':')
            print 'Current Subscriptions:\n'
            for sub in current_subs:
                print '  ', sub
            sub_choice = raw_input('Enter subscription: ')

            to_send = 'OFFL:' + user
            response = send_and_receive(to_send)
            mssg_list = response.split(':')
            print '\nOffline Messages:'
            for m in mssg_list:
                temp = m.split('-')
                temp_usr = temp[0]
                temp_usrlen = len(temp_usr) - 1
                if temp_usr[:temp_usrlen] == sub_choice:
                    print '  ', m

def edit_subs(user):
    while 1:
        print '\n----------------------'
        print '  Edit Subscriptions  '
        print '----------------------'
        print '0. Go Back to Main Menu'
        print '1. Add Subscription'
        print '2. Drop Subscription'
        print '3. View Current Subscriptions'

        menu_choice = raw_input('Enter choice: ')
        if menu_choice == '0':
            return
        elif menu_choice == '1':
            while 1:
                sub_to_add = raw_input('Enter Subscription to Add: ')
                to_send = 'SUB_ADD:' + user + ':' + sub_to_add
                response = send_and_receive(to_send)
                print response
                if response == 'Subscription Added!':
                    break
        elif menu_choice == '2':        ## DROP SUB
            to_send = 'SEE_SUBS:' + user
            response = send_and_receive(to_send)
            current_subs = response.split(':')

            for s in current_subs:
                print '  ' + s

            sub_to_drop = raw_input('Enter Subscription to Drop: ')
            to_send = 'SUB_DROP:'+ user + ':' + sub_to_drop
            response = send_and_receive(to_send)
            print response	## 'Sub dropped!'
        elif menu_choice == '3':
            to_send = 'SEE_SUBS:' + user  
            response = send_and_receive(to_send)
            current_subs = response.split(':')
            for s in current_subs:
                print '  ' + s

def post_message(user):
    while 1:
        print '\n--------------------'
        print '   POST A MESSAGE   '
        print '--------------------'
        print '0. Go Back to Main Menu'
        print '1. Continue'

        menu_choice = raw_input('Enter choice: ')
        if menu_choice == '0':
            return
        else:
            while 1:
                post = raw_input('Enter Post (<= 140 characters, 0 to cancel): ')
                if post == '0':
                    break
                hashtags = raw_input('Enter Hashtags separated by space(0 for none)')
                if len(post) <= 140:
                    if hashtags != '0':
                        #tags_str = combine_hashtags(hashtags)
                        to_send = 'POST:' + user + ':' + post + ':' + hashtags
                    else:
                        to_send = 'POST:' + user + ':' + post + ':none'
                    response = send_and_receive(to_send)
                    print response
                    break
                else:
                    print 'Post must be less than 140 characters. Try again.'
## end

def hashtag_search(user):
    while 1:
        print '\n--------------------'
        print '   HASHTAG SEARCH   '
        print '--------------------'
        print '0. Go Back to Main Menu'
        print '1. Continue...'
        
        menu_choice = raw_input('Enter choice: ')
        if menu_choice == '0':
            break
        else:
            hashtag = raw_input('Enter hashtag to search: ')
            if hashtag[0] != '#':
                hashtag = '#' + hashtag
            to_send = 'HASH:' + user + ':' + hashtag
            response = send_and_receive(to_send)

            mssg_list = response.split(':')
            print '\nMessages with', hashtag
            for mssg in mssg_list:
                print '  ', mssg

def display_realtime_mssgs(user):
    to_send = 'REALTIME:' + user
    response = send_and_receive(to_send)
    if response == 'None':
        print '\nNo New Messages'
        return
    else:
        print '\nNew Messages:'
        realtime_mssgs = response.split(':')
        for mssg in realtime_mssgs:
            print '  ', mssg
        #print 'end display'

def logout(user):
    to_send = 'LOGOUT:' + user  ## CHANGED
    response = send_and_receive(to_send)
    print response

def view_menu():
	print '\n--------------------'
	print '      MAIN MENU     '
	print '--------------------'
	print '1. See Offline Messages'
	print '2. Edit Subscriptions'
	print '3. Post a Message'
	print '4. Hashtag Search'
	print '5. Logout'

def login():
    prompt = 1
    while prompt:
	    # prompt user for username and password
        username = raw_input('Username: ')
        password = raw_input('Password: ')

        login = "LOGIN:" + username + ':' + password
        reply = send_and_receive(login)
        print '\n'
        print reply
        if reply[0:7] != 'Invalid':
            prompt = 0
    return username

message = 'Entering'
reply = send_and_receive(message)

while 1:
    user = login()
    menu = 1
    while menu:
        display_realtime_mssgs(user)
        view_menu()
        menu_choice = raw_input('Enter choice: ')

        if menu_choice == '0':
            menu = 0
        elif menu_choice == '1':
            offl_mssgs(user)
        elif menu_choice == '2':
            edit_subs(user)
        elif menu_choice == '3':
            post_message(user)
        elif menu_choice == '4':
            hashtag_search(user)
        elif menu_choice == '5':
            logout(user)
            menu = 0
        else:
            menu = 0

s.close()	# close socket

