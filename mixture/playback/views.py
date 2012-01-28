from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response

from rdio import Rdio
rdio = Rdio((settings.RDIO_KEY, settings.RDIO_SECRET))

def playback(request):
  response = rdio.call('search', {
    'types':'track',
    'query': request.REQUEST.get('artist', '') + ' ' + request.REQUEST.get('track', '')
  })

  context = {
    'track': response['result']['results'][0]
  }

  return render_to_response('playback.html', context)

