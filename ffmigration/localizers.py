# -*- coding: utf-8 -*-

from urllib2 import urlparse
from os.path import exists, join, dirname
from os import mkdir

from simplejson import loads

_loads = lambda string: loads(string.decode("utf-8"))

from utils import download
from utils import slugify
from sources import FriendFeedSource

import logging
logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.INFO)

class FriendFeedLocalizer(object):
    """ A process that converts sources remote file paths to local file paths.
    """

    def __init__(self, feed_id, options={}):

        self.feed_id = feed_id
        self.feed_data = _loads(FriendFeedSource(feed_id).read())
        self.options = options

        if not options.has_key("backup_path"):
            options["backup_path"] = self._backup_path()

        if not exists(self.options['backup_path']):
            mkdir(self.options['backup_path'])

        if not exists(self._thumbnails_path()):
            mkdir(self._thumbnails_path())

        if not exists(self._images_path()):
            mkdir(self._images_path())

        if not exists(self._attachments_path()):
            mkdir(self._attachments_path())

        self.downloads = []

    def run(self):

        logging.info("Starting localization")

        current = 0
        for entry in self.feed_data['entries']:
            if entry.has_key("thumbnails"):
                self._localize_thumbnails(entry)
                self._localize_images(entry)
            if entry.has_key("files"):
                self._localize_attachments(entry)

            logging.info("%s entries localized." % str(current))
            current += 1

        logging.info("Starting downloads...")

        current = 0
        dl_length = len(self.downloads)
        for dl in self.downloads:
            logging.info("Downloading %d of %d" % (current, dl_length))
            download(dl[0], dl[1])
            current += 1
        return self.feed_data

    def _backup_path(self):
        """Returns folder that will we backup
        """
        return join((dirname(__file__)), self.feed_id)

    def _thumbnails_path(self):
        """Returns folder that where we will save thumbnails
        """
        return join(self.options['backup_path'], "thumbnails")

    def _images_path(self):
        """Returns folder that where we will save thumbnails
        """
        return join(self.options['backup_path'], "images")

    def _attachments_path(self):
        """Returns folder that where we will save attachments
        """
        return join(self.options['backup_path'], "attachments")

    def _queue_download(self, remote_path, local_path):
        self.downloads.append((remote_path, local_path))

    def _localize_thumbnails(self, entry):
        """Localizes thumbnail urls of entry
        """
        for thumbnail in entry['thumbnails']:                
            self._queue_download(thumbnail['url'], self._filename_for_thumbnail(thumbnail))
            thumbnail['url']  = self._filename_for_thumbnail(thumbnail)

    def _localize_images(self, entry):
        for thumbnail in entry['thumbnails']:          
            if thumbnail['link'].startswith("http://m.friendfeed-media.com/"):
                self._queue_download(thumbnail['link'], self._filename_for_image(thumbnail))
                thumbnail['link'] = self._filename_for_image(thumbnail)

    def _localize_attachments(self, entry):
        """Localizes attachment urls of entry
        """
        for attachment in entry['files']:
            self._queue_download(attachment['url'], self._filename_for_attachment(attachment))
            attachment['url'] = self._filename_for_attachment(attachment)

    def _filename_for_thumbnail(self, thumbnail):
        """Generates local filename for thumbnail
        """
        return join(self._thumbnails_path(), slugify(urlparse.urlparse(thumbnail['url']).path[1:]))

    def _filename_for_image(self, thumbnail):
        """Generates local filename for thumbnail image
        """
        return join(self._images_path(), urlparse.urlparse(thumbnail['link']).path[1:])

    def _filename_for_attachment(self, attachment):
        """Generates local filename for attachment
        """
        return join(self._attachments_path(), slugify(attachment['name']))

if __name__ == "__main__":

    import sys

    sys.path.append("..")

    feed_id = "5posta"
    localizer = Localizer(feed_id, FeedSource(feed_id))
    localizer.run()

    env = Environment(loader=PackageLoader('ffsnake', 'templates'))
    template = env.get_template('base.html')
