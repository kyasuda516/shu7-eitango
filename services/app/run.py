from flask import Flask
from flask import make_response
from flask import render_template
from flask import redirect
from flask_caching import Cache
from flask_caching import CachedResponse
# from flask_cors import CORS
from werkzeug.debug import DebuggedApplication
import os
from datetime import date
import mymodule

app = Flask(__name__)
if os.environ.get('DEBUG_MODE', '').lower() in ('1', 'true'):
  app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
  app.debug = True

cache = Cache(app, config={
  'CACHE_TYPE': 'redis',
  'CACHE_REDIS_HOST': mymodule.REDIS_HOST,
  'CACHE_REDIS_PORT': mymodule.REDIS_PORT,
  'CACHE_REDIS_PASSWORD': mymodule.get_const_value('REDIS_PASSWORD'),
  'CACHE_REDIS_DB': mymodule.get_const_value('REDIS_DB_PAGE'),
  'CACHE_DEFAULT_TIMEOUT': 60,
})

@app.context_processor
def utility_processor():
  return dict(days=mymodule.DAYS)

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
  return render_template('error_404.html'), 404

@app.route('/bunch', methods=['GET'])
def get_today_bunch():
  day_id = (date.today().weekday()+1)%7
  day_sym = [day_sym for day_sym, day in mymodule.DAYS.items() if day['id']==day_id][0]
  return redirect(f'/bunch/{day_sym}')

@app.route('/bunch/<string:day_sym>', methods=['GET'])
@cache.cached()
def get_bunch(day_sym):
  if day_sym in mymodule.DAYS:
    pass
  elif day_sym.lower() in mymodule.DAYS:
    return redirect(f'/bunch/{day_sym.lower()}')
  elif day_sym not in mymodule.DAYS:
    return render_template('error_404.html'), 404

  table = f'bunch{mymodule.DAYS[day_sym]["id"]}'
  with mymodule.DbCursor() as cur:
    # カードを取得
    cur.execute(f'SELECT * FROM `{table}`')
    cards = cur.fetchall()

    # 日付を取得
    # cur.execute(f'SHOW TABLE STATUS WHERE name='{table}'')
    # created = cur.fetchone()['Create_time']
    cur.execute(f"SELECT `CREATE_TIME` FROM INFORMATION_SCHEMA.PARTITIONS WHERE `TABLE_NAME`='{table}'")
    dt = list(cur.fetchone().values())[0]
    date = f'{dt.year}年{dt.month}月{dt.day}日'

  # それぞれのカードについて発音を取得
  cache_cli = mymodule.CacheClient()
  for card in cards:
    pos_ja = card['pos']                              # POS(日本語)
    pos = mymodule.POSES.get(pos_ja, 'unclassified')  # POS(英語)
    pron_bytes = cache_cli.get(mymodule.PRON_KEY_FORMAT.format(pos=pos, word=card['word']))
    pron = '-' if pron_bytes is None else pron_bytes.decode('utf-8')
    card['pron'] = pron

  response = make_response(render_template(
    'bunch.html',
    this_day_sym=day_sym,
    cards=cards,
    created_date=date,
  ))
  timeout = 1 if os.environ.get('DEBUG_MODE', '').lower() in ('1', 'true') else mymodule.seconds_until("6:00:00")
  # Note: 0ではデフォルトの一定秒数になるので1で1秒に
  return CachedResponse(
    response=response,
    timeout=timeout,
  )