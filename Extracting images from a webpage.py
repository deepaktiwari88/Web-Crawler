
""" Before running please create a .txt file containing the required links in the same directory
    as this file """

from urllib import request
from html.parser import HTMLParser
from urllib import parse

links = []
f = open('links.txt', 'r')  #Replace a.txt with appropriate file name
for line in f:
    a = line.replace('\n', '')
    links.append(a)

f.close()

class check(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.flag=0

    def handle_data(self, data):
        if data.find('Drawings and Prints')!=-1:        #Downloading images with this department
            self.flag = 1

    def get_flag(self):
        return self.flag

class Download_images(HTMLParser):
    def __init__(self, url, count):
        super().__init__()
        self.count = count
        self.url = url

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for name, value in attrs:
                if name == 'srcset':
                    a = parse.urljoin(self.url, value).split(" ")[6]
                    address = parse.urljoin(self.url, a)
                    #print(address)
                    name = str(self.count) + '.jpg'
                    request.urlretrieve(address, name)
                    self.count += 1

    def get_count(self):
        return self.count

count = 1

for url in links:
    flag=0
    if url == '':
        break
    try:
        #print(url)
        response = request.urlopen(url)
        bytes = response.read()
        string = bytes.decode('utf-8')
        checker = check(url)
        checker.feed(string)
        flag = checker.get_flag()
        #print(flag)
        if flag==1:
            downloader = Download_images(url, count)
            downloader.feed(string)
            count = downloader.get_count()
    except:
        print("No image available")
