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
    return word
    url = f'https://wordsapiv1.p.rapidapi.com/words/{word}/pronunciation'
    res = requests.get(url, headers=self.headers)
    data = res.json()
    try:
      pron = data['pronunciation']['all']
    except:
      pron = word
    self.logger.info(f'time:{time.time():.9f}\tres_code:{res.status_code}\tword:{word}\tpron:{pron}')
    self.i += 1
    return pron