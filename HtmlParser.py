import urllib
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup, SoupStrainer


from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
           # Check the list of defined attributes.
           for name, value in attrs:
               # If href is defined, print it.
               if name == "href":
                   self.data = value


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(mystr):
    s = MLStripper()
    s.feed(mystr)
    return s.get_data()



##load main url html data
page = urllib2.urlopen('https://www.sec.gov/Archives/edgar/data/842023/0000932471-16-012827-index.htm').read()
soup = BeautifulSoup(page, 'html.parser')

#soup = BeautifulSoup(page, 'html.parser', parse_only=SoupStrainer('a', href=True))
soup.prettify()

##find the table which contains link to file
table = soup.find("table", {"class" : "tableFile"})
##get the row(2nd) which contains link for filing form
rows = table.find_all('tr')[1::2]

##get link from the row
parser = MyHTMLParser()
parser.feed(str(rows))
url = 'https://www.sec.gov' + parser.data


##remove html tags from the file and get the whole file as a string
fp = urllib.request.urlopen(url)
mybytes = fp.read()

mystr = mybytes.decode("utf8")
fp.close()

mystr2 = strip_tags(mystr)
print(mystr2) 



