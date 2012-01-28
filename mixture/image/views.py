# Create your views here.
from django.http import HttpResponse

from pyiqe import Api as IQEngine
iqe = IQEngine('e15511587ea4414f901b9bc1dbaa444a', '46e9fc3bd4684dd6903525fd16da9b74')

def index(request):
  return HttpResponse('hello, world')