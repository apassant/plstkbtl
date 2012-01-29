# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from song.models import MusixMatch

def index(request, terms):
    tracks = MusixMatch().getTracks(terms)
    return render_to_response("song.html", {
        'tracks': tracks,
    }, context_instance=RequestContext(request))
