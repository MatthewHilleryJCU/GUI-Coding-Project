import sys


# def load_page(url: str) -> str:
def load_page(url):
    """ Returns the content of the web page for a valid url.
        Otherwise it returns the empty string.
    """

    if sys.version_info.major == 3:
        from urllib.request import urlopen
        from urllib.error import URLError

        try:
            response = urlopen(url)

            if response.status == 200:
                body_text = str(response.read())
                return body_text
            return ""
        except URLError:
            return ""
    else:
        from urllib2 import urlopen
        from urllib2 import URLError

        try:
            response = urlopen(url)
            return response.read()
        except URLError:
            return ""
