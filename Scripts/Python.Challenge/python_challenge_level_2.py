#!/usr/bin/env python

import urllib2

url_addr = 'http://www.pythonchallenge.com/pc/def/ocr.html'
response = urllib2.urlopen(url_addr)
response.geturl()
response.readline()
response.close()
