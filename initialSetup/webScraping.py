#!/usr/bin/python3.6

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import sqlite3
import time
import random

import threading
import concurrent.futures

#import thread

database = "database/test.db"
linkFile = "data/links.csv"

databaseConnection = sqlite3.connect(database)
dbSql = databaseConnection.cursor();

baseLinkImage = 'https://www.themoviedb.org'

# multithread implementation to drasticly improve speed
# each position contains a dictionary with:
# {cl: [], overview: overview, imageLink: imageLink, actor: []}
collectedData = []
notCollected = []

def CollectDataFor(cl):
    cl = cl.split(',')
    linkToInfo = baseLinkImage + '/movie/' + str(cl[2])

    counter = 0
    while counter < 10:
        req = Request(linkToInfo, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()

        webSoup = BeautifulSoup(webpage, "html.parser")

        overview = webSoup.find_all("div", {"class": "overview"})
        overview = re.findall(r'<p>(.*?)</p>', str(overview))[0]

        imageLink = webSoup.find_all("img", {"class": "poster"})
        imageLink = baseLinkImage + str(re.findall(r'src="(.*?)"', str(imageLink))[0])

        actor = webSoup.find_all("ol", {"class": "people"})
        actor = re.findall(r'<p>.*<a.*>(.*?)</a>.*</p>', str(actor))

        if len(overview) > 10:
            infoDict = {}
            infoDict["cl"] = cl
            infoDict["overview"] = overview
            infoDict["imageLink"] = imageLink
            infoDict["actor"] = actor
            collectedData.append(infoDict)
        else:
            #print("Not found. Repeating" + str(counter))
            counter += 1
            time.sleep(random.random()*20)
            if counter == 10:
                print("CANT FIND DATA FOR: " + linkToInfo)


def InsertIntoDatabase():
    while collectedData:
        cData = collectedData.pop(0)
        print(cData)
        for tc in cData["actor"]:
            if len(tc) > 1:
                tcId = dbSql.execute("SELECT id FROM actor WHERE name=?", (tc,)).fetchall()
                if len(tcId) == 0:
                    dbSql.execute("INSERT INTO actor(name) VALUES(?)", (tc,))
                tcId = dbSql.execute("SELECT id FROM actor WHERE name=?", (tc,)).fetchall()
                dbSql.execute("INSERT INTO movieActor(id_movie, id_actor) VALUES(?,?)", (int(cData["cl"][0]), int(tcId[0][0]),))

        dbSql.execute("UPDATE movie SET overview=?, image=? WHERE id=?", (cData["overview"], cData["imageLink"], int(cData["cl"][0]),))
        cMovie = dbSql.execute("SELECT title, overview FROM movie WHERE id=?", (int(cData["cl"][0]),)).fetchall()
        print("Inserted additional data for movie: ", cMovie[0][0])


maxThreads = 8
chunkCounter = 0

with open(linkFile, newline='') as cLink:
    moviedbId = re.sub(r'[^\x00-\x7f]',r' ', cLink.read())
    moviedbId = moviedbId.splitlines()
    moviedbId.pop(0)

    chunks = [moviedbId[x:x+maxThreads] for x in range(0, len(moviedbId), maxThreads)]

    for chunk in chunks:
        with concurrent.futures.ThreadPoolExecutor(max_workers=maxThreads) as executor:
            executor.map(CollectDataFor, chunk)
        InsertIntoDatabase()
        chunkCounter += len(chunk)
        print("Processed: ", chunkCounter, " From: ", len(moviedbId))

# commiting and closing conection
databaseConnection.commit()
databaseConnection.close()
