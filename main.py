from fetcher import *

artist = "Dance Gavin Dance"
album = "Downtown Battle Mountain"

fetcher = AlbumArtFetcher()
data = fetcher.get_art_and_dims(artist, album)

print len(data)
