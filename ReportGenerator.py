import os
from datetime import *
from pprint import pprint
import re
import auth

db_history_path = "db/histories/"
week_num = str(datetime.today().isocalendar()[1])
year_num = str(datetime.now().year)[2:]
day_num = str(datetime.now().day)
date_tag = " [W" + week_num + "D" + day_num + "Y" + year_num + "]"


class ReportGenerator:

  def __init__(self, username, watchlist_path):
    self.username = username
    self.watchlist_path = watchlist_path

  def generate_aggregate_report(self):
    self.create_playlist(auth.agg_report, "AGGREGATE REPORT" + date_tag)

  def generate_playlist_report(self, playlist_uri):
    new_playlist_report_uri = self.create_update_playlist(playlist_uri)
    if new_playlist_report_uri is not None:
      self.db_append_playlist(playlist_uri, new_playlist_report_uri)

  def create_update_playlist(self, playlist_uri):
    new_tracks = self.diff_playlists(self.playlist_tracks(playlist_uri),
                                     self.playlist_tracks_history(playlist_uri))
    if not new_tracks:
      return None
    else:
      auth.agg_report += new_tracks
      return self.create_playlist(new_tracks, self.playlist_name(playlist_uri) + date_tag)

  def create_playlist(self, track_uri_list, playlist_name):
    if len(track_uri_list) > 0:

      p = auth.sp.user_playlist_create(self.username, playlist_name, public=False)
      playlist_uri = p.get('uri')

      # Spotify limits you to adding 100 tracks at a time
      buffer = track_uri_list[:100]
      remainder_list = track_uri_list[100:]
      while len(buffer) > 0:
        auth.sp.user_playlist_add_tracks(self.username, playlist_uri, buffer)
        buffer = remainder_list[:100]
        remainder_list = remainder_list[100:]

      return playlist_uri
    else:
      return None

  def playlist_name(self, playlist_uri):
    user, id = self.parse_uri(playlist_uri)
    name = auth.sp.user_playlist(user, id, fields='name').get('name')
    return str(name)

  # Return a list of songs
  def playlist_tracks_history(self, playlist_uri):
    l = self.db_get_history_playlists(playlist_uri)
    if l is None:
      return None

    track_history = self.playlist_group_tracks(l)
    return track_history

  def playlist_group_tracks(self, playlist_uris):
    tracks = []
    for playlist_uri in playlist_uris:
      tracks += self.playlist_tracks(playlist_uri)
    return tracks


  def playlist_tracks(self, playlist_uri):
    username, playlist_id = self.parse_uri(playlist_uri)

    items = self.scan_paginated_playlist(playlist_id)
    return self.get_uris(items)


  def scan_paginated_playlist(self, playlist_id):
    results = auth.sp.user_playlist_tracks(self.username, playlist_id)
    tracks = results['items']
    while results['next']:
      results = auth.sp.next(results)
      tracks.extend(results['items'])
    return tracks

  @staticmethod
  def get_uris(items):
    uris = []
    for item in items:
      track = item['track']
      uris.append(track['uri'])
    return uris

  @staticmethod
  def parse_uri(playlist_uri):
    username = playlist_uri.split(':')[2]
    playlist_id = playlist_uri.split(':')[4]
    return username, playlist_id

  # list comparisons to find the newly added tracks
  @staticmethod
  def diff_playlists(current_uri_list, archive_uri_list):
    if archive_uri_list is None:
      return current_uri_list
    else:
      new_tracks = [x for x in current_uri_list if x not in archive_uri_list]
      return new_tracks

  # db methods
  @staticmethod
  def remove_comment(line, sep):
    for s in sep:
      i = line.find(s)
      if i >= 0:
        line = line[:i]
    return line.strip()

  @staticmethod
  def parse_watchlist(str_list):
    tmp = []
    for line in str_list:
      s = ReportGenerator.remove_comment(line, "#")
      if s is not "":
        tmp.append(s)
    return tmp

  @staticmethod
  def db_get_watchlist(watchlist_path):
    file = open(watchlist_path, 'r')
    l = file.read().split('\n')
    file.close()
    l = ReportGenerator.parse_watchlist(l)
    return l

  @staticmethod
  def db_get_history_playlists(playlist_uri):
    os.makedirs(db_history_path, exist_ok=True)
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

  @staticmethod
  def db_append_playlist(uri, latest_report_uri):
    f = db_history_path + uri

    if os.path.exists(f):
      append_write = 'a+'  # append if already exists
    else:
      append_write = 'w'  # make a new file if not

    f = open(f, append_write)
    f.write(latest_report_uri+'\n')
    f.close()
