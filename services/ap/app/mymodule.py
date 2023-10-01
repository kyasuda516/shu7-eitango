import os
import requests
from logging import getLogger, INFO
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from time import time
from datetime import time as create_time
import limits

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
# REDIS_DB3 = get_const_value('REDIS_DATABASE3')     # 発音データのキャッシュ用

class WordsAPI():
  headers = {
    'X-RapidAPI-Key': get_const_value('WORDSAPI_KEY'),
    'X-RapidAPI-Host': 'wordsapiv1.p.rapidapi.com'
  }
  i = 1

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

  def get_pronunciation(self, word) -> str:
    pron = '-'

    if AVOID_API or not self.limiter.hit(self.rate_limit, 'WordsAPI'):
      time_request = time()
      res_code = 429
      res_sec = 0.
    else:
      pron = 'success'
      time_request = time()
      res_code = 2200
      res_sec = 0.

      # url = f'https://wordsapiv1.p.rapidapi.com/words/{word}/pronunciation'
      # time_request = time()
      # res = requests.get(url, headers=self.headers)
      # res_sec = time() - time_request
      # res_code = res.status_code

      # self.i += 1

      # decoded = True
      
      # try:
      #   data = res.json()
      # except requests.exceptions.JSONDecodeError:
      #   decoded = False
      
      # if decoded:
      #   data = data[0] if isinstance(data, list) else data
      #   if isinstance(data, dict):
      #     prons = data.get('pronunciation', pron)
      #     if isinstance(prons, dict):
      #       pron = data.get('all', pron)
      #     elif isinstance(prons, str):
      #       pron = prons
    
    self.logger.info(f'time:{time_request:.9f}\tword:{word}\tres_code:{res_code}\tres_sec:{res_sec:.6f}\tpron:{pron}')
    return pron