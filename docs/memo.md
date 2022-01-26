# 作業メモ

## 環境設定

### venv

```cmd
python -m venv venv
.\venv\Scripts\activate
```

### djangoインストール

チュートリアルを見ながら進める
https://docs.djangoproject.com/ja/4.0/intro/tutorial01/

```cmd
pip install django
pip freeze > requirements.txt
```

### プロジェクト作成

プロジェクト名は"gcdemo"にする。

```
django-admin startproject gcdemo
cd gcdemo
gcdemo> python manage.py runserver # 動作した
cd ..
python gcdemo/manage.py runserver   # これでもOK
```

### アプリケーションの作成

アプリケーションは"gccalendar"にする
```
python manage.py startapp gccalendar
```

あとは手順に従って`gccalendar/urls.py`と`gcdemo/urls.py`を適切に修正するとOK。

### データベースの準備

今回はsqliteを使うのでDBの事前設定は不要とのこと。
```
> python manage.py migrate
```
`gcdemo/db.sqlite3` というファイルが作成された。

### スーパーユーザー作成

```
> python manage.py createsuperuser
Username (leave blank to use 'haruyan'): admin
Email address: admin@example.com
Password: # gcdemo-admin とする
Password (again):
Superuser created successfully.
```

### 通常ユーザーの作成

アプリで使用する通常ユーザーを作成する。
http://127.0.0.1:8000/admin/
から先ほどのスーパーユーザーでログインし、
http://127.0.0.1:8000/admin/auth/user/
からユーザーを作成する。

```
username: haruyan
password: PYEx7t_HG#2E*Lh
```
パスワードはchromeが提案したもので。

## ログイン機能

### テンプレートディレクトリの設定

`gcdemo/settings.py`を修正
`INSTALLED_APPS`にgccalendarを追加する
こうすることで、Djangoのテンプレートエンジンがgccalendar/templatesディレクトリをテンプレート保管場所と認識してくれるようになる。

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gccalendar',
]
```
gccalendarディレクトリに`templates`ディレクトリを作成。
その中に`gccalendar`ディレクトリを作成
その中にindex.htmlを作成。
次にgccalendar/views.pyを修正。

```python
def index(request):
  # return HttpResponse("Hello, world. You're at the polls index.")
  return render(request, 'gccalendar/index.html')
```
これで、templates/gccalendar/index.htmlの内容がレンダリングされる。

### ログインページ作成

ここからは https://note.com/rhayahi/n/na21aef3b8ee2 を参考にする。

記事通りにlogin.htmlの作成
記事を参考にgccalendar/url.pyの設定

```python
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', auth_views.LoginView.as_view(template_name='login.html')),
]
```
gccalendarの方に追加した。

これで、`http://127.0.0.1:8000/gccalendar/login`でdjango組み込みのログインページが表示された。

実際に先ほど作った通常ユーザーでログインしてみると、

```
Page not found(404)
Request Method:	GET
Request URL:	http://127.0.0.1:8000/accounts/profile/
```

などと表示される。ログイン自体は成功しているが遷移先のURLにviewが設定されていない。

`gcdemo/urls.py`
```python:gcdemo/urls.py
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('accounts/profile/', views.profile),
    path('gccalendar/', include('gccalendar.urls')),
    path('admin/', admin.site.urls),
]
```
`accounts/profile/`へのpathを追加。実行する関数は`views.profile`。

`gcdemo/views.py`
```python:gcdemo/views.py
from django.shortcuts import render
from django.http import HttpResponse

def profile(request):
  return render(request, 'profile.html')
```

テンプレートディレクトリにprofile.htmlを作っておく。

ここまでの設定が完了したらログイン後profileページに遷移できる。

## データエントリー

### エンティティの追加

ER.drawio の通りエンティティ（area/収集地区, gcday/収集日, gctype/ごみ種類）を追加する。

`models.py`
```python
from django.db import models

# Create your models here.
class Area(models.Model):
  name = models.CharField(max_length=80)

class GcType(models.Model):
  name = models.CharField(max_length=80)
  imagebase64 = models.TextField()

class GcDay(models.Model):
  area = models.ForeignKey(Area, on_delete=models.CASCADE)
  gcdate = models.DateField()
  gctype = models.ForeignKey(GcType, on_delete=models.CASCADE)

```

モデルクラスを作ったらマイグレーションする。

```
> python manage.py makemigrations gccalendar
Migrations for 'gccalendar':
  gccalendar\migrations\0001_initial.py
    - Create model Area
    - Create model GcType
    - Create model GcDay
> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, gccalendar, sessions
Running migrations:
  Applying gccalendar.0001_initial... OK
```