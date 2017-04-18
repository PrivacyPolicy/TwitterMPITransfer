import tweepy
import re

auth = tweepy.OAuthHandler('CdjejuMglmJroi0rcbiVdhDbX',
    'NNjNH7PDTCb2bvoF1Wz3shKTy2LF09AHXKSOyUi7Bn3npxBVeC')

access_token = '3192263874-L20YdVudcRkASLcuG4fSiI01S0prymZ4FS9J0XV'
access_token_secret = 'CE1mT3q8CVYU74PkErvTqw92VB7wWDc3McoW7yuMCWXa4'

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


i = 1
def scrape(term, minID, maxID):
    
    if minID == 0 and maxID == 0:
        # handle initial case
        result = api.search(term, lang='en', rpp=10000)
    else:
        # default case, where min and max ID are given
        result = api.search(term, lang='en', rpp=10000, count=minID, max_id=maxID)

    tweets = []

    for tweet in result:
        try:
            tweetObj = {}
            text = tweet.text
            text = " ".join(filter(lambda x:x[0]!='@', text.split())) # remove @s
            if (text[0:2] == "RT"):
                text = text[3:] # remove RT from beginning of tweet
            text = re.sub(r'http[s]?\:\/\/.+?($|\s)', '', text, flags=re.MULTILINE)
            text = re.sub(r';', '.', text, flags=re.MULTILINE)
            
            tweetObj["text"] = str(text)
            tweetObj["id"] = tweet.id
            tweetObj["retweets"] = tweet.retweet_count
            tweetObj["user"] = str(tweet.user.name)
            try:
                tweetObj["favorites"] = tweet.retweeted_status.favorite_count
            except AttributeError:
                tweetObj["favorites"] = 0
                
            # id;sentiment;retweets;favorites;username;text
            tweets.append(str(tweetObj["id"]) + ";0;" + str(tweetObj["retweets"]) \
                + ";" + str(tweetObj["favorites"]) + ";" + tweetObj["user"] + ";" \
                + tweetObj["text"])
            # print(i, str(text), tweet.id, tweet.retweet_count, tweet.user.name, tweet.favorite_count, '\n')
        except UnicodeEncodeError:
            print("No text data; ignoring")
    
    return tweets
    
   
#def main():
#    print(scrape('donald trump', 600000000000000000, 890000000000000000))
#    
#main()
