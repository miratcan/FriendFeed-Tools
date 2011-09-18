from urllib2 import urlopen, URLError
from os.path import exists
import re
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',level=logging.INFO)

def download(remote_file_path, local_file_path):
    """Simple file downloader function
    """
    if not exists(local_file_path):
        try:
            open(local_file_path, 'w').write(urlopen(remote_file_path).read()) # moaarrr...!
        except URLError:
            logging.error(remote_file_path, "could'nt downloaded, skipping...")
        logging.info("%s downloaded..." % local_file_path)
    else:
        logging.warning("%s skipping..." % local_file_path)

def slugify(string):
    string = re.sub('\s+', '_', string)
    string = re.sub('[^\w.-]', '', string)
    return string.strip('_.- ').lower()
