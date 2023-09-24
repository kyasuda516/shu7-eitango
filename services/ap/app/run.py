from flask import Flask
from flask import render_template
from flask import redirect
from flask_caching import Cache
# from flask_cors import CORS
from werkzeug.debug import DebuggedApplication
import mysql.connector
import os
from datetime import date, datetime

app = Flask(__name__)
if os.environ.get('DEBUG_MODE') in ('1', 1, 'True', True):
  app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
  app.debug = True

def get_const_value(const_name: str) -> str:
  filepath_env_name = f'{const_name}_FILE'
  if filepath_env_name in os.environ and os.path.exists(os.environ[filepath_env_name]):
    with open(os.environ[filepath_env_name], 'r') as f:
      return f.readline()
  elif const_name in os.environ:
    return os.environ[const_name]
  else:  
    raise ValueError(f'Varievle {const_name} is not defined.')

if not os.environ.get('DEBUG_MODE') in ('1', 1, 'True', True):
  cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_HOST': os.environ['REDIS_HOST'],
    'CACHE_REDIS_PORT': os.environ['REDIS_PORT'],
    'CACHE_REDIS_PASSWORD': get_const_value('REDIS_PASSWORD'),
    'CACHE_REDIS_DB': get_const_value('REDIS_DATABASE'),
    'CACHE_DEFAULT_TIMEOUT': 60,
  })

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

def get_timeout():
  HH, MM, SS = 6, 0, 30
  now = datetime.now()
  sec = (now.replace(hour=HH, minute=MM, second=SS) - now).total_seconds() % (24*60*60)
  return int(sec)

@app.context_processor
def utility_processor():
  return dict(days=DAYS)

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
  return render_template('error_404.html'), 404

@app.route('/bunch', methods=['GET'])
def get_today_bunch():
  day_id = (date.today().weekday()+1)%7
  day_sym = [day_sym for day_sym, day in DAYS.items() if day['id']==day_id][0]
  return redirect(f'/bunch/{day_sym}')

# @app.route('/bunch/<string:day_sym>', methods=['GET'])    # ほんとはこう書きたいが、デバッグ用の分岐のために
# @cache.cached(timeout=get_timeout())                      # 代わりとなるコードを *1 に後述する。
def get_bunch(day_sym):
  if day_sym in DAYS:
    pass
  elif day_sym.lower() in DAYS:
    return redirect(f'/bunch/{day_sym.lower()}')
  elif day_sym not in DAYS:
    return render_template('error_404.html'), 404

  cnx = mysql.connector.connect(
    host=os.environ['MYSQL_HOST'],
    port=os.environ['MYSQL_PORT'],
    user=get_const_value('MYSQL_USER'),
    password=get_const_value('MYSQL_PASSWORD'),
    database=get_const_value('MYSQL_DATABASE'),
  )
  table = f'bunch{DAYS[day_sym]["id"]}'
  cur = cnx.cursor(dictionary=True)

  # カードを取得
  cur.execute(f'SELECT * FROM `{table}`')
  cards = cur.fetchall()

  # 日付を取得
  # cur.execute(f'SHOW TABLE STATUS WHERE name='{table}'')
  # created = cur.fetchone()['Create_time']
  cur.execute(f"SELECT `CREATE_TIME` FROM INFORMATION_SCHEMA.PARTITIONS WHERE `TABLE_NAME`='{table}'")
  dt = list(cur.fetchone().values())[0]
  date = f'{dt.year}年{dt.month}月{dt.day}日'
  print(date)

  cnx.close()

  return render_template(
    'bunch.html', 
    this_day_sym=day_sym,
    cards=cards,
    created_date=date,
  )

if not os.environ.get('DEBUG_MODE') in ('1', 1, 'True', True):                # ここから *1
  get_bunch = cache.cached(timeout=get_timeout())(get_bunch)
get_bunch = app.route('/bunch/<string:day_sym>', methods=['GET'])(get_bunch)  # ここまで
