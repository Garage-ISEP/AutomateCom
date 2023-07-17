from typing import Tuple, Any
import os
import tweepy


def post_tweet(tweet: str) -> Tuple[bool, Any]:
    """
    Post a tweet using Twitter credentials and API key.
    :param tweet: Content of the tweet
    :return: Boolean value and (status or Exception)
    """
    twitter_auth_keys = {
        "consumer_key": os.getenv("TWITTER_CONSUMER_KEY"),
        "consumer_secret": os.getenv("TWITTER_CONSUMER_SECRET"),
        "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
        "access_token_secret": os.getenv("TWITTER_TOKEN_SECRET")
    }
    auth = tweepy.OAuthHandler(
        twitter_auth_keys['consumer_key'],
        twitter_auth_keys['consumer_secret']
    )
    auth.set_access_token(
        twitter_auth_keys['access_token'],
        twitter_auth_keys['access_token_secret']
    )
    api = tweepy.API(auth)
    try:
        status = api.update_status(status=tweet)
        return True, status
    except tweepy.errors.TweepyException as e:
        return False, e

if __name__ == '__main__':
    pass