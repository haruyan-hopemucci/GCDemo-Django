from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.template import loader
from .models import *
from .constants import *
from .forms import *

import datetime

def index(request):
  print(request.user.username)
  if not request.user.is_staff:
    return HttpResponseForbidden()
  context = {
    'user': request.user
  }
  return render(request, 'gccalendar/admin/index.html', context)

def area_list(request):
  areas = Area.objects.all()
  context = {
    'areas' : areas
  }
  return render(request, 'gccalendar/admin/area-list.html', context)

def area_new(request):
  # message_bodyやmessage_type_classは警告やエラーなどのメッセージに使う。
  context = {
    'message_body' : "",
    'message_type_class' : "no-message",
    'form' : None
  }
  # getリクエストなら新規作成の新規画面、postリクエストなら入力後の内容になるはず。
  if request.method == "POST":
    # postメソッドの場合、リクエスト内容からformオブジェクトを作成する。
    form = AreaForm(request.POST)
    # Formクラス側との定義とバリデーションする。ModelFormの場合は元のモデルとのバリデーション。
    if form.is_valid():
      # saveメソッドで保存するだけ。
      form.save()
      return redirect('admin_area_list')
    else:
      # バリデーションチェックに引っかかった場合
      context['message_body'] = "入力値が不正です。"
      context['message_type_class'] = 'danger'
      context['form'] = form
  else:
    # getメソッドの場合は、空のフォームを送信。
    context['form'] = AreaForm()
  return render(request, 'gccalendar/admin/area-new.html', context)

def area_edit(request, area_id):
  context = {
    'message_body' : "",
    'message_type_class' : "no-message",
    'form' : None
  }
  if request.method == "POST":
    # 編集内容を送信された状態。
    # POSTの内容とともに、instanceパラメータに更新対象のオブジェクトをセットする。
    # そうしないとsave時に新規レコード扱いになってしまう。
    form = AreaForm(request.POST, instance=Area.objects.get(pk=area_id))
    if form.is_valid():
      form.save()
      return redirect('admin_area_list')
    else:
      context['message_body'] = "入力値が不正です。"
      context['message_type_class'] = 'danger'
      context['form'] = form
  else:
    # 編集前の状態。
    # instanceパラメータに更新対象のオブジェクトをセットする。
    context['form'] = AreaForm(instance=Area.objects.get(pk=area_id))
    
  return render(request, 'gccalendar/admin/area-edit.html', context)

def area_delete(request, area_id):
  context = {
    'message_body' : "",
    'message_type_class' : "no-message",
    'areas' : None
  }
  # objects.getで取得する場合、pkが存在しない値の場合は例外になってしまう。
  # filterで取得すればexistsメソッドで存在するかどうかの判定ができる。
  target = Area.objects.filter(pk=area_id)
  if target.exists():
    # 対象のidのレコードが存在すればdelete.
    target.delete()
    context['message_body'] = f"id:{area_id}を削除しました。"
    context['message_type_class'] = 'success'
    context['areas'] = Area.objects.all()
  else:
    # 対象のidのレコードが存在しなければエラーメッセージ.
    context['message_body'] = "不正な入力値です。"
    context['message_type_class'] = 'danger'
    context['areas'] = Area.objects.all()

  return render(request, 'gccalendar/admin/area-list.html', context)
  
def gcday_new(request):
  context = {
    'message_body' : "",
    'message_type_class' : "no-message",
    'form' : None
  }
  if request.method == "POST":
    form = GCDayForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('admin_area_list')
    else:
      context['message_body'] = "入力値が不正です。"
      context['message_type_class'] = 'danger'
      context['form'] = form
  else:
    context['form'] = GCDayForm()
  return render(request, 'gccalendar/admin/gcday-new.html', context)

def gcday_delete(request, gcday_id):
  context = {
    'message_body' : "",
    'message_type_class' : "no-message",
    'areas' : None
  }
  target = GcDay.objects.filter(pk=gcday_id)
  if target.exists():
    target.delete()
    context['message_body'] = f"id:{gcday_id}を削除しました。"
    context['message_type_class'] = 'success'
    context['areas'] = GcDay.objects.all()
  else:
    context['message_body'] = "不正な入力値です。"
    context['message_type_class'] = 'danger'
    context['areas'] = GcDay.objects.all()

  return render(request, 'gccalendar/admin/area-list.html', context)

def gctype_list(request):
  gctypes = GcType.objects.all()
  context = {
    'gctypes' : gctypes
  }
  return render(request, 'gccalendar/admin/gctype-list.html', context)

def gctype_new(request):
  context = {
    'message_body' : "",
    'message_type_class' : "no-message",
    'form' : None
  }
  if request.method == "POST":
    # 引数にPOSTデータとFILESデータの両方を指定しなければならない。
    form = GCTypeForm(request.POST, request.FILES)
    if(form.is_valid()):
      model = GcType()
      model.name = form.cleaned_data['name']
      import base64
      # 画像をbase64エンコードしてテキストとして保存する。
      # b64encodeしたデータはバイナリなので、decode関数でstringに変換しなければならないようだ。
      # 大きなファイルを扱わないようにサイズ制限すると良いかと。デフォルトでは2.5MB未満のファイルはインメモリで処理されるとのこと。
      model.imagebase64 = base64.b64encode(request.FILES['image'].read()).decode()
      model.save()
      context['message-body'] = "保存しました。"
      context['message-type_class'] = 'success'
      context['form'] = GCTypeForm()
    else:
      context['message-body'] = "不正な入力値です。"
      context['message-type_class'] = 'danger'
      context['form'] = form
  else:
    # 新規作成時は引数無しでOK
    context['form'] = GCTypeForm()
  return render(request, 'gccalendar/admin/gctype-new.html', context)

def gctype_delete(request, gctype_id):
  context = {
    'message_body' : "",
    'message_type_class' : "no-message",
    'gctypes' : None
  }
  target = GcType.objects.filter(pk=gctype_id)
  if target.exists():
    target.delete()
    context['message_body'] = f"id:{gctype_id}を削除しました。"
    context['message_type_class'] = 'success'
    context['gctypes'] = GcType.objects.all()
  else:
    context['message_body'] = "不正な入力値です。"
    context['message_type_class'] = 'danger'
    context['gctypes'] = GcType.objects.all()

  return render(request, 'gccalendar/admin/gctype-list.html', context)

def gctype_edit(request, gctype_id):
  context = {
    'message_body' : "",
    'message_type_class' : "no-message",
    'form' : None
  }
  if request.method == "POST":
    form = GCTypeEditForm(request.POST, request.FILES)
    if(form.is_valid()):
      model = GcType.objects.get(pk=gctype_id)
      model.name = form.cleaned_data['name']
      if len(request.FILES) > 0:
        import base64
        # 画像をbase64エンコードしてテキストとして保存する。
        # b64encodeしたデータはバイナリなので、decode関数でstringに変換しなければならないようだ。
        # 大きなファイルを扱わないようにサイズ制限すると良いかと。デフォルトでは2.5MB未満のファイルはインメモリで処理されるとのこと。
        model.imagebase64 = base64.b64encode(request.FILES['image'].read()).decode()
      model.save()
      context['message_body'] = "更新しました。"
      context['message_type_class'] = 'success'
      context['form'] = form
      print(context)
  else:
    obj = GcType.objects.get(pk=gctype_id)
    initData = { 'name': obj.name}
    form = GCTypeEditForm(initial=initData)
    form.name = obj.name
    context['form'] = form
    
  return render(request, 'gccalendar/admin/gctype-edit.html', context)

def gcdays_bulk_setting(request):
  context = {
    'message_body' : "",
    'message_type_class' : "no-message",
    'form' : None
  }
  if request.method == "POST":
    form = GCDayBulkSettingForm(request.POST)
    if form.is_valid():
      # 当年度の既存のデータを削除し、新しいデータを挿入
      year = int(form.cleaned_data['year'])
      area = form.cleaned_data['area']
      gctype = form.cleaned_data['gctype']
      date_from = datetime.date(year,1,1)
      date_to = datetime.date(year+1,1,1)
      target = GcDay.objects.filter(area=area).filter(gctype=gctype).filter(gcdate__gte=date_from).filter(gcdate__lt=date_to)
      # print(target)
      target.delete()
      # 対象の日付リストを作成
      datelist = []
      targetDow = []
      targetWom = []
      if form.cleaned_data['checkSun']:
        targetDow.append(6)
      if form.cleaned_data['checkMon']:
        targetDow.append(0)
      if form.cleaned_data['checkTue']:
        targetDow.append(1)
      if form.cleaned_data['checkWed']:
        targetDow.append(2)
      if form.cleaned_data['checkThu']:
        targetDow.append(3)
      if form.cleaned_data['checkFri']:
        targetDow.append(4)
      if form.cleaned_data['checkSat']:
        targetDow.append(5)
      if form.cleaned_data['checkWeek1']:
        targetWom.append(1)
      if form.cleaned_data['checkWeek2']:
        targetWom.append(2)
      if form.cleaned_data['checkWeek3']:
        targetWom.append(3)
      if form.cleaned_data['checkWeek4']:
        targetWom.append(4)
      if form.cleaned_data['checkEveryWeek']:
        targetWom = [1,2,3,4,5,6]
      date_curr = date_from
      date_prev = date_from - datetime.timedelta(days=1)
      date_Wom = 1
      while date_curr < date_to:
        # print('curr:',date_curr)
        if date_curr.weekday() in targetDow and date_Wom in targetWom:
          datelist.append(date_curr)
        date_prev = date_curr
        date_curr = date_curr + datetime.timedelta(days=1)
        if date_curr.weekday() == 6:
          date_Wom = date_Wom + 1
        # if date_curr.month > date_prev.month:
        #   date_Wom = 1
        date_Wom = date_curr.day // 7 + 1
      
      insertObjs = []
      for d in datelist:
        gcday = GcDay()
        gcday.area = area
        gcday.gcdate = d
        gcday.gctype = gctype
        insertObjs.append(gcday)
      
      # print(insertObjs)
      GcDay.objects.bulk_create(insertObjs)

      context['message_body'] = "データが作成されました。"
      context['message_type_class'] = 'success'
      context['form'] = form
    else:
      context['message_body'] = "不正な入力値です。"
      context['message_type_class'] = 'danger'
      context['form'] = form
  else:
    context['form'] = GCDayBulkSettingForm()
  return render(request, 'gccalendar/admin/gcdays-bulk-setting.html', context)
