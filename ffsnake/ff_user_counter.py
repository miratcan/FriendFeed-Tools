from api.friendfeed import FriendFeed
from api.friendfeed import urllib2
from os.path import exists
import cPickle


starting_feeds = ("aynebilm", "5posta", "joanmiro")

feed_stack = set(starting_feeds)
feed_repo  = set()
ff_api = FriendFeed()


def subscribers_of(feed_id):
    try:
        feed_info = ff_api.fetch_feed_info(feed_id)
    except urllib2.HTTPError:
        feed_info = None
        print "Skipping :", feed_id 
    except:
        cPickle.dump(feed_stack, file("feed_stack.pkl", "w"))
        cPickle.dump(feed_repo , file("feed_repo.pkl",  "w"))

    if feed_info:
        subscribers = set([subscription["id"] for subscription in feed_info['subscribers']])
    else:
        subscribers = set()

    return subscribers

# if there is saved process, load it.
if exists("feed_stack.pkl"):
    feed_stack = cPickle.load(file("feed_stack.pkl"))

if exists("feed_repo.pkl"):
    feed_repo = cPickle.load(file("feed_repo.pkl"))

while feed_stack:
    #get current feed
    current_feed = feed_stack.pop()
    # add it to repo
    feed_repo.add(current_feed)
    # get subscribers of current feed
    subscribers = subscribers_of(current_feed)
    # differ subscribers from feed_repo and feed_stack
    # only feed_stack.update is not enought
    subscribers.difference_update(feed_repo.union(feed_stack))
    # push subscribers to feed_stack
    feed_stack.update(subscribers)
    # give some report bro
    print "Stack merged with %s's %d subscribers. Stack size: %s, Repo size: %s " % (current_feed, len(subscribers), len(feed_stack), len(feed_repo))
