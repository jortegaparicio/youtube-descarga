#!/usr/bin/python3

#
# Simple XML parser for YTsax
# Juan Antonio Ortega Aparicio
# Just prints the titles in a videos.xml file

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string
import urllib.request



class CounterHandler(ContentHandler):

    def __init__(self):
        self.inTitle = False
        self.inUrl = False
        self.theTitle = ""
        self.list = ""
        self.theUrl = ""
        self.counter = 0 # Both counters are for skipping the first link
        self.counter2 = 0

    def startElement(self, name, attrs):
        if name == 'title':
            self.inTitle = True
        elif name == 'link':
            self.inUrl = True
            if self.counter != 0:
                self.theUrl = attrs.get('href')
            self.counter = 1

    def endElement(self, name):
        if name == 'link':
            if self.counter2 != 0 :
                print('\t\t<li><a href="' + self.theUrl + '">' + self.theTitle + '</a></li>')
            self.counter2 = 2
        if self.inUrl:
            self.inTitle = False
            self.inUrl = False
            self.theTitle = ""
            self.theUrl = ""

    def characters(self, chars):
        if self.inTitle:
            self.theTitle += chars


# --- Main prog
if __name__ == "__main__":

    # Load parser and driver
    JokeParser = make_parser()
    JokeHandler = CounterHandler()
    JokeParser.setContentHandler(JokeHandler)

    id = 'https://www.youtube.com/feeds/videos.xml?channel_id=' + sys.argv[1]
    html = urllib.request.urlopen(id)

    print("<html>\n<head>\n\t<title>Títulos del canal de Youtube de CursosWeb</title>\n</head>\n<body>\n\t<p>Títulos del canal CursosWeb:"
         "</p>\n\t<ul>" )
    # Ready, set, go!

    JokeParser.parse(html)

    print("\t</ul>\n"+"</body>\n" + "<html>")
