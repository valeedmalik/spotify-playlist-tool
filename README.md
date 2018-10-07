# Notes

* The tool database keeps the uri of all playlists generated.
* If you delete a playlist on the clientside, that does not effect execution of the tool. The playlist
will still persist on spotify's servers and the tracks will be pulled from it as if you never deleted them.


#### spotify-playlist-tool/.env

```bash
SPOTIPY_CLIENT_ID     ='xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
SPOTIPY_CLIENT_SECRET ='xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
SPOTIPY_REDIRECT_URI  ='https://www.google.com/'

USERNAME              = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'

```



TODO:
1. Aggregate Reports - Single playlist report option
    * single playlists can hold up to 10,000 FYI
    * at scale, will need to paginate aggregate reports 
2. Eliminate dependence on a local db, 
Name/tag playlists where they can be searchable and retrievable