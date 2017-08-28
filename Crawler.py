import os
from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse

def init():
    for i in range(1,6):
        file = 'Level'+str(i)
        f = open(file,'w')
        f.write("")
        f.close()

class Linkfinder(HTMLParser):

    def __init__(self,url,level,visited,domain):
        super().__init__()
        self.url = url
        self.visited = visited
        self.level = level
        self.domain = domain

    def handle_starttag(self, tag, attrs):
        file = 'Level'+ str(self.level)
        f = open(file,'a')
        if tag=='a':
            for name,value in attrs:
                if name=='href':
                    newurl = parse.urljoin(self.url,value)

                    if not newurl.startswith('http'):
                        continue

                    if newurl.endswith('pdf') or newurl.endswith('png') or newurl.endswith('jpg'):
                        continue

                    newurl = newurl.split('#')[0]

                    if newurl.find(self.domain)==-1:
                        continue

                    if newurl not in self.visited:
                        self.visited.add(newurl)
                        f.write(newurl+'\n')
        f.close()

    def get_links(self):
        return self.visited

init()

base = "https://pec.ac.in"      #Change this for different websites
domain = 'pec.ac.in'

f = open("Level0",'w')
f.write(base)
f.close()
myset=set()
crawled = set()
level = 1
total_levels = 5                #Change levels accordingly
while level < total_levels+1:
    file = 'Level'+str(level-1)
    queue = []
    f = open(file,'r')
    for line in f:
        line.replace('\n','')
        queue.append(line)
        #print(line)

    f.close()

    for url in queue:
        if url.endswith('\n'):
            url.replace('\n','')

        if url in crawled:
            continue
        try:
            print("Crawling ",url)
            crawled.add(url)
            response=urlopen(url)
            bytes=response.read()
            string=bytes.decode('utf-8')
            finder=Linkfinder(url,level,myset,domain)
            finder.feed(string)
            myset = finder.get_links()
        except:
            print(url," cant be crawled")
            continue

    level += 1
