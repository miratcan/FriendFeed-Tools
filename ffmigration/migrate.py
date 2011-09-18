#-*- coding:utf-8 -*-
from migraters import FriendFeedHtmlMigration
from sources import FriendFeedSource
from localizers import FriendFeedLocalizer
from optparse import OptionParser
from os.path import join
from urllib2 import HTTPError
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.INFO)

# QUESTION: I am not sure that i have to describe dependencies at runtime.
try:
    from simplejson import dump
except ImportError:
    raise ImportError("You need to install simplejson package to run this application")

def main():
    parser = OptionParser(
        usage="usage: %prog [options] feedid",
        version="%prog 1.0")

    parser.add_option(
        "-t", "--thumbnails",
        action="store_true",
        dest="localize_thumbnails",
        default=False,
        help="Localize and backup thumbnails of feed")

    parser.add_option(
        "-i", "--images",
        action="store_true",
        dest="localize_images",
        default=False,
        help="Localize and backup shared images of feed")

    parser.add_option(
        "-a", "--attachments",
        action="store_true",
        dest="localize_attachments",
        default=False,
        help="Localize and backup shared attachment of feed")

    parser.add_option(
        "-l", "--limit",
        action="store",
        dest="fetch_limit",
        default=0,
        type="int",
        help="Limit number of entries that will be collected",)


    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Wrong number of arguments")

    feed_id = args[0]
    try:
        source = FriendFeedSource(feed_id, fetch_limit=options.fetch_limit)
        localizer = FriendFeedLocalizer(
            feed_id,
            options = {
                "localize_thumbnails": options.localize_thumbnails,
                "localize_images": options.localize_images,
                "localize_attachments": options.localize_attachments
        })
        localized_data = localizer.run()
        localized_data_file = file(join(localizer.options['backup_path'], feed_id + ".lfd"), "w")
        dump(localized_data, localized_data_file)
        localized_data_file.close()
        migrater = FriendFeedHtmlMigration()
        migrater.run(localized_data)
    except HTTPError:
        logging.error("Geçersiz ID")
    

if __name__ == '__main__':
    main()
