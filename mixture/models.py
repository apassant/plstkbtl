from django.db import models

from dependencies.musixmatch.musixmatch import track as TRACK
from dependencies.seevl.seevl.seevl import SeevlEntitySearch

from django.conf import settings

# Create your models here.
class MusixMatch(object):

    def __init__(self):
        self.apikey = 'a4bdc6b3fa75aea2fef27dde5da26dc3'
        
    def getTracks(self, query):
        return self.filterTracks(TRACK.search(q=query, apikey=self.apikey, page_size=10))
        
    def filterTracks(self, tracks):
        """Get only tracks with artist matching in seevl"""
        return filter(lambda x: 
            len(SeevlEntitySearch({
                'prefLabel' : x.artist_name.encode('utf-8')
            }, seevl_app_id = settings.SEEVL_APP_ID, seevl_app_key = settings.SEEVL_APP_KEY).run()),
            tracks)
    
    def getTrack(self, track):
        track = TRACK.Track(track)
        return {
            'artist' : track.artist_name,
            'title' : track.track_name,
            'lyrics' : track.lyrics()['lyrics_body']
        
        }

        