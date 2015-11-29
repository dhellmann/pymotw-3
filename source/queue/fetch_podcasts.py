#!/usr/bin/env python
"""Use several threads to download enclosures from RSS feeds.
"""
#end_pymotw_header

from queue import Queue
import threading
import time
import urllib
from urllib.parse import urlparse

import feedparser

# Set up some global variables
num_fetch_threads = 2
enclosure_queue = Queue()

# A real app wouldn't use hard-coded data...
feed_urls = [
    'http://talkpython.fm/episodes/rss',
]


def message(s):
    print('%s: %s' % (threading.current_thread().name, s))


def download_enclosures(q):
    """This is the worker thread function.
    It processes items in the queue one after
    another.  These daemon threads go into an
    infinite loop, and only exit when
    the main thread ends.
    """
    while True:
        message('looking for the next enclosure')
        url = q.get()
        parsed_url = urlparse(url)
        message('downloading: %s' % parsed_url.path)
        response = urllib.request.urlopen(url)
        data = response.read()
        # Save the downloaded file to the current directory
        outfile_name = url.rpartition('/')[-1]
        message('writing to %s' % outfile_name)
        with open(outfile_name, 'wb') as outfile:
            outfile.write(data)
        q.task_done()


# Set up some threads to fetch the enclosures
for i in range(num_fetch_threads):
    worker = threading.Thread(
        target=download_enclosures,
        args=(enclosure_queue,),
        name='worker-%s' % i,
    )
    worker.setDaemon(True)
    worker.start()

# Download the feed(s) and put the enclosure URLs into
# the queue.
for url in feed_urls:
    response = feedparser.parse(url, agent='fetch_podcasts.py')
    for entry in response['entries'][:5]:
        for enclosure in entry.get('enclosures', []):
            parsed_url = urlparse(enclosure['url'])
            message('queuing %s' % parsed_url.path)
            enclosure_queue.put(enclosure['url'])

# Now wait for the queue to be empty, indicating that we have
# processed all of the downloads.
message('*** main thread waiting')
enclosure_queue.join()
message('*** done')
