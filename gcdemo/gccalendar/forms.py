from sys import maxsize
from django import forms
from django.db import models
from .models import *

class AreaForm(forms.ModelForm):
  class Meta:
    model = Area
    fields = ['name']
    labels = { 'name': 'エリア名'}
    help_texts = { 'name': 'エリア名を入力してください'}

class GCDayForm(forms.ModelForm):
  class Meta:
    model = GcDay
    fields = ['area', 'gcdate', 'gctype']

class GCTypeForm(forms.Form):
  name = forms.CharField(label="ごみ分別名", max_length=80)
  # フォームでファイル送信を扱うにはFileFieldを使う。
  image = forms.FileField(label="アイコン")

class GCTypeEditForm(forms.Form):
  name = forms.CharField(label="ごみ分別名", max_length=80)
  image = forms.FileField(label="アイコン", required=False)

class GCDayBulkSettingForm(forms.Form):
  gctype = forms.ModelChoiceField(GcType.objects, label="ごみ分別種類")
  area = forms.ModelChoiceField(Area.objects, label="対象エリア")
  year = forms.CharField(label="年度", max_length=4)
  checkSun = forms.BooleanField(label="日曜日", required=False)
  checkMon = forms.BooleanField(label="月曜日", required=False)
  checkTue = forms.BooleanField(label="火曜日", required=False)
  checkWed = forms.BooleanField(label="水曜日", required=False)
  checkThu = forms.BooleanField(label="木曜日", required=False)
  checkFri = forms.BooleanField(label="金曜日", required=False)
  checkSat = forms.BooleanField(label="土曜日", required=False)
  checkEveryWeek = forms.BooleanField(label="毎週", required=False)
  checkWeek1 = forms.BooleanField(label="第1週", required=False)
  checkWeek2 = forms.BooleanField(label="第2週", required=False)
  checkWeek3 = forms.BooleanField(label="第3週", required=False)
  checkWeek4 = forms.BooleanField(label="第4週", required=False)
  def __init__(self, *args, **kwargs):
    super(GCDayBulkSettingForm, self).__init__(*args, **kwargs)
    for field in self.fields.values():
      # タグのクラス設定。bootstrap有効にするため。
      if field.__class__.__name__ == 'BooleanField':
        field.widget.attrs["class"] = "form-chekc-input"
      else:
        field.widget.attrs["class"] = "form-control"