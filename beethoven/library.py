import os.path
import eyeD3

class LibraryModel:
  def get_music_collection(self, path):
    if self.music_directory_is_valid(path):
      return self.build_music_map(path)
    print path, 'is not a valid directory.'
    return None

  def music_directory_is_valid(self, path):
    return os.path.exists(path) and os.path.isdir(path)
  
  #recursively builds a dictionary given a root directory
  # dictionary is of form (artist, album) -> [list of files that belong to that artist and album]
  def build_music_map(self, path):
    dictionary = {}
    for root, dirs, files in os.walk(path):
      for filename in files:
        if (filename.endswith('.mp3') or filename.endswith('.m4a')):
          full_path = os.path.join(root, filename)
          tag = eyeD3.Tag()
          tag.link(full_path)
          artist = tag.getArtist()
          album = tag.getAlbum()
          # This may be a dirty hack. if the value of (artist, album) does not exist,
          # then create an empty list there so it can be used later
          try:
            dictionary[(artist, album)]
          except:
            dictionary[(artist, album)] = []
          # Add the new file to the list of songs that belong to (album, artist)
          dictionary[(artist, album)].append(full_path)
    return dictionary
