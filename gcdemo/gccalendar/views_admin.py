from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.template import loader
from .models import GcDay, Area
from .constants import *

import datetime

def index(request):
  print(request.user.username)
  if not request.user.is_staff:
    return HttpResponseForbidden()
  context = {
    'user': request.user
  }
  return render(request, 'gccalendar/admin/index.html', context)