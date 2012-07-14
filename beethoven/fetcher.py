import urllib2
import simplejson

class AlbumArtFetcher:
  def get_art_and_dims(self, artist, album):
   json_results = self.search_albumart(artist, album)
   album_art_data = []
   if self.result_is_ok(json_results):
     album_art_data = self.get_image_metadata(json_results)
   return album_art_data

  # Google Image API search, return results in json formatted text
  def search_albumart(self, artist, album):
    search_term = artist + ' ' + album
    search_term = search_term.lower() 

    # There's probably a library I can use the escapes other characters as well
    search_term = search_term.replace(' ', '+')
    search_term = search_term.replace('&', '%26')

    url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q={0}'.format(search_term)
    request = urllib2.Request(url, None, {'Referer': 'Beethoven Album Art Fetcher'})
    response = urllib2.urlopen(request)
    results = simplejson.load(response)
    return results

  # Returns true if it gets Status OK
  def result_is_ok(self, result):
    return result['responseStatus'] == 200

  # Gets the data of album art file, along with width and height
  def get_image_metadata(self, result):
    search_results = result['responseData']['results']
    metadata = []
    for jsondict in search_results:
      url = jsondict['url']
      image_data = self.get_file_from_url(url)
      dims = (jsondict['height'], jsondict['width'])
      if image_data is not None:
        metadata.append((image_data, dims, url))
    return metadata

  # Retrieves the image from the actual host, provided they don't block us
  def get_file_from_url(self, url):
    req = urllib2.Request(url, headers = { 'User Agent': 'Beethoven Album Art Fetcher' })
    image_data = None
    try:
      con = urllib2.urlopen(req)
      image_data = con.read()
    except urllib2.HTTPError as e:
      pass
      # print 'Could not pull image for url: ' + url
    return image_data
