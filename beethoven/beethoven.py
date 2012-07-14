#!/usr/bin/env python

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
  print 'Usage: beethoven.py <root music directory>'
  sys.exit()

# Use root directory to recursively find all mp3 files
library = LibraryModel()
library_data = library.get_music_collection(root_dir)

fetcher = AlbumArtFetcher()
selected_index = 0
for artist, album in library_data.keys():
  print 'Fetching album art for artist:', artist, 'album:', album
  art_verification_url = None
  # Get the image data and dimensions for each album artist combo
  data = fetcher.get_art_and_dims(artist, album)
  # Because library data is of the form (album, artist) =>[array of filenames],
  # we can iterate through each file and set the album art tag
  if (len(data) > 1):
      for filepath in library_data[(artist, album)]:
        tag = eyeD3.Tag()
        tag.link(filepath)
        tag.removeImages()
        album_art_file = write_image_data_to_file(data[selected_index][0])
        tag.addImage(eyeD3.ImageFrame.FRONT_COVER, album_art_file.name)
        os.unlink(album_art_file.name)
        try:
          tag.update()
          art_verification_url = data[selected_index][2]
        except:
          print 'Could not update album art tag for', filepath 
  print 'Setting  album art for artist:', artist, 'album:', album, 'as', art_verification_url
print 'Done.'
