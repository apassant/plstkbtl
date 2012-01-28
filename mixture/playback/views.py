from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response

from seevl import Seevl
from rdio import Rdio
rdio = Rdio((settings.RDIO_KEY, settings.RDIO_SECRET))

def playback(request):
  response = rdio.call('search', {
    'types':'track',
    'query': request.REQUEST.get('artist', '') + ' ' + request.REQUEST.get('track', '')
  })

  s = Seevl(settings.SEEVL_APP_ID, settings.SEEVL_APP_KEY)
  artist = s.search_by_name(request.REQUEST.get('artist', ''))[0]
  
  context = {
    'track': response['result']['results'][0],
    'artist' : artist
  }
  
  return render_to_response('playback.html', context)

