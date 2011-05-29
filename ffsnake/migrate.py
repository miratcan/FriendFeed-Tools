from sources import EntrySource
from urllib2 import urlparse
from os.path import exists, join, dirname
from os import mkdir
from utils import download
from cPickle import dump

class FriendFeedDumper(object):
    def __init__(self, feed_id):

        self.feed_id = feed_id
        self.entry_source = EntrySource(feed_id, stop=50)
        self.backup_path = self._backup_path()
        self.thumbnails_path = self._thumbnails_path()
        self.attachments_path = self._attachments_path()
        self.entries = list()

        if not exists(self.backup_path):
            mkdir(self.backup_path)

        if not exists(self.thumbnails_path):
            mkdir(self.thumbnails_path)

        if not exists(self.attachments_path):
            mkdir(self.attachments_path)

    def _backup_path(self):
        """Returns folder that will we backup
        """
        return join((dirname(__file__)), self.feed_id)

    def _thumbnails_path(self):
        """Returns folder that where we will save thumbnails
        """
        return join(self.backup_path, "thumbnails")

    def _attachments_path(self):
        """Returns folder that where we will save attachments
        """
        return join(self.backup_path, "attachments")

    def dump(self):
        i = 0
        for entry_data in self.entry_source:
            entry = FriendFeedEntry(entry_data, self.thumbnails_path, self.attachments_path)
            entry.localize()
            self.entries.append(entry.data)
            print i, "entries collected."
            i += 1
        dump(self.entries, file(join(self.backup_path, "feed.pkl"), "w"))

class FriendFeedEntry(object):
    """
    """

    def __init__(self, data, thumbnails_path, attachments_path):
        """
        """
        self.thumbnails_path = thumbnails_path
        self.attachments_path = attachments_path
        self.data = data

    def localize(self):
        if "thumbnails" in self.data.keys():
            self._localize_thumbnails()

        if "files" in self.data.keys():
            self._localize_attachments()

    def _localize_thumbnails(self):
        """Localizes thumbnail urls of entry
        """
        self._download_thumbnails()
        for thumbnail in self.data['thumbnails']:
            thumbnail['url'] = self._filename_for_thumbnail(thumbnail)

    def _localize_imags(self):
        for thumbnail in self.data['thumbnails']:
            thumbnail['url'] = self._filename_for_thumbnail(thumbnail)

    def _filename_for_thumbnail(self, thumbnail):
        """Generates local filename for thumbnail
        """
        return join(self.thumbnails_path, urlparse.urlparse(thumbnail['url']).path[1:].replace("/", ""))

    def _localize_attachments(self):
        """Localizes attachment urls of entry
        """
        self._download_attachments()
        for attachment in self.data['files']:
            attachment['url'] = self._filename_for_attachment(attachment)

    def _filename_for_attachment(self, attachment):
        """Generates local filename for attachment
        """
        return join(self.attachments_path, attachment['name'])

    def _download_thumbnails(self):
        """Downloads thumbnails
        """
        for thumbnail in self.data['thumbnails']:
            download(thumbnail['url'], self._filename_for_thumbnail(thumbnail))

    def _download_attachments(self):
        """Downloads attachments
        """
        for attachment in self.data['files']:
            download(attachment['url'], self._filename_for_attachment(attachment))

if __name__ == "__main__":
    dumper = FriendFeedDumper("akif87")
dumper.dump()
