from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader
from .models import GcDay, Area
from .constants import *

import datetime

# Create your views here.
def index(request):
  # 本日より7日分の日付を取得
  # today = datetime.date.today()
  today = datetime.date(2022,1,26)
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

def area_id(request, area_id):
  '''
  area_idからカレンダーを表示する

  Parameters
  ----------
  area_id: int
    対象エリアのpk(id)
  '''
  # area_idからAreaオブジェクトの取得
  # 取得できなかった場合は404を返す。
  # ショートカット get_object_or_404 も存在してこっちの方が楽だと思うが、他言語との兼ね合いを考えてtry-exceptで処理する。
  try:
    area = Area.objects.get(pk=area_id)
  except Area.DoesNotExist:
    raise Http404("area_id is not exists.")
  # 週間カレンダー作成部分
  today = datetime.date(2022,1,26) #仮
  lastday = today + datetime.timedelta(days=6)
  addDays = range(0,7)
  days = [None] * 7
  for i in addDays:
    days[i] = today + datetime.timedelta(days=i)

  # リレーション先の値を抽出条件にしてフィルタする
  gcdayData = GcDay.objects.filter(area__pk=area.pk).filter(gcdate__gte=today).filter(gcdate__lte=lastday)
  # print("filter",gcdayData)
  # gcdayData = GcDay.objects.filter(area__pk=area.pk)

  daysData = list()

  for d in days:
    addData = {'day': d.strftime("%d日"), 'dow': jpdow(d), 'gcday': None}
    fil = gcdayData.filter(gcdate=d)
    # print(fil)
    if(fil.count() == 0):
      None
    else:
      addData['gcday'] = fil[0]
    # print(addData)
    daysData.append(addData)

  context = {
    'days': daysData,
    'area_name': area.name,
  }
  return render(request, 'gccalendar/area_weekly.html', context)

def area_id_monthly(request, area_id, yyyymm=None):
  '''
  対象エリアの月カレンダーを返す。

  Parameters
  ----------
  yyyymm : str
    対象月の年月
  '''
  # area_idからAreaオブジェクトの取得
  # 取得できなかった場合は404を返す。
  # ショートカット get_object_or_404 も存在してこっちの方が楽だと思うが、他言語との兼ね合いを考えてtry-exceptで処理する。
  today = datetime.date(2022,1,26) # 仮
  try:
    area = Area.objects.get(pk=area_id)
  except Area.DoesNotExist:
    raise Http404("area_id is not exists.")
  # 対象年月の取得
  yyyymm = '202201' # 仮
  y,m = int(yyyymm[0:4]),int(yyyymm[4:6])
  # 対象年月の一日目を取得
  gcday_first = datetime.date(y,m,1)
  # 対象年月の月末日を取得
  gcday_last = datetime.date(y+(1 if m==12 else 0),(1 if m==12 else m+1),1) + datetime.timedelta(days=-1)
  # 初日から最初の日曜日までさかのぼる
  # pythonでのweekdayは月曜日始まり。0が月曜、5が土曜、6が日曜。
  while gcday_first.weekday() != 6:
    gcday_first = gcday_first + datetime.timedelta(days=-1)
  # 月末から最後の土曜日まで進める
  while gcday_last.weekday() != 5:
    gcday_last = gcday_last + datetime.timedelta(days=1)
  days = []
  daynow = gcday_first
  while True:
    days.append(daynow)
    if daynow == gcday_last:
      break
    daynow = daynow + datetime.timedelta(days=1)
  # リレーション先の値を抽出条件にしてフィルタする
  gcdayData = GcDay.objects.filter(area__pk=area.pk).filter(gcdate__gte=gcday_first).filter(gcdate__lte=gcday_last)

  daysData = list()

  for d in days:
    addData = {'day': d.strftime("%d日"), 'dow': jpdow(d), 'gcday': None}
    fil = gcdayData.filter(gcdate=d)
    # print(fil)
    if fil.count() == 0:
      None
    else:
      addData['gcday'] = fil[0]
    # print(addData)
    if d == today:
      addData['cell_class'] = 'today'
    else:
      addData['cell_class'] = ''
    daysData.append(addData)

  context = {
    'days': daysData,
    'area_name': area.name,
  }
  return render(request, 'gccalendar/area_monthly.html', context)
  # return HttpResponse(f'stub y={y}, m={m}, first={gcday_first}, last={gcday_last}, days={days}')