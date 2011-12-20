class LibraryModel:
  def get_music_collection(self, path):
    return 0
  # given a path
  # find every file in it that is a (wma, mp3, wav) recursively
  # get the artist
  # get the album
  # get the path
  # add to a map of the form Map[<artist name>, Map[<album name>, <song path>]]
  # return this map

library_model = LibraryModel()
library_data = library_model.get_music_collection('/home/javon/programming/projects/beethoven/music-dir')
print library_data
