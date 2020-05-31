# HalfJoke
HalfJoke bot written in Python, that uses MongoDB as storage for tweets. 

**Twitter URL:** 
https://twitter.com/HalfJokeBot

## Database
I have used MongoDB and I created 2 main collections. The first one called Jokes stores documents that have an id that resembles the id given to a certain tweet and a text value that stores the tweet.
The second collection stores only one document that stores the id of the last tweet that the bot has dealt with, so whenever it looks through the mentions it does not count the ones that it has already answered.

## Commands
**#hj**
With this hashtag you tell the bot to reply to your mention into its feed with a half joke that is selected randomly within the database.

**#sg** 
With this hashtag you tell the bot to store the rest of the text in the mention to the database so it can use it later.

I also implemented a GUI made with Tktinter. However that is not the main funcionality of the bot, so it could be completely cut.
