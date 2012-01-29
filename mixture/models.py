from django.conf import settings

from musixmatch import track as TRACK
from dependencies.seevl.seevl.seevl import SeevlEntitySearch

class MusixMatch(object):
    """Integraion with MxM API"""
    
    def __init__(self):
        """Setup API key"""
        self.apikey = settings.MXM_API_KEY
        
    def getTracks(self, query):
        """Get tracks matching a query term"""
        return self.filterTracks(TRACK.search(q=query, apikey=self.apikey, page_size=10))
        
    def filterTracks(self, tracks):
        """Filter to get only tracks with artist matching in seevl"""
        return filter(lambda x: 
            len(SeevlEntitySearch({
                'prefLabel' : x.artist_name.encode('utf-8')
            }, seevl_app_id = settings.SEEVL_APP_ID, seevl_app_key = settings.SEEVL_APP_KEY).run()),
            tracks)
    
    def getTrack(self, track):
        """Get track infos"""
        track = TRACK.Track(track)
        return {
            'artist' : track.artist_name,
            'title' : track.track_name,
            'lyrics' : track.lyrics()['lyrics_body']
        
        }

        