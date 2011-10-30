from api.friendfeed import FriendFeed
from api.friendfeed import urllib2

from os.path import exists

import cPickle

from datetime import datetime
from datetime import timedelta

CURRENT_TIME = datetime.now()
STARTING_FEEDS = ("joanmiro",)
MAX_PASSIVE_DAYS = timedelta(30)

ff_api = FriendFeed()
feed_stack = set(STARTING_FEEDS)
feed_repo = set()

def subscribers_of(feed_id):
    """
    1) Gets subscribers of feed
    2) Checks subscribers entries to find passive feeds.
    3) Returns active_feeds, passive_feeds
    """
    subscribers = []

    try:
        feed_info = ff_api.fetch_feed_info(feed_id)
    except urllib2.HTTPError:
        feed_info = None
        print "Could'nt read subscribers:", feed_id

    if feed_info:
        print "Feed info fetched:", feed_info['id']
        # get subscribers
        subscribers = feed_info['subscribers']
        # filter as user
        subscribers = filter(lambda f: f['type']=="user", subscribers)
    else:
        subscribers = []
    return subscribers


def feed_is_active(feed_info):
    try:
        entries = ff_api.fetch_feed(feed_info['id'], num=1)['entries']
    except urllib2.HTTPError:
        print "Could'nt read entries :", feed_info['id']
        return False

    if len(entries) > 0:
        latest_entry = entries[0]
    else:
        print "Strange... this feed has no entries:", feed_info['id']
        return False

    if CURRENT_TIME - latest_entry['date'] < MAX_PASSIVE_DAYS:
        print "Feed is ACTIVE:", feed_info['id']
        return True
    else:
        print "Feed is PASSIVE:", feed_info['id']
        return False

# if there is saved process, load it.
if exists("feed_stack.pkl"):
    feed_stack = cPickle.load(file("feed_stack.pkl"))

if exists("feed_repo.pkl"):
    feed_repo = cPickle.load(file("active_feeds.pkl"))

while feed_stack:
    # get current feed
    current_feed = feed_stack.pop()

    # if feed is active
    feed_repo.add(current_feed)

    # get subscribers of current feed
    subscribers = subscribers_of(current_feed)

    # filter feeds thats not active
    print "Removing passive feeds from list"
    subscribers = filter(feed_is_active, subscribers)

    # differ subscribers from feed_repo and feed_stack
    # only feed_stack.update is not enought
    subscribers.difference_update(feed_repo.union(feed_stack))

    # push subscribers to feed_stack
    feed_stack.update(subscribers)

    # give some report bro
    print "Stack merged with %s's %d subscribers. Stack size: %s, Repo size: %s " % (current_feed, len(subscribers), len(feed_stack), len(feed_repo))
