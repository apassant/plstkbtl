from django.db import models

import musixmatch

from musixmatch import track as TRACK
from musixmatch import artist as ARTIST
from musixmatch import tracking as TRACKING

# Create your models here.

class MusixMatch(object):

    def __init__(self, query):
        self.query = query
        self.apikey = 'a4bdc6b3fa75aea2fef27dde5da26dc3'
        self.tracks = TRACK.search(q=self.query, apikey=self.apikey, page_size=100)


