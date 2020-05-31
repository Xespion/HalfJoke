import time
import random
from pymongo import MongoClient
import tweepy
import tkinter as tk
from tkinter import *

# * MongoDB url connection
MONGO_URI = 'mongo_url_conecction'
client = MongoClient(MONGO_URI)

# * Twitter Keys
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

# * CONNECTION
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# * Get Data from database
db = client.get_database('HalfJoke')
storedJokes = db.JokeStore
idCol = db.IdColl 

# ? Returns the last id from the database
def retrieve_id():
    lastid = idCol.find()[0]
    return lastid["id"]

# ? Stores the last seen id to the database replacing the last one
def store_id(last_seen_id):
    lid = {"num": 1}
    sid = {"$set": {"id" : last_seen_id}}
    idCol.update_one(lid, sid)
    return

# ? Reply to tweets depending on the command
def reply_to_tweets():
    print('Retrieving and replying to tweets...', flush=True)
    last_seen_id = retrieve_id()
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        last_seen_id = mention.id
        store_id(last_seen_id)
        #Dual Case
        if '#sg' in mention.full_text.lower() and '#hj' in mention.full_text.lower():
            print('found too many things', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    ' Could you please decide if you want mah jokes or your suggestions mate?' , mention.id)
        #Halfjokes
        elif '#hj' in mention.full_text.lower():
            print('found #hj!', flush=True)
            print('responding back...', flush=True)
            count = storedJokes.count_documents({})
            hjoke = storedJokes.find()[random.randrange(count)]
            api.update_status('@' + mention.user.screen_name +
                    ' ' + hjoke["joke"], mention.id)
        #Suggestions
        elif '#sg' in mention.full_text.lower():
            print('found #sg!', flush=True)
            print('responding back and storing tweet...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    ' Thankies nya!', mention.id)
                    
            tweet = mention.full_text.split(' ')
            text = ''

            for word in tweet:
                if '@' not in word and '#' not in word:
                    text = text + word + ' '

            new_joke = {
                'id': mention.id,
                'joke':  text
            }
            storedJokes.insert_one(new_joke)

# * Variables used to store tweets
wtweet = ' '
wtweet02 = ' '
search = ' '

# ? Posts a written tweet to the feed of the bot
def post_tweet():
    global wtweet
    wtweet = entry.get()
    api.update_status(wtweet)

# ? Posts tweet
def post_tweet02(posted):
    api.update_status(posted)

# ? Posts the selected tweet from a list
def look_DB():
    global search
    search = '.*' + entry2.get() + '.*'
    ocurrences = storedJokes.find( { 'joke': { '$regex': search } } )

    # ! Registers a double click in the list box
    def OnDouble(event):
        selection=Lb1.curselection()
        posted = Lb1.get(selection[0])
        post01 = Button(top, text = "Post tweet", fg = "red", command = post_tweet02(posted))
        post01.place(x= 50, y= 200)

    top = Toplevel()
    top.geometry("400x250")
    Lb1 = Listbox(top)
    i = 1
    # ! Add ocurrences of the search to the listbox
    for o in ocurrences:
        Lb1.insert(i, o["joke"])
    Lb1.bind("<Double-Button-1>", OnDouble)
    Lb1.pack(padx=10,pady=10,fill=tk.BOTH,expand=False)
    top.mainloop()

# * Main Window
root = tk.Tk()
root.geometry("250x250")

# * Frame for bot signature function
frame01 = Frame(root)
frame01.pack()
turn = Button(frame01, text = "Execute Bot", fg = "red", command = reply_to_tweets)
turn.pack( side = LEFT)

# * Entry to post an  original tweet
entry = tk.Entry(root)
entry.place(x=50, y=50)
post = Button(root, text = "Post tweet", fg = "red", command = post_tweet)
post.place(x = 50, y= 75)

# * Entry to search a tweet in the database 
entry2 = tk.Entry(root)
entry2.place(x=50, y=120)
post = Button(root, text = "Search Tweet", fg = "red", command = look_DB)
post.place(x = 100, y= 150)
root.mainloop()
