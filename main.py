# Gets uri for each song in a playlist
# user. Uses Client Credentials flow


import json
# from auth import get_session
import auth
from ReportGenerator import ReportGenerator

with open('./config.json') as config_file:
  config_data = json.load(config_file)

  watchlist_path = config_data['watchlist_path']

  username = auth.init()

  report_generator = ReportGenerator(username, watchlist_path)

  watchlist = report_generator.db_get_watchlist(config_data['watchlist_path'])

  # test_playlist_uri = 'spotify:user:valeedm92:playlist:5iMnObRSZlbUY2sgyut9Jf'
  # print(watchlist)
  # x = playlist_name(test_playlist_uri)
  # print(x)

  for playlist in watchlist:
    report_generator.generate_playlist_report(playlist)

    print(playlist)

  report_generator.generate_aggregate_report()
