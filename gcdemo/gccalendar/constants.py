# 静的定義変数集
from datetime import datetime

const_dowstr = ['日','月','火','水','木','金','土']


def jpdow(dt : datetime):
  """
  datetimeオブジェクトから曜日の1文字分を出力する。

  Parameters
  ----------
  dt : datetime
    変換対象のdatetimeオブジェクト
  
  Returns
  -------
  dow_jpstr : str
    日月火水木金土のうちのどれか
  """
  return const_dowstr[int(dt.strftime("%w"))]