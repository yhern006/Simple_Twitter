# Simple_Twitter

An implementation of a simple Twitter application. It has two main parts: 
a client and server.

## Client Side Functionalities

Users use clients to share tweets and see the tweets of the other users 
they subscribe to.

First, the user is asked for their username and password.
A welcome message is displayed if login credentials are correct, and the 
number of unread offline messages is displayed.

Realtime messages are displayed when a user's subscription posts a message 
when the user is logged in.

1. Offline Messages
A user can see any messages that were sent when they were offline.

2. Edit Subscriptions
A user can add, drop and view current subscriptions.

3. Post a Message
A user can post a message.

4. Hashtag Search
A user can search for the last 10 tweets containing a specific hashtag. 

5. Logout
When a user logs out, their offline and realtime messages are cleared.

## Server Side

The server is responsible for authenticating the users, getting their tweets 
from them, and sending those tweets to other users. Nothing is stored 
locally in the clients since all the information is received from the 
server.

When a user posts a message, the server checks if the user's subscribers 
are logged in. If they are, the post is stored in the subscriber's realtime 
messages list. If the subscribers are offline, the post is store in their offline 
messages list.

## Source Files

client.py - handles client side
server.py - handles server side sockets
helper.py - includes server's helper functions

