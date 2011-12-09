# 2011.12.08 21:18:29 EST
import urllib2
import simplejson

class AlbumArtFetcher:

    def search_albumart(self, artist, album):
        search_term = artist + ' ' + album
        search_term = search_term.lower()
        search_term = search_term.replace(' ', '+')
        url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q={0}'.format(search_term)
        request = urllib2.Request(url, None, {'Referer': 'Beethoven Album Art Fetcher'})
        response = urllib2.urlopen(request)
        results = simplejson.load(response)
        return results



    def result_is_ok(self, result):
        return result.get('responseStatus') == 200



    def get_image_metadata(self, result):
        search_results = result.get('responseData').get('results')
        metadata = []
        for jsondict in search_results:
            url = jsondict['url']
            image_data = self.get_file_from_url(url)
            dims = (jsondict['height'], jsondict['width'])
            if image_data != None:
                metadata.append((image_data, dims))

        return metadata



    def get_file_from_url(self, url):
        req = urllib2.Request(url, headers={'User Agent': 'Beethoven Album Art Fetcher'})
        image_data = None
        try:
            con = urllib2.urlopen(req)
            image_data = con.read()
        except urllib2.HTTPError as e:
            print 'Could not pull image for url: ' + url
        return image_data



    def get_art_and_dims(self, artist, album):
        json_results = self.search_albumart(artist, album)
        if self.result_is_ok(json_results):
            return self.get_image_metadata(json_results)



artist = 'Glassjaw'
album = 'coloring book'
fetcher = AlbumArtFetcher()
data = fetcher.get_art_and_dims(artist, album)
print len(data)
