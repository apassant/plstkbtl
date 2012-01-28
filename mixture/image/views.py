# Create your views here.
from django.core.context_processors import csrf
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render_to_response
import os

from pyiqe import Api as IQEngine
from django.views.decorators.csrf import csrf_exempt


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
      path = os.path.normpath(os.path.join(__file__, '../../static/upload/%s.jpg' % qid))
      open(path, 'w').write(imgdata)
      # return the URL
      return HttpResponse('/image/%s' % qid)
    else:
      return HttpResponseRedirect('/image/')
  except Exception, e:
    print `e`

  
  
def poll(request, qid):
  result = iqe.result(qid)
  data = result['data']
  if 'results' in data:
    return HttpResponseRedirect('/tracks/'+data['results']['labels'])
  else:
    return render_to_response('poll.html', csrf(request))
