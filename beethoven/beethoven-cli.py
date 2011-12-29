from fetcher import *
from library import *
import sys
import eyeD3


# should not assume it's a jpg here
def write_image_data_to_file(file_data):
  f = open('/tmp/albumart.jpg', 'w')
  f.write(file_data)
  f.close()
  return '/tmp/albumart.jpg'

try:
  root_dir = sys.argv[1]
except:
  print 'Usage: beethoven-cli.py <root music directory>'
  sys.exit()

library = LibraryModel()
library_data = library.get_music_collection(root_dir)

fetcher = AlbumArtFetcher()
for artist_album in library_data.keys():
  artist = artist_album[0]
  album = artist_album[1]
  print 'fetching album art for artist:', artist, 'album:', album
  data = fetcher.get_art_and_dims(artist, album)
  for filepath in library_data[artist_album]:
    tag = eyeD3.Tag()
    tag.link(filepath)
    tag.removeImages()
    file_path = write_image_data_to_file(data[0][0])
    tag.addImage(eyeD3.ImageFrame.FRONT_COVER, file_path)
    try:
      tag.update()
    except:
      print 'Could not update album art tag for', filepath 
print 'Done.'
