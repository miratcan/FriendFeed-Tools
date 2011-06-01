from urllib import urlopen, urlencode
from simplejson import loads, dumps
_loads = lambda string: loads(string.decode("utf-8"))

class FeedSource(object):
    """
    File like object for feeds.

    >>> entry_source = EntrySource("breth")
    >>> entry_source.read() # returns feed with all of its entries
    """

    FEED_DATA_PATTERN = "http://friendfeed-api.com/v2/feed/%s?%s"
    FETCH_SIZE = 100

    def __init__(self, feed_id, fetch_size=100, stop_at=0):
        self.feed_id = feed_id
        self.cursor_at = 0
        self.stop_at = stop_at
        print "Feed collector initialized for %s" % self.feed_id

    def read(self):
        chunk = self._take_a_bite()
        feed_buffer = chunk
        while chunk['entries']:
            print "%s entries collected." % self.cursor_at
            feed_buffer['entries'].extend(chunk['entries'])
            if self.stop_at != 0 and self.cursor_at > self.stop_at:
                break
            chunk = self._take_a_bite()
        return dumps(feed_buffer)

    def _take_a_bite(self):
        params = urlencode({"start": self.cursor_at, "num" : self.FETCH_SIZE})
        feed_url = self.FEED_DATA_PATTERN % (self.feed_id, params)
        data = _loads(urlopen(feed_url).read())
        if data.has_key("errorCode"):
            raise ValueError(data['errorCode'])
        else:
            self.cursor_at += self.FETCH_SIZE
        return data

if __name__ == "__main__":
    collector = FeedCollector("joanmiro", stop_at=200)
    d = collector.read()
    for e in d['entries']:
        print e['body']
