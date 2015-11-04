# Simple Twitter Project
# Helper functions for server.py
# Author: Yvette Hernandez


def get_usr_index(usr):
    return user_index[usr]

def get_usr_key(value):
    for key, val in user_index.items():
        if val == value:
            return key

def get_usr_subs(usr):
    ''' Returns a list of subscriptions '''
    usr_index = get_usr_index(usr)
    return list_of_subs[usr_index]

def get_usr_subscribers(usr):
    ''' Returns a list of subscribers '''
    list_of_subscribers = []
    index = 0
    for subscriber in list_of_subs:
        for subsrp in subscriber:
            if subsrp == usr:
                subscriber_name = get_usr_key(index)
                list_of_subscribers.append(subscriber_name)
        index = index + 1
    return list_of_subscribers
    
# first check who are user's subs, then load subs onto offl_mssgs
def load_offl_mssgs(usr):
    usr_index = get_usr_index(usr)
    offl_mssgs[usr_index] = []      # empty past offl mssgs
	
    usr_subs = get_usr_subs(usr)
    for l in usr_subs:
        sub_index = get_usr_index(l)
        for sub_mssg in list_of_usr_mssgs[sub_index]:
            temp = l + " - " + sub_mssg
            offl_mssgs[usr_index].append(temp)

def get_unread_count(usr):
    usr_index = get_usr_index(usr)
    return len(offl_mssgs[usr_index])
    
def copy_list(list_to_copy):
    new_list = list_to_copy[:]
    return new_list

def clear_offl_mssgs(usr, sub):
    ''' Clears offline messages from a specific subscription '''
    usr_index = get_usr_index(usr)
    temp_offl_list = copy_list(offl_mssgs[usr_index])
  
    if len(temp_offl_list) == 0:
        return
    else: 
        for mssg in temp_offl_list:
            curr_offl_mssg = mssg.split(' - ')
            curr_offl_sub = curr_offl_mssg[0]
            if curr_offl_sub == sub:
                offl_mssgs[usr_index].remove(mssg)

def update_offl_mssgs(usr, sub, mssg):
    usr_index = get_usr_index(usr)
    offl_mssg = sub + ' - ' + mssg
    offl_mssgs[usr_index].append(offl_mssg)
    return
    
def update_all_mssgs(usr, post):
    mssg = usr + ' - ' + post
    all_mssgs.append(mssg)

def update_realtime_mssgs(usr, sub, post):
    ''' adds post to user's realtime list based on subscription '''
    usr_index = get_usr_index(usr)
    mssg = sub + ' - ' + post
    realtime_mssgs[usr_index].append(mssg)

def send_realtime_mssgs(usr):
    usr_index = get_usr_index(usr)
    # go through realtime_mssgs list
    reply = ''
    if len(realtime_mssgs[usr_index]) == 0:
        return 'None'
    else:
        for mssg in realtime_mssgs[usr_index]:
            reply = reply + ':' + mssg
        return reply[1:]
        
def clear_realtime_mssgs(usr, sub):
    usr_index = get_usr_index(usr)
    temp_list = copy_list(realtime_mssgs[usr_index])
    
    if len(temp_list) == 0:
        return
    else:
        for mssg in temp_list:
            curr_mssg = mssg.split(' - ')
            curr_sub = curr_mssg[0]
            if curr_sub == sub:
                realtime_mssgs[usr_index].remove(mssg)
    return

def check_login(username, password):
    if users.has_key(username):
        if users[username] == password:
            log_status[username] = 1
            print 'Logged in: ' + username
            unread_mssgs = get_unread_count(username)
            
            if unread_mssgs == -1:	# user DNE || wrong pswrd
                reply = 'Invalid username or password. Try again.'
            else:
                reply = 'Welcome ' + username + '! You have '
                reply = reply + str(unread_mssgs) + ' unread messages'
        else:
            reply = 'Invalid username or password. Try again.'
    else:
        reply = 'Invalid username or password. Try again.'
    return reply
    
def get_hashtags(mssg):
    ''' gets tags from mssg and returns a list'''
    mssg_list = mssg.split(':')
    tags_str = mssg_list[1]
    if tags_str == 'none':
        return []
    else:
        tags_list = tags_str.split(' ')
        return tags_list

def post_message(user, post, tags):
    ''' Post real time if users are logged in
        Post offl if users not logged in '''
    if tags == 'none':
        mssg = post
    else:
        #new_tags = separate_hashtags(tags)
        mssg = post + ' ' + tags
    update_all_mssgs(user, post + ':' + tags)
    # Go through user's subscribers
    subscribers = get_usr_subscribers(user)
     
    for s in subscribers:
        if log_status[s] == 0:
            update_offl_mssgs(s, user, mssg)
        else:
            update_realtime_mssgs(s, user, mssg)
    return
    
def hashtag_search(user, hashtag):
    reply = ''
    if len(all_mssgs) == 0:
        return 'No Hashtags.'

    count = 0
    for mssg in all_mssgs:
        tags_list = get_hashtags(mssg)
        if len(tags_list) != 0:
            for tag in tags_list:
                if tag == hashtag and count < 10:
                    mssg_to_send = mssg.replace(':', ' ')
                    reply = reply + ':' + mssg_to_send
                    count = count + 1    
    return reply[1:]

def handle_subscriptions(data):
    temp_list = data.split(':')
    temp_user = temp_list[1]

    if data[0:7] == 'SUB_ADD':
        sub_to_add = temp_list[2]
        if users.has_key(sub_to_add):
            lggdin_usr_idx = get_usr_index(temp_user)
            list_of_subs[lggdin_usr_idx].append(sub_to_add)
            reply = 'Subscription Added!'
        else:
            reply = 'Invalid Subscription. Try again.'
    else:               ## SUB_DROP
        sub_to_drop = temp_list[2]
        lggdin_usr_idx = get_usr_index(temp_user)
        list_of_subs[lggdin_usr_idx].remove(sub_to_drop)
        clear_offl_mssgs(temp_user, sub_to_drop)
        reply = 'Subscription Dropped!'
    return reply
    
def get_offl_mssgs(user):
    usr_index = get_usr_index(user)
    if len(offl_mssgs[usr_index]) == 0:
        reply = 'None'
    else:
        reply = ''
        for m in offl_mssgs[usr_index]:
            reply = reply + ":" + m	
        reply = reply[1:]
    return reply

def logout_user(user):
    log_status[user] = 0
    user_subs = get_usr_subs(user)
    for sub in user_subs:
        clear_offl_mssgs(user, sub) 
        clear_realtime_mssgs(user, sub)
    return 'Logged Out\n'
    
def get_reply(data):
    if data[0:12] == 'Send to all:':
	    # send to all connections
        for t in threads:
            t.sendall(data[12:])
        reply = 'Sent to all!'
    elif data[0:5] == 'LOGIN':
        login_list = data.split(':')
        login_user = login_list[1]
        login_pass = login_list[2]
        reply = check_login(login_user, login_pass)
    elif data[0:6] == 'LOGOUT':
        temp_list = data.split(':')
        temp_user = temp_list[1]
        reply = logout_user(temp_user)
    elif data[0:8] == 'SEE_SUBS':
        temp_list = data.split(':')
        temp_user = temp_list[1]
        user_subs = get_usr_subs(temp_user)
        reply = ''
        for s in user_subs:
            reply = reply + ':' + s 
        reply = reply[1:]
    elif data[0:4] == 'OFFL':
        temp_list = data.split(':')
        temp_user = temp_list[1]
        reply = get_offl_mssgs(temp_user)
    elif data[0:3] == 'SUB':
        reply = handle_subscriptions(data)
    elif data[0:4] == 'POST':
        temp_list = data.split(':')
        temp_user = temp_list[1]
        temp_post = temp_list[2]
        temp_tags = temp_list[3]
        post_message(temp_user, temp_post, temp_tags)
        reply = 'Post posted!'
    elif data[0:4] == 'HASH':
        temp_list = data.split(':')
        temp_user = temp_list[1]
        temp_tag = temp_list[2]
        reply = hashtag_search(temp_user, temp_tag)
    elif data[0:8] == 'REALTIME':   # send realtime_mssgs list as str
        temp_list = data.split(':')
        temp_user = temp_list[1]
        reply = send_realtime_mssgs(temp_user)
        print reply
    else:
        reply = 'OK...' + data
    return reply
    

