import sys
import configparser
try:
    import tweepy
except ImportError:
    print("[ERROR] Unable to import Tweepy module: can't run!")
    sys.exit()


class Authenticator:

    def __init__(self):
        self._consumer_key = ""
        self._consumer_secret = ""
        self._access_key = ""
        self._access_secret = ""
        self._auth = ""
        self._api = ""
        self._config = configparser.ConfigParser()

    def auth_setup(self, auth_file):
        try:
            print("[*] Reading user credentials...")
            with open(auth_file, 'r') as self._auth:
                self._config.read_file(self._auth)
                self._consumer_key = self._config.get(
                    "ConsumerKey", "consumer_key")
                self._consumer_secret = self._config.get(
                    "ConsumerSecret", "consumer_secret")
                self._access_key = self._config.get("AccessKey", "access_key")
                self._access_secret = self._config.get(
                    "AccessSecret", "access_secret")
            print("[SUCCESS] Done.\n")
        except (IOError, OSError):
            print("[ERROR] Unable to find user data file (auth_user.ini)")
            sys.exit()

        print("[*] Trying access to Twitter...")

        try:
            self._auth = tweepy.OAuthHandler(
                self._consumer_key, self._consumer_secret)
        except Exception as e:
            print("[ERROR] Unable to make OAuthHandler session!")
            print("\n[Details]: ", e)
            sys.exit()
        try:
            self._auth.set_access_token(self._access_key, self._access_secret)
        except Exception as e:
            print("[ERROR] Unable to set Access Token!")
            print("\n[Details]: ", e)
            sys.exit()
        try:
            self._api = tweepy.API(self._auth)
        except Exception as e:
            print("[ERROR] Unable to access Twitter profile!")
            print("\n[Details]: ", e)
            sys.exit()

        print("[SUCCESS] Access granted.\n")
        return self._api
