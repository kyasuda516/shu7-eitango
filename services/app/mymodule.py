import os
from pathlib import Path
import redis
from datetime import datetime
import mysql.connector
from mysql.connector.cursor import MySQLCursor

DISABLE_API = os.environ.get('DISABLE_API', '').lower() in ('1', 'true')
MYSQL_HOST = 'db'
MYSQL_PORT = '3306'
REDIS_HOST = 'cache'
REDIS_PORT = '6379'
REDIS_DB_PAGE_FILE = '/run/secrets/cache_db_page'
REDIS_DB_LIMS_FILE = '/run/secrets/cache_db_limits'
REDIS_DB_PRON_FILE = '/run/secrets/cache_db_pron'
WORDSAPI_KEY_FILE = '/run/secrets/wordsapi_key'
LOG_DIR = Path(__file__).parent / 'log'
if not LOG_DIR.exists(): LOG_DIR.mkdir()
PRON_KEY_FORMAT = 'wordsapi/pron/{pos}/{word}'
DAYS = {
  day_name[:3].lower(): {
    'id': index, 
    'name': day_name,
    'caption': f'{day_name[:3]}.',
    'bunch_name': f"{day_name}'s Bunch",
  }
  for index, day_name
  in enumerate([
    'Sunday',
    'Monday', 
    'Tuesday', 
    'Wednesday', 
    'Thursday', 
    'Friday', 
    'Saturday', 
  ])
}
POSES = {
  '冠詞':   'definite article' ,
  '副詞':   'adverb' ,
  # '文字':   'letter' ,
  # '不定詞': 'to' ,
  '名詞':   'noun' ,
  '前置詞': 'preposition' ,
  '形容詞': 'adjective' ,
  '動詞':   'verb' ,
  '接続詞': 'conjunction' ,
  # '間投詞': 'interjection' ,
  # '未分類': 'unclassified' ,
  # '限定詞': 'determiner' ,
  '代名詞': 'pronoun' ,
  # '数詞':   'number' ,
  # '否定詞': 'not' ,
  # '例外':   'ex' ,
}

def get_const_value(const_name: str) -> str:
  filepath_env_name = f'{const_name}_FILE'
  if filepath_env_name in globals():
    with open(eval(filepath_env_name)) as f: return f.readline()
  elif const_name in globals():
    return eval(const_name)
  elif filepath_env_name in os.environ:
    with open(os.environ[filepath_env_name]) as f: return f.readline()
  elif const_name in os.environ:
    return os.environ[const_name]
  else:
    raise ValueError(f'Varievle {const_name} is not defined.')

def seconds_until(time_string: str) -> int:
  """time_stringまでの秒数を取得
  
  time_string: "20:11:56" または "20:11" という形で指定
  """

  h, m, *s = [int(elem) for elem in time_string.split(':')]
  s = s[0] if len(s) > 0 else 0
  now = datetime.now()
  sec = (now.replace(hour=h, minute=m, second=s) - now).total_seconds() % (24*60*60)
  return int(sec)  # 小数点以下切り捨て

class DbCursor(MySQLCursor):
  """With文で横着できるMySQLカーソル"""
  def __new__(cls):
    cnx = mysql.connector.connect(
      host=MYSQL_HOST,
      port=MYSQL_PORT,
      user=get_const_value('MYSQL_USER'),
      password=get_const_value('MYSQL_PASSWORD'),
      database=get_const_value('MYSQL_DATABASE'),
    )
    self = cnx.cursor(dictionary=True)
    self.cnx = cnx
    return self
  
  def __enter__(self):
    return self
  
  def __exit__(self, exception_type, exception_value, traceback):
    self.close()
  
  def close(self):
    super().close()
    self.cnx.close()

class CacheClient():
  """SingletonパターンのRedisクライアント（ただし、発音用のデータベースと接続）"""
  __pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=get_const_value('REDIS_DB_PRON'),
    password=get_const_value('REDIS_PASSWORD'),
  )

  def __new__(cls):
    if not hasattr(cls, "_instance"):
      cls._instance = redis.Redis(connection_pool=cls.__pool)
    return cls._instance