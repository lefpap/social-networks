import os
import json
import tweepy
from dataclasses import dataclass

@dataclass
class APIKeys:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str


def load_api_keys() -> APIKeys:

    # Load keys from environment variables
    consumer_key = os.getenv('X_CONSUMER_KEY')
    consumer_secret = os.getenv('X_CONSUMER_SECRET')
    access_token = os.getenv('X_ACCESS_TOKEN_KEY')
    access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')
    
    # Check if any of the keys are missing
    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        raise ValueError("One or more API keys are missing. Please check your .env file.")

    return APIKeys(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )


def create_tweepy_api(api_keys: APIKeys) -> tweepy.API:
    # Authenticate with the Twitter API
    auth = tweepy.OAuth1UserHandler(
        api_keys.consumer_key, 
        api_keys.consumer_secret, 
        api_keys.access_token, 
        api_keys.access_token_secret
    )
    api = tweepy.API(auth)
    
    # Verify the credentials
    if not api.verify_credentials():
        raise tweepy.TweepError("Failed to verify credentials.")

    return api


def print_user_info(user_info):
    print("User ID:", user_info.id)
    print("Name:", user_info.name)
    print("Screen Name:", user_info.screen_name)
    print("Followers Count:", user_info.followers_count)
    print("Friends Count:", user_info.friends_count)
    print("Description:", user_info.description)
    print("Location:", user_info.location)
    print("Profile Image URL:", user_info.profile_image_url_https)

    # Print the full JSON response for analysis
    print("\nFull JSON response:")
    print(json.dumps(user_info._json, indent=4, sort_keys=True))


if __name__ == "__main__":
    try:
        # Load API keys
        api_keys = load_api_keys()
        
        # Create the Tweepy API object
        api = create_tweepy_api(api_keys)
        
        # Fetch and print user information
        user_info = api.verify_credentials()
        if user_info:
            print_user_info(user_info)
        else:
            print("Failed to authenticate.")
        
    except ValueError as ve:
        print("Configuration error occurred. Please check your API keys and .env file.")
        
    except tweepy.TweepError as te:
        print("An error occurred with the Twitter API. Please try again later.")
        
    except Exception as e:
        print("An unexpected error occurred. Please check the logs for more details.")
