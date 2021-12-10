#!/usr/bin/python3.6

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import sqlite3

database = "database/test.db"
linkFile = "data/links.csv"

databaseConnection = sqlite3.connect(database)
dbSql = databaseConnection.cursor();

baseLinkImage = 'https://www.themoviedb.org'



with open(linkFile, newline='') as cLink:
    moviedbId = re.sub(r'[^\x00-\x7f]',r' ', cLink.read())
    moviedbId = moviedbId.splitlines()
    moviedbId.pop(0)

    for cl in moviedbId:
        cl = cl.split(',')
        linkToInfo = baseLinkImage + '/movie/' + str(cl[2])

        req = Request(linkToInfo, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()

        webSoup = BeautifulSoup(webpage, "html.parser")

        overview = webSoup.find_all("div", {"class": "overview"})
        overview = re.findall(r'<p>(.*?)</p>', str(overview))[0]

        imageLink = webSoup.find_all("img", {"class": "poster"})
        imageLink = baseLinkImage + str(re.findall(r'src="(.*?)"', str(imageLink))[0])

        cast = webSoup.find_all("ol", {"class": "people"})
        cast = re.findall(r'<p>.*<a.*>(.*?)</a>.*</p>', str(cast))

        for tc in cast:
            if len(tc) > 1:
                tcId = dbSql.execute("SELECT id FROM cast WHERE name=?", (tc,)).fetchall()
                if len(tcId) == 0:
                    dbSql.execute("INSERT INTO cast(name) VALUES(?)", (tc,))
                tcId = dbSql.execute("SELECT id FROM cast WHERE name=?", (tc,)).fetchall()
                dbSql.execute("INSERT INTO movieCast(id_movie, id_cast) VALUES(?,?)", (int(cl[0]), int(tcId[0][0]),))

        dbSql.execute("UPDATE movie SET overview=?, image=? WHERE id=?", (overview, imageLink, int(cl[0]),))
        cMovie = dbSql.execute("SELECT title, overview FROM movie WHERE id=?", (int(cl[0]),)).fetchall()
        print("Inserted additional data for movie: ", cMovie[0][0])

        # print(overview)
        # print(imageLink)
        # print(cast)
