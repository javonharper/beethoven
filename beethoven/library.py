import os.path

  # find every file in it that is a (wma, mp3, wav) recursively
  # get the artist
  # get the album
  # get the path
  # add to a map of the form Map[<artist name>, Map[<album name>, <song path>]]
  # return this map

class LibraryModel:
  def get_music_collection(self, path):
    if self.music_directory_is_valid(path):
      return self.build_music_map(path)
    print path, 'is not a valid directory.'
    return None

  def music_directory_is_valid(self, path):
    return os.path.exists(path) and os.path.isdir(path)
  
  def build_music_map(self, path):
    return None
#    for root, dirs, files in os.walk(path):
#      for filename in files:
#        print filename.endswith('.mp3')

library_model = LibraryModel()
library_data = library_model.get_music_collection('/home/javon/programming/projects/beethoven/music-dir')
print library_data
