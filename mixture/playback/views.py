from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response

from seevl import SeevlEntitySearch
from rdio import Rdio

from song.models import MusixMatch

rdio = Rdio((settings.RDIO_KEY, settings.RDIO_SECRET))

def playback(request, mxmid):

  assert(mxmid)
  track = MusixMatch().getTrack(mxmid)
  response = rdio.call('search', {
    'types':'track',
    'query': "%s %s" %(track['artist'], track['title'])
  })
  
  seevlArtist = SeevlEntitySearch({
    'prefLabel' : track['artist']
  }, seevl_app_id = settings.SEEVL_APP_ID, seevl_app_key = settings.SEEVL_APP_KEY).run()[0]

  context = {
    'track': response['result']['results'][0],
    'artist' : seevlArtist,
    'lyrics' : track['lyrics']
  }
  
  return render_to_response('playback.html', context)