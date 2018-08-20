import os
import datetime
import posixpath
from urllib.parse import urlsplit, unquote

def filesystem_init():
    if not os.path.exists(download_cache_path()):
        os.makedirs(download_cache_path())

def root_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")

def download_cache_path():
    return os.path.join(root_path(),'osu_cache')

def exists_in_cache(filename):
    return os.path.isfile(os.path.join(download_cache_path(), filename))

def url_to_filename(url):
    urlpath = urlsplit(url).path
    basename = posixpath.basename(unquote(urlpath))
    if (os.path.basename(basename) != basename or unquote(posixpath.basename(urlpath)) != basename):
        return "default.png"
    return basename