import mymodule
import requests
from logging import getLogger, INFO
from logging.handlers import TimedRotatingFileHandler
from time import time
from datetime import time as create_time
import limits

class WordsAPI():
  headers = {
    'X-RapidAPI-Key': mymodule.get_const_value('WORDSAPI_KEY'),
    'X-RapidAPI-Host': 'wordsapiv1.p.rapidapi.com'
  }

  logger = getLogger(f'{__name__}::WordsAPI')
  logger.addHandler(TimedRotatingFileHandler(
    filename=mymodule.LOG_DIR / 'wordsapi.log', 
    when='MIDNIGHT',
    backupCount=7,
    encoding='UTF-8',
    delay=False,
    atTime=create_time(0, 0, 30),
  ))
  logger.setLevel(INFO)

  storage = limits.storage.RedisStorage(
    f'redis://:{mymodule.get_const_value("REDIS_PASSWORD")}@{mymodule.REDIS_HOST}'
    f':{mymodule.REDIS_PORT}/{mymodule.get_const_value("REDIS_DB_LIMS")}'
  )
  limiter = limits.strategies.MovingWindowRateLimiter(storage)
  rate_limit = limits.parse('200/2hours')
  
  def get_pronunciation(self, pos: str, word: str) -> str:
    pron = '-'

    if self.limiter.hit(self.rate_limit, 'WordsAPI'):
      if mymodule.DISABLE_API:
        from random import randint, choice
        from time import sleep
        sleep(0.3)
        pron = ''.join([choice('ʌ æ ɑː əː ə ai au iː i iə u uː uə e ei eə ɔ ɔː ɔi ou p b t d k g f v θ ð s z ʃ ʒ ʧ ʤ h l r w j m n ŋ'.split(' ')) for _ in range(randint(5, 16))])
        time_request = time()
        res_code = 600
        res_sec = 0.

      else:
        url = f'https://wordsapiv1.p.rapidapi.com/words/{word}/pronunciation'
        time_request = time()
        res = requests.get(url, headers=self.headers)
        res_sec = time() - time_request
        res_code = res.status_code

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
              pron = prons.get(pos, False) or prons.get('all', pron)
            elif isinstance(prons, str):
              pron = str(prons)

    else:
      res_code = 629
      time_request = time()
      res_sec = 0.
    
    self.logger.info(
      f'time:{time_request:.9f}\tword:{word}\tres_code:{res_code}\tres_sec:{res_sec:.6f}\tpron:{pron}')
    return pron

def main(cache_until: str):
  api = WordsAPI()
  cache_cli = mymodule.CacheClient()
  with mymodule.DbCursor() as cur:
    for bunch_id in range(7):
      table = f'bunch{bunch_id}'
      cur.execute(f'SELECT `pos`, `word` FROM `{table}`')
      cards = cur.fetchall()
      for card in cards:
        pos_ja = card['pos']                              # POS(日本語)
        pos = mymodule.POSES.get(pos_ja, 'unclassified')  # POS(英語)
        word = card['word']
        pron = api.get_pronunciation(pos, word)
        pron_bytes = pron.encode('utf-8')
        cache_cli.setex(
          name=mymodule.PRON_KEY_FORMAT.format(pos=pos, word=word), 
          time=mymodule.seconds_until(cache_until), 
          value=pron_bytes
        )

if __name__ == '__main__':
  from sys import argv
  assert len(argv) == 2
  main(argv[1])