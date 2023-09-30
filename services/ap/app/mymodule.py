import os
import requests
from logging import getLogger, FileHandler, INFO
from pathlib import Path
import time

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

class WordsAPI():
  headers = {
    'X-RapidAPI-Key': get_const_value('WORDSAPI_KEY'),
    'X-RapidAPI-Host': 'wordsapiv1.p.rapidapi.com'
  }
  i = 1
  logger = getLogger(f'{__name__}::WordsAPI')
  logger.addHandler(FileHandler(
    filename=LOG_DIR / 'wordsapi.log', encoding='UTF-8'
  ))
  logger.setLevel(INFO)

  def get_pronunciation(self, word):
    self.logger.info(f'time:{time.time():.9f}\tword:{word}\tres_code:999\tres_sec:0.000000\tpron:-')
    return '-'
    url = f'https://wordsapiv1.p.rapidapi.com/words/{word}/pronunciation'
    time_request = time.time()
    res = requests.get(url, headers=self.headers)
    res_sec = time.time() - time_request
    self.i += 1

    pron = '-'
    decoded = True
    
    try:
      data = res.json()
    except requests.exceptions.JSONDecodeError:
      decoded = False
    
    if decoded:
      data = data[0] if isinstance(data, list) else data
      if isinstance(data, dict):
        prons = data.get('pronunciation', pron)
        if isinstance(prons, dict):
          pron = data.get('all', pron)
        elif isinstance(prons, str):
          pron = prons
    
    self.logger.info(f'time:{time_request:.9f}\tword:{word}\tres_code:{res.status_code}\tres_sec:{res_sec:.6f}\tpron:{pron}')
    return pron