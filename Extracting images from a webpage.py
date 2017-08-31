from urllib import request
from html.parser import HTMLParser
from urllib import parse

links=[]
f = open('a.txt','r')   # Replace a.txt with appropriate file name that contains links of webpages
for line in f:
    a = line.replace('\n','')
    links.append(a)

f.close()

class Download_images(HTMLParser):

    def __init__(self,url,count):
        super().__init__()
        self.count = count
        self.url = url

    def handle_starttag(self, tag, attrs):
        if tag=='img':
            for name,value in attrs:
                if name=='src':
                    address = parse.urljoin(self.url,value).split(" ")[0]
                    #print(address)
                    name = str(self.count)+'.jpg'
                    request.urlretrieve(address,name)
                    self.count +=1

    def get_count(self):
        return self.count

count=1

for url in links:
    if url=='':
        break
    response = request.urlopen(url)
    bytes = response.read()
    string = bytes.decode('utf-8')
    #print(string)
    downloader = Download_images(url,count)
    downloader.feed(string)
    count = downloader.get_count()
