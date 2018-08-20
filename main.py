# Gets uri for each song in a playlist
# user. Uses Client Credentials flow
from pprint import pprint


# from auth import get_session
import auth
from helpers import create_playlist, diff_playlists, playlist_tracks, \
  db_get_watchlist, parse_uri, generate_report, playlist_name

username = 'valeedm92'
test_playlist_uri = 'spotify:user:valeedm92:playlist:5iMnObRSZlbUY2sgyut9Jf'

auth.init()
watchlist = db_get_watchlist()
# check future bass playlist (100+)
# uris = playlist_tracks(test_playlist_uri)

# playlist_uri = create_playlist(uris)

# l = diff_playlists(
#   playlist_tracks("spotify:user:valeedm92:playlist:3rtDhIERTp3K67CRaxKudj"),
#   playlist_tracks("spotify:user:valeedm92:playlist:6tkpfAH1uFlnjXPqKZ9G3f"))
#
# create_playlist(l, "new test report(W" + week_num + "Y" + year_num + ")")





# pprint(watchlist)
# x = playlist_name(test_playlist_uri)
# print(x)




for playlist in watchlist:
  generate_report(playlist)

