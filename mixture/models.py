from django.conf import settings

from dependencies.seevl.seevl.seevl import SeevlEntitySearch

import os

class MusixMatch(object):
    """Integraion with MxM API"""
    
    def __init__(self):
        """Setup API key"""
        os.environ['MUSIXMATCH_API_KEY'] = settings.MXM_API_KEY

    def getTracks(self, query):
        """Get tracks matching a query term"""
        ## Need to do the import here to be sure the environment var is set        
        from musixmatch import track as TRACK
        return self.filterTracks(TRACK.search(q=query, page_size=10))

    def filterTracks(self, tracks):
        """Filter to get only tracks with artist matching in seevl"""
        return filter(lambda x: 
            len(SeevlEntitySearch({
                'prefLabel' : x.artist_name.encode('utf-8')
            }, seevl_app_id = settings.SEEVL_APP_ID, seevl_app_key = settings.SEEVL_APP_KEY).run()),
            tracks)

    def getTrack(self, track):
        """Get track infos"""
        ## Need to do the import here to be sure the environment var is set
        from musixmatch import track as TRACK
        track = TRACK.Track(track)
        return {
            'artist' : track.artist_name,
            'title' : track.track_name,
            'lyrics' : track.lyrics()['lyrics_body']
        }

        