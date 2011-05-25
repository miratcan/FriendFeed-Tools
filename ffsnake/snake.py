from api.friendfeed import FriendFeed
from api.friendfeed import urllib2

# start from here
starting_feeds = ("debbieturner",)
# stack
feed_stack = set(starting_feeds)
# repo
feed_repo = set()
# api
ff_api = FriendFeed()

def get_subscribers(feed_id):
    print "Extending stack with subscribers of", feed_id
    try:
        feed_info = ff_api.fetch_feed_info(feed_id)
    except urllib2.HTTPError:
        print feed_id, "is not exists, skipping."

    if feed_info:
        subscribers = set([subscription["id"] for subscription in feed_info['subscribers']))
    else:
        subscribers = set()
    return subscribers


while stack:
    current_feed = feed_stack.pop()
    current_feeds_subscribers = get_subscribers(current_feed)
    feed_stack.update(current_feeds_subscribers)
    feed_repo.update(current_feeds_subscribers)
    print "Current stack size : %s, Feed repo size : %s " % (len(feed_stack), len(feed_repo))

print stack
