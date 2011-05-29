from urllib2 import urlopen, URLError
from os.path import exists

def download(remote_file_path, local_file_path):
    """Simple file downloader function
    """
    if not exists(local_file_path):
        try:
            open(local_file_path, 'w').write(urlopen(remote_file_path).read()) # moaarrr...!
        except URLError:
            print remote_file_path, "could'nt downloaded, skipping..."
        print local_file_path, "downloaded..."
    else:
        print local_file_path, "skipping..."
