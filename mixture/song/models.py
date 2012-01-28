from django.db import models

import musixmatch

from musixmatch import track as TRACK
from musixmatch import artist as ARTIST
from musixmatch import tracking as TRACKING

from seevl.seevl import SeevlEntitySearch
from django.conf import settings

# Create your models here.

class MusixMatch(object):

    def __init__(self, query):
        self.query = query
        self.apikey = 'a4bdc6b3fa75aea2fef27dde5da26dc3'
        self.tracks = self.filterTracks(TRACK.search(q=self.query, apikey=self.apikey, page_size=10))
        
    def filterTracks(self, tracks):
        """Get only tracks with artist matching in seevl"""
        return filter(lambda x: 
            len(SeevlEntitySearch({'prefLabel' : x.artist_name}, seevl_app_id = settings.SEEVL_APP_ID, seevl_app_key = settings.SEEVL_APP_KEY).run()),
            tracks)
        
