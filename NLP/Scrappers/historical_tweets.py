##
import tweepy

CONSUMER_KEY    = 'u9oTn95Tyx7PeKqaVoQOr4zIg'
CONSUMER_SECRET = 'DsH1mYSYyQOKOlUkvVvtV0YBBiWdaSyVleEAOhJbNmJYF2VaI6'

# Access:
ACCESS_TOKEN  = '936220490246557696-cansWdvPlCC0HAOzXL3CxU3b7M1XrKJ'
ACCESS_SECRET = 'lZtJmEHxC88gVZ1hcQPLCslwVjS8ZjDy45IVyaqrwFrdk'

def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API with authentication:
    api = tweepy.API(auth)
    return api

api = twitter_setup()


for tweet in tweepy.Cursor(api.search,q="Apple",count=10,
                           lang="en",
                           since='2018-08-01', until='2018-08-02').items():
    print (tweet.created_at, tweet.text)
