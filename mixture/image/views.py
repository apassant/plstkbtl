# Create your views here.
from django.core.context_processors import csrf
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render_to_response

from pyiqe import Api as IQEngine
iqe = IQEngine('e15511587ea4414f901b9bc1dbaa444a', '46e9fc3bd4684dd6903525fd16da9b74')


class UploadFileForm(forms.Form):
  file = forms.FileField()


def index(request):
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      data, qid = iqe.query(imgdata=request.FILES['file'].read())
      return HttpResponseRedirect('/image/'+qid)
  else:
    form = UploadFileForm()
  context = {'form': form}
  context.update(csrf(request))
  return render_to_response('upload.html', context)
  
  
def poll(request, qid):
  result = iqe.result(qid)
  data = result['data']
  if 'results' in data:
    return HttpResponseRedirect('/play/'+data['results']['labels'])
  else:
    return render_to_response('poll.html', csrf(request))
