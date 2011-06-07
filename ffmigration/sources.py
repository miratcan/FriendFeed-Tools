from urllib2 import urlopen
from urllib import urlencode
from simplejson import loads, dumps
from time import sleep as wait

_loads = lambda string: loads(string.decode("utf-8"))

class FriendFeedSource(object):
    """
    File like object for feeds.

    >>> entry_source = EntrySource("breth")
    >>> entry_source.read() # returns feed with all of its entries
    """
    # TODO : If friendfeed starts to send same data it means 
    # we get over the latest feed. I think it's a bug of friendfeed
    # becuz it's not happening at feeds that have not connected
    # with twitter. We need to stop at there.

    FEED_DATA_PATTERN = "http://friendfeed-api.com/v2/feed/%s?%s"
    MAX_FETCH_SIZE = 150
    WAIT_BETWEEN_BITES = 5 # seconds

    def __init__(self, feed_id, fetch_size=100, fetch_limit=0):
        self.feed_id = feed_id
        self.cursor_at = 0
        self.fetch_limit = fetch_limit
        print "Feed collector initialized for %s" % self.feed_id
        print "Ready for fetching %s entries" % (self.fetch_limit or "all")

    def read(self):
        chunk = self._take_a_bite()
        feed_buffer = chunk
        while chunk['entries']:
            if self.fetch_limit != 0 and self.cursor_at >= self.fetch_limit:
                break
            feed_buffer['entries'].extend(chunk['entries'])
            print "Waiting for %d seconds..." % self.WAIT_BETWEEN_BITES
            wait(self.WAIT_BETWEEN_BITES)
            print "Fetching data..."
            chunk = self._take_a_bite()
            print "%s entries collected." % self.cursor_at
        return dumps(feed_buffer)

    def _take_a_bite(self):
        if self.fetch_limit:
            if self.fetch_limit - self.cursor_at > self.MAX_FETCH_SIZE:
                fetch_size = self.MAX_FETCH_SIZE
            else:
                fetch_size = self.fetch_limit - self.cursor_at
        else:
            fetch_size = self.MAX_FETCH_SIZE
        params = urlencode({"start": self.cursor_at, "num" : fetch_size})
        feed_url = self.FEED_DATA_PATTERN % (self.feed_id, params)
        stream = urlopen(feed_url)
        data = _loads(stream.read())
        stream.close()

        if data.has_key("errorCode"):
            raise ValueError(data['errorCode'])
        else:
            self.cursor_at += self.MAX_FETCH_SIZE
        return data

if __name__ == "__main__":
    # TODO: write tests here...
    collector = FeedCollector("joanmiro", fetch_limit=200)
    d = collector.read()
    for e in d['entries']:
        print e['body']
