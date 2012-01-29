# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.conf import settings

from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import InMemoryUploadedFile
from django import forms

from mixture.models import Mixture

from dependencies.pyiqe.pyiqe import Api as IQEngine
from dependencies.seevl.seevl.seevl import SeevlEntitySearch
from dependencies.rdio.rdio import Rdio

import os


def tracks(request, terms):
  """Get list of tracks mathching the query terms"""
  tracks = Mixture().getTracks(terms)
  return render_to_response("song.html", {
    'tracks': tracks,
  }, context_instance=RequestContext(request))


def play(request, mxmid):
  """Play the track given a MxM id"""
  track = Mixture().getTrack(mxmid)
  return render_to_response('playback.html', {
      'track' : track
  }, context_instance=RequestContext(request))
  
  
iqe = IQEngine('e15511587ea4414f901b9bc1dbaa444a', '46e9fc3bd4684dd6903525fd16da9b74')

class UploadFileForm(forms.Form):
  file = forms.FileField()

def index(request):
  return render_to_response('upload.html', {})

@csrf_exempt
def upload(request):
  try:
    if request.POST:
      # save it somewhere
      imgdata = str(request.raw_post_data)
      data, qid = iqe.query(imgdata=imgdata)
      path = os.path.normpath(os.path.join(__file__, '../static/upload/%s.jpg' % qid))
      print path
      open(path, 'w').write(imgdata)
      # return the URL
      return HttpResponse('/image/%s' % qid)
    else:
      return HttpResponseRedirect('/')
  except Exception, e:
    print `e`

def poll(request, qid):
  result = iqe.result(qid)
  data = result['data']
  if 'results' in data:
    return HttpResponseRedirect('/tracks/'+data['results']['labels'])
  else:
    return render_to_response('poll.html', csrf(request))
