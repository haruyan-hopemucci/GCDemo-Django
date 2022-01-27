from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import GcDay
# Create your views here.
def index(request):
  # return HttpResponse("Hello, world. You're at the polls index.")
  # template = loader.get_template('gccalendar/index.html')
  # return HttpResponse(template.render({},request))
  data = GcDay.objects.all()
  context = {
    'days': data
  }
  return render(request, 'gccalendar/index.html', context)