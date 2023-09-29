import os
# import requests

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

  def get_pronunciation(self, word):
    # url = f'https://wordsapiv1.p.rapidapi.com/words/{word}/pronunciation'
    # res = requests.get(url, headers=self.headers)
    # return res.json()['pronunciation']['all']
    return word