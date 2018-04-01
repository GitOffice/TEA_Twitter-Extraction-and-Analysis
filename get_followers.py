#!/usr/bin/env python3
import sys
import argparse
try:
    import auth_check
except ImportError:
    print("[ERROR] Unable to import auth_check module: can't run!")
    sys.exit()
try:
    import followers_scraper
except BaseException:
    print("[ERROR] Unable to import timeline_scraper module: can't run!")
    sys.exit()
try:
    import text_sentiment
except ImportError:
    print("[ERROR] Unable to import text_sentiment module: can't run!")
    sys.exit()


def get_args():
    parser = argparse.ArgumentParser(
        description='Script get account timeline and filter its tweets using def. keywords')
    parser.add_argument(
        '-a',
        '--auth',
        type=str,
        help='User auth. file',
        required=True)
    parser.add_argument(
        '-u',
        '--user',
        type=str,
        help='Account to process',
        required=True)
    parser.add_argument(
        '-o',
        '--ofile',
        type=str,
        help='CSV output filename',
        required=False,
        default="user_followers.csv")

    args = parser.parse_args()
    uauth = args.auth
    cuser = args.user
    outfile = args.ofile

    return uauth, cuser, outfile


if __name__ == "__main__":

    try:

        uauth, cuser, outfile = get_args()

        auth = auth_check.Authenticator()
        auth = auth.auth_setup(uauth)

        sc = followers_scraper.FollowerScraper()
        sc.get_followers(auth, cuser, outfile)

    except KeyboardInterrupt:
        print("[NOTICE] Script interrupted via keyboard (Ctrl+C)")
        print("Exit...")
        sys.exit()
