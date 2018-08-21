import os
from datetime import *
from pprint import pprint

import auth

username = 'valeedm92'
db_history_path = "db/histories/"
watchlist_path = './db/watchlist'
week_num = str(datetime.today().isocalendar()[1])
year_num = str(datetime.now().year)[2:]
day_num = str(datetime.now().day)
date_tag = "[D" + day_num + "W" + week_num + "Y" + year_num + "]"



# def remove_dead_links():



# report creation
def generate_report(playlist_uri):
  new_playlist_report_uri = create_update_playlist(playlist_uri)
  if new_playlist_report_uri is not None:
    db_append_playlist(playlist_uri, new_playlist_report_uri)


def create_update_playlist(playlist_uri):
  new_tracks = diff_playlists(playlist_tracks(playlist_uri),
                              playlist_tracks_history(playlist_uri))
  print("LSKDJAF;LSJD;LQ;AJKDSFA;S " )
  pprint(new_tracks)
  if not new_tracks:
    return None
  else:
    return create_playlist(new_tracks, playlist_name(playlist_uri) + date_tag)


def create_playlist(track_uri_list, playlist_name):
  p = auth.sp.user_playlist_create(username, playlist_name, public=False)
  playlist_uri = p.get('uri')

  # Spotify limits you to adding 100 tracks at a time
  buffer = track_uri_list[:100]
  remainder_list = track_uri_list[100:]
  while len(buffer) > 0:
    auth.sp.user_playlist_add_tracks(username, playlist_uri, buffer)
    buffer = remainder_list[:100]
    remainder_list = remainder_list[100:]

  return playlist_uri


def playlist_name(playlist_uri):
  user, id = parse_uri(playlist_uri)
  name = auth.sp.user_playlist(user, id, fields='name').get('name')
  return str(name)


# Return a list of songs

def playlist_tracks_history(playlist_uri):
  l = db_get_history_playlists(playlist_uri)
  if l is None:
    return None

  track_history = playlist_group_tracks(l)
  return track_history


def playlist_group_tracks(playlist_uris):
  tracks = []
  for playlist_uri in playlist_uris:
    tracks += playlist_tracks(playlist_uri)
  return tracks


def playlist_tracks(playlist_uri):
  username, playlist_id = parse_uri(playlist_uri)

  items = scan_paginated_playlist(username, playlist_id)
  return get_uris(items)


def scan_paginated_playlist(username, playlist_id):
  results = auth.sp.user_playlist_tracks(username, playlist_id)
  tracks = results['items']
  while results['next']:
    results = auth.sp.next(results)
    tracks.extend(results['items'])
  return tracks


def get_uris(items):
  uris = []
  for item in items:
    track = item['track']
    uris.append(track['uri'])
  pprint(uris)
  return uris


def parse_uri(playlist_uri):
  username = playlist_uri.split(':')[2]
  playlist_id = playlist_uri.split(':')[4]
  return username, playlist_id

# list comparisons to find the newly added tracks
def diff_playlists(current_uri_list, archive_uri_list):
  if archive_uri_list is None:
    return current_uri_list
  else:
    new_tracks = [x for x in current_uri_list if x not in archive_uri_list]
    return new_tracks

# db methods
def db_get_watchlist():
  file = open(watchlist_path, 'r')
  l = file.read().split('\n')
  file.close()
  return l


def db_get_history_playlists(playlist_uri):
  f = db_history_path + playlist_uri
  if os.path.exists(f):
    f = open(f, 'r')
    l = f.read().split('\n')
    l = list(filter(None, l))
    f.close()
    return l
  else:
    "No history found... Starting new history for: " + playlist_uri
    f = open(f, 'w')


def db_append_playlist(uri, latest_report_uri):
  f = db_history_path + uri

  if os.path.exists(f):
    append_write = 'a+'  # append if already exists
  else:
    append_write = 'w'  # make a new file if not

  f = open(f, append_write)
  f.write(latest_report_uri+'\n')
  f.close()
