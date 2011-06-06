from migraters import FriendFeedHtmlMigration
from sources import FriendFeedSource
from localizers import FriendFeedLocalizer
from optparse import OptionParser

def main():
    parser = OptionParser(
        usage="usage: %prog [options] filename",
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

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Wrong number of arguments")

    feed_id = args[0]
    source = FriendFeedSource(feed_id)
    localizer = FriendFeedLocalizer(
        feed_id,
        localize_thumbnails = parser.options['localize_thumbnails'],
        localize_images = parser.options['localize_images'],
        localize_attachments = parser.options['localize_attachments'])
    localized_data = localizer.run()
    
    
if __name__ == '__main__':
    main()
