from api.friendfeed import FriendFeed
from api.friendfeed import urllib2

ff_api = FriendFeed()

class EntrySource(object):
    """
    Entry source generator...

    >>> entry_source = EntrySource("breth")
    """
    def __init__(self, feed_id, num=100, stop=0):
        self.feed_id = feed_id
        self.num = num
        self.chunk = []
        self.start = 0
        self.stop = 0

    def __iter__(self):
        pass
        #return self

    def next(self):
        if self.chunk:
            return self.chunk.pop()
        else:
            entries = ff_api.fetch_feed(self.feed_id,
                start=self.start, num=self.num)['entries']

            if not entries:
                print "No data came..."
                raise StopIteration
            elif self.stop > 0 and self.start > self.stop:
                raise StopIteration
            else:
                self.chunk = entries
                self.start += self.num
                return self.chunk.pop()


