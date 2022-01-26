from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
  # return HttpResponse("Hello, world. You're at the polls index.")
  return render(request, 'gccalendar/index.html')
  # template = loader.get_template('gccalendar/index.html')
  # return HttpResponse(template.render({},request))