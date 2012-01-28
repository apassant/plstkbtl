from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response

from seevl import SeevlEntitySearch
from rdio import Rdio
rdio = Rdio((settings.RDIO_KEY, settings.RDIO_SECRET))

def playback(request):
  
  artist = request.REQUEST.get('artist', '')
  track = request.REQUEST.get('track', '')

  response = rdio.call('search', {
    'types':'track',
    'query': "%s %s" %(artist, track)
  })
  
  seevlArtist = SeevlEntitySearch({'prefLabel' : artist}, seevl_app_id = settings.SEEVL_APP_ID, seevl_app_key = settings.SEEVL_APP_KEY).run()[0]
  
  context = {
    'track': response['result']['results'][0],
    'artist' : seevlArtist
  }
  
  return render_to_response('playback.html', context)

