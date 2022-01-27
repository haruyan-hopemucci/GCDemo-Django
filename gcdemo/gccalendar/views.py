from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import GcDay
from .constants import *

import datetime

# Create your views here.
def index(request):
  # 本日より7日分の日付を取得
  today = datetime.date.today()
  addDays = range(0,7)
  days = [None] * 7
  for i in addDays:
    days[i] = today + datetime.timedelta(days=i)

  gcdayData = GcDay.objects.all()

  daysData = list()

  for d in days:
    addData = {'day': d.strftime("%d日"), 'dow': jpdow(d), 'gcday': None}
    fil = gcdayData.filter(gcdate=d)
    print(fil)
    if(fil.count() == 0):
      None
    else:
      addData['gcday'] = fil[0]
    print(addData)
    daysData.append(addData)

  context = {
    'days': daysData
  }
  return render(request, 'gccalendar/index.html', context)