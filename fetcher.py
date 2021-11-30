from helpers import AMS_Helper

def get_artwork(album, artist, track):
    url = None
    albums = itunespy.search_album(album) 

    ams_helper = AMS_Helper()
    w, h = ams_helper.get_resolution()

    for result in albums:
        if artist in result.artistName:
            for t in result.get_tracks():
                if track in t.trackName:
                    return t.get_artwork_url(w)
                else:
                    return result.get_artwork_url(w)
    return url


# print("Getting artwork from online!")
# url = get_artwork(args[1], args[0], args[2])
# print(url)
# urllib.request.urlretrieve(url, filepath)