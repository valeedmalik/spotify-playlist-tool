# Gets uri for each song in a playlist
# user. Uses Client Credentials flow


# from auth import get_session
import auth
from helpers import db_get_watchlist, generate_aggregate_report, \
  generate_playlist_report

username = 'valeedm92'
test_playlist_uri = 'spotify:user:valeedm92:playlist:5iMnObRSZlbUY2sgyut9Jf'

auth.init()
watchlist = db_get_watchlist()
# pprint(watchlist)
# x = playlist_name(test_playlist_uri)
# print(x)

for playlist in watchlist:
  generate_playlist_report(playlist)
  print(playlist)

generate_aggregate_report()
