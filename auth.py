import os
from pathlib import Path  # python3 only

import spotipy
import spotipy.util as util
from dotenv import load_dotenv


def get_token():
  load_dotenv(dotenv_path=Path('.') / '.env', verbose=True)
  SPOTIPY_CLIENT_ID     = os.getenv("SPOTIPY_CLIENT_ID")
  SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
  SPOTIPY_REDIRECT_URI  = os.getenv("SPOTIPY_REDIRECT_URI")
  SCOPE                 = 'playlist-read-collaborative playlist-modify-private playlist-modify-public playlist-read-private user-read-private user-read-playback-state user-modify-playback-state user-library-read user-library-modify'
  USERNAME              = os.getenv("USERNAME")
  return util.prompt_for_user_token(USERNAME, SCOPE, SPOTIPY_CLIENT_ID,
                                     SPOTIPY_CLIENT_SECRET,
                                     SPOTIPY_REDIRECT_URI), USERNAME

def init():
  global token, sp, agg_report
  token, username = get_token()
  sp = spotipy.Spotify(auth=token)
  agg_report = []
  return username

#   results = sp.current_user_saved_tracks()
#   for item in results['items']:
#     track = item['track']
#     print(track['name'] + ' - ' + track['artists'][0]['name'])
# else:
#   print("Can't get token for", USERNAME)

