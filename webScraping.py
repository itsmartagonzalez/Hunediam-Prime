#!/usr/bin/python3.6

# import urllib.request
#
# allFromPage = urllib.request.urlopen('https://www.themoviedb.org/movie/862-toy-story').read().decode()
#
# print(allFromPage)

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

baseLinkImage = 'https://www.themoviedb.org'

req = Request('https://www.themoviedb.org/movie/862-toy-story', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

webSoup = BeautifulSoup(webpage, "html.parser")

overview = webSoup.find_all("div", {"class": "overview"})
overview = re.findall(r'<p>(.*?)</p>', str(overview))[0]

imageLink = webSoup.find_all("img", {"class": "poster"})
imageLink = baseLinkImage + str(re.findall(r'src="(.*?)"', str(imageLink))[0])

cast = webSoup.find_all("ol", {"class": "people"})
cast = re.findall(r'<p>.*<a.*>(.*?)</a>.*</p>', str(cast))

print(overview)
print(imageLink)
print(cast)
