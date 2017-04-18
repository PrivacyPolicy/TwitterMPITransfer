import tweepy
import re

# from tweepy import API

auth = tweepy.OAuthHandler('CdjejuMglmJroi0rcbiVdhDbX',
    'NNjNH7PDTCb2bvoF1Wz3shKTy2LF09AHXKSOyUi7Bn3npxBVeC')

# try:
#     redirect_url = auth.get_authorization_url()
#     print(redirect_url)
# except tweepy.TweepError:
#     print ('Error!@ failed to get request token')

# session.set('request_token', auth.request_token)

# verifier = input('Verifier:')
#
# try:
#     auth.get_access_token(verifier)
#     print ('x_token: ', auth.access_token)
#     print ('x_token: ', auth.access_token_secret)
# except tweepy.TweepError:
#     print ('Error! Failed to get access token.')

access_token = '3192263874-L20YdVudcRkASLcuG4fSiI01S0prymZ4FS9J0XV'
access_token_secret = 'CE1mT3q8CVYU74PkErvTqw92VB7wWDc3McoW7yuMCWXa4'

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet)

# for i in range(1, 10):
i = 1
if True:                                                          #         853808734421889024
    result = api.search('donald trump',lang='en',rpp=10, count=5, max_id=852808734421889024) #, max_id=853803997282484224

    for tweet in result:
        try:
            text = tweet.text
            text = " ".join(filter(lambda x:x[0]!='@', text.split())) # Removes the @'s
            if (text[0:2] == "RT"):
                text = text[3:-1] # Removes the word RT to determine the tweet was a RT
                # text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
            text = re.sub(r'http[s]?\:\/\/.+?($|\s)', '', text, flags=re.MULTILINE)

            print(i, str(text), tweet.id, '\n')
        except UnicodeEncodeError:
            try:
                if (hasattr(tweet, tweet.image)):
                    print(i, 'THAT AIN\'T A TWEET.')
            except AttributeError:
                print(i, 'No Image Either')
        i += 1


# print(unidecode(result))
