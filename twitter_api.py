import os
import json
import tweepy
from dataclasses import dataclass

@dataclass
class APIKeys:
    '''Δομή δεδομένων για τα κλειδιά του API'''
    
    consumer_key: str
    consumer_secret: str
    access_token_key: str
    access_token_secret: str

def load_api_keys() -> APIKeys:
    '''Φόρτωση των κλειδιών του API από το αρχείο .env'''

    consumer_key = os.getenv('X_CONSUMER_KEY')
    consumer_secret = os.getenv('X_CONSUMER_SECRET')
    access_token_key = os.getenv('X_ACCESS_TOKEN_KEY')
    access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')
    
    # Έλεγχος αν λείπει κάποιο από τα κλειδιά
    if not all([consumer_key, consumer_secret, access_token_key, access_token_secret]):
        raise ValueError("One or more API keys are missing. Please check your .env file.")

    return APIKeys(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token_key=access_token_key,
        access_token_secret=access_token_secret
    )

def create_tweepy_api(api_keys: APIKeys) -> tweepy.API:
    '''Δημιουργία tweepy API'''

    auth = tweepy.OAuth1UserHandler(
        api_keys.consumer_key, 
        api_keys.consumer_secret, 
        api_keys.access_token_key, 
        api_keys.access_token_secret
    )
    api = tweepy.API(auth)
    
    return api

def print_user_info(user_info):
    '''Εκτύπωση των πληροφοριών του χρήστη'''

    print("User ID:", user_info.id)
    print("Name:", user_info.name)
    print("Screen Name:", user_info.screen_name)
    print("Followers Count:", user_info.followers_count)
    print("Friends Count:", user_info.friends_count)
    print("Description:", user_info.description)
    print("Location:", user_info.location)
    print("Profile Image URL:", user_info.profile_image_url_https)

    # Εκτύπωση του πλήρους JSON για ανάλυση
    print("\nFull JSON response:")
    print(json.dumps(user_info._json, indent=4, sort_keys=True))

if __name__ == "__main__":
    try:
        # Φόρτωση κλειδιών API
        api_keys = load_api_keys()
        
        # Δημιουργία του API
        api = create_tweepy_api(api_keys)
        
        # Κλήση της verify_credentials και εμφάνιση των πληροφοριών χρήστη
        user_info = api.verify_credentials()
        print_user_info(user_info)
        
    except ValueError as ve:
        print("Configuration error occurred. Please check your API keys and .env file.")
        
    except tweepy.Unauthorized as tu:
        print("Unauthorized access. Please check your API keys.")
        
    except Exception as e:
        print("An unexpected error occurred. Please check the logs for more details.")