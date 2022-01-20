#!/usr/bin/python3

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import sqlite3
import time
import random
import logging
import copy

import threading
import concurrent.futures

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
        if len(imageLink) > 0:
            imageLink = baseLinkImage + str(re.findall(r'src="(.*?)"', str(imageLink))[0])
        else:
            imageLink = None

        actor = webSoup.find_all("ol", {"class": "people"})
        actor = re.findall(r'<p>.*<a.*>(.*?)</a>.*</p>', str(actor))

        if len(overview) > 10:
            logger.info("Found info for " + str(cl[0]))
            infoDict = {}
            infoDict["cl"] = cl
            infoDict["overview"] = overview
            infoDict["imageLink"] = imageLink
            infoDict["actor"] = actor
            collectedData.append(infoDict)
            counter = 10
        else:
            logger.info("Not found. Repeating id:" + str(cl[0]) + ' - c:' + str(counter))
            counter += 1
            time.sleep(random.random()*2)
            if counter == 10:
                logger.warning("CANT FIND DATA FOR: " + str(linkToInfo))


def InsertIntoDatabase():
    while collectedData:
        cData = collectedData.pop(0)
        logger.debug(str(cData))
        for tc in cData["actor"]:
            if len(tc) > 1:
                tcId = dbSql.execute("SELECT id FROM actor WHERE name=?", (tc,)).fetchall()
                if len(tcId) == 0:
                    dbSql.execute("INSERT INTO actor(name) VALUES(?)", (tc,))
                tcId = dbSql.execute("SELECT id FROM actor WHERE name=?", (tc,)).fetchall()
                dbSql.execute("INSERT INTO movieActor(id_movie, id_actor) VALUES(?,?)", (int(cData["cl"][0]), int(tcId[0][0]),))

        dbSql.execute("UPDATE movie SET overview=?, image=? WHERE id=?", (cData["overview"], cData["imageLink"], int(cData["cl"][0]),))
        cMovie = dbSql.execute("SELECT title, overview FROM movie WHERE id=?", (int(cData["cl"][0]),)).fetchall()
        logger.info("Inserted additional data for movie: " + str(cMovie[0][0]))

def alreadyInDatabase(cl):
    cl = cl.split(',')
    overview = dbSql.execute("SELECT overview FROM movie WHERE id=?", (cl[0],)).fetchall()
    logger.debug(str(overview))
    if overview[0][0] is not None and len(overview[0][0]) > 25:
        return True
    return False

maxThreads = 10
chunkCounter = 0
moviesLeft = 0

with open(linkFile, newline='') as cLink:
    moviedbId = re.sub(r'[^\x00-\x7f]',r' ', cLink.read())
    moviedbId = moviedbId.splitlines()
    moviedbId.pop(0)
    moviesLeft = len(moviedbId)

    chunks = [moviedbId[x:x+maxThreads] for x in range(0, len(moviedbId), maxThreads)]

    for chunk in chunks:
        #logger.debug("chunk data:"+str(chunk))
        i = 0
        while i < len(chunk):
            if alreadyInDatabase(chunk[i]):
                del chunk[i]
                moviesLeft -= 1
            else:
                i += 1
        if len(chunk) > 0:
            logger.debug("Still no data:"+str(chunk))
            if len(chunk) > 1:
                with concurrent.futures.ThreadPoolExecutor(max_workers=maxThreads) as executor:
                    executor.map(CollectDataFor, chunk)
            else:
                print(chunk[0])
                CollectDataFor(chunk[0])
            InsertIntoDatabase()
            chunkCounter += len(chunk)
            print("Movies left:", moviesLeft - chunkCounter)

# commiting and closing conection
databaseConnection.commit()
databaseConnection.close()
