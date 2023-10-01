import os
import requests
from logging import getLogger, INFO
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from time import time
from datetime import time as create_time
import limits
import redis
from datetime import datetime

AVOID_API = os.environ.get('AVOID_API') in ('1', 1, 'True', True)

LOG_DIR = Path(__file__).parent / 'log'
if not LOG_DIR.exists(): LOG_DIR.mkdir()

def get_const_value(const_name: str) -> str:
  filepath_env_name = f'{const_name}_FILE'
  if filepath_env_name in os.environ and os.path.exists(os.environ[filepath_env_name]):
    with open(os.environ[filepath_env_name], 'r') as f:
      return f.readline()
  elif const_name in os.environ:
    return os.environ[const_name]
  else:
    raise ValueError(f'Varievle {const_name} is not defined.')

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_PASSWORD = get_const_value('REDIS_PASSWORD')
REDIS_DB = get_const_value('REDIS_DATABASE')       # ページキャッシュ用
REDIS_DB2 = get_const_value('REDIS_DATABASE2')     # API呼び出し監視用
REDIS_DB3 = get_const_value('REDIS_DATABASE3')     # 発音データのキャッシュ用

def get_timeout() -> int:
  HH, MM, SS = 6, 1, 30
  now = datetime.now()
  sec = (now.replace(hour=HH, minute=MM, second=SS) - now).total_seconds() % (24*60*60)
  return int(sec)

class WordsAPI():
  headers = {
    'X-RapidAPI-Key': get_const_value('WORDSAPI_KEY'),
    'X-RapidAPI-Host': 'wordsapiv1.p.rapidapi.com'
  }

  logger = getLogger(f'{__name__}::WordsAPI')
  logger.addHandler(TimedRotatingFileHandler(
    filename=LOG_DIR / 'wordsapi.log', 
    when='MIDNIGHT',
    backupCount=7,
    encoding='UTF-8',
    delay=False,
    atTime=create_time(0, 0, 30),
  ))
  logger.setLevel(INFO)

  storage = limits.storage.RedisStorage(f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB2}')
  limiter = limits.strategies.MovingWindowRateLimiter(storage)
  rate_limit = limits.parse('200/2hours')

  pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB3,
    password=REDIS_PASSWORD,
  )
  redis_cli = redis.Redis(connection_pool=pool)
  pron_key_preffix = 'wordsapi/pron/'

  def get_pronunciation(self, word) -> str:
    pron_bytes = self.redis_cli.get(f'{self.pron_key_preffix}{word}')
    pron = None if pron_bytes is None else pron_bytes.decode('utf-8')

    # AVOID_API = False         # 必ず消す！！！☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★☆★
    if not AVOID_API and pron is None and self.limiter.hit(self.rate_limit, 'WordsAPI'):
      from random import randint, choice
      from time import sleep
      sleep(0.1)
      pron = ''.join([choice(list('零壱弐参肆伍陸漆捌玖')) for _ in range(randint(4, 12))])
      time_request = time()
      res_code = 2200
      res_sec = 0.

      # url = f'https://wordsapiv1.p.rapidapi.com/words/{word}/pronunciation'
      # time_request = time()
      # res = requests.get(url, headers=self.headers)
      # res_sec = time() - time_request
      # res_code = res.status_code

      # decoded = True
      # try:
      #   data = res.json()
      # except requests.exceptions.JSONDecodeError:
      #   decoded = False
      
      # pron = '-'
      # if decoded:
      #   data = data[0] if isinstance(data, list) else data
      #   if isinstance(data, dict):
      #     prons = data.get('pronunciation', pron)
      #     if isinstance(prons, dict):
      #       pron = prons.get('all', pron)
      #       # pron = prons.get(pos, False) or prons.get('all', pron)
      #       # pos として有効なのはとりあえず verb noun adjective adverb がある
      #     elif isinstance(prons, str):
      #       pron = prons
      
      pron_bytes = pron.encode('utf-8')
      self.redis_cli.setex(f'{self.pron_key_preffix}{word}', get_timeout(), pron_bytes)
    
    else:
      if AVOID_API: 
        pron = pron or 'Avoided!'
        res_code = 603
      elif pron is not None:
        res_code = 600
      else:
        pron = '-'
        res_code = 629
      time_request = time()
      res_sec = 0.
    
    self.logger.info(f'time:{time_request:.9f}\tword:{word}\tres_code:{res_code}\tres_sec:{res_sec:.6f}\tpron:{pron}')
    return pron