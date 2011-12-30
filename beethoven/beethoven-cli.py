from fetcher import *
from library import *
import sys
import tempfile
import eyeD3

def write_image_data_to_file(file_data):
 # Should not assume image is a jpg, workaround because eyed3 can't guess mimetype
 f = tempfile.NamedTemporaryFile(suffix = '.jpg', delete = False)
 f.write(file_data)
 f.close()
 return f

try:
  root_dir = sys.argv[1]
except:
  print 'Usage: beethoven-cli.py <root music directory>'
  sys.exit()

#Use root directory to recursively find all mp3 files
library = LibraryModel()
library_data = library.get_music_collection(root_dir)

fetcher = AlbumArtFetcher()
for artist, album in library_data.keys():
  print 'fetching album art for artist:', artist, 'album:', album
  # Get the image data and dimensions for each album artist combo
  data = fetcher.get_art_and_dims(artist, album)
  # Because library data is of the form (album, artist) =>[array of filenames],
  # we can iterate through each file and set the album art tag
  for filepath in library_data[(artist, album)]:
    tag = eyeD3.Tag()
    tag.link(filepath)
    tag.removeImages()
    # Since cli version will be a little less versitile, always grab the 
    # first result (second [0] is getting the art from the (art, (width, height)) tuple)
    album_art_file = write_image_data_to_file(data[0][0])
    tag.addImage(eyeD3.ImageFrame.FRONT_COVER, album_art_file.name)
    os.unlink(album_art_file.name)
    try:
      tag.update()
    except:
      print 'Could not update album art tag for', filepath 
print 'Done.'
