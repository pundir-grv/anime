#!/usr/bin/env python
# Small script to download anime 

__author__ = "Gaurav Pundir"

import logging
import os
import pycurl
import sys
import urllib.parse
from loadConfig import create_logger, config
from parseBaseUrl import getUrlList

MAXRETRIES = config["maxretries"]

def download(fileName, mode, curlObj):
    """Recursively download the file"""
    global MAXRETRIES
    if MAXRETRIES == 0:
        logging.critical("Maximum retry limit reached for {}".format(fileName))
        curlObj.close()
        return
    try:
        with open(fileName, mode) as fp:
            curlObj.setopt(pycurl.WRITEDATA, fp)
            curlObj.perform()
        curlObj.close()
    except Exception as e:
        logging.critical("ERROR : {}".format(e))
        logging.info("Retrying")
        MAXRETRIES -= 1
        curlObj.setopt(pycurl.RESUME_FROM, os.path.getsize(fileName))
        download(fileName, "ab", curlObj)

def downloadProgress(download_t, download_d, upload_t, upload_d):
    try:
        frac = float(download_d)/float(download_t)
    except:
        frac = 0
    sys.stdout.write("\r%s %3i%%" % ("Download:", frac*100))

def getCurlObj(url):
    """Return the curl obj for given url"""
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.CONNECTTIMEOUT, 30)
    curl.setopt(pycurl.NOPROGRESS, 0)
    curl.setopt(pycurl.PROGRESSFUNCTION, downloadProgress)
    return curl

def main():
    baseDir = os.getcwd()
    for anime in config["anime"]:
        os.chdir(baseDir)
        logging.info("Processing {}".format(anime["animeDir"]))
        if not os.path.isdir(anime["animeDir"]):
            os.mkdir(anime["animeDir"])
        os.chdir(anime["animeDir"])
        baseCurlObj = getCurlObj(anime["animeBaseUrl"])
        urlList = getUrlList(baseCurlObj)
        if not urlList:
            continue
        for episodeUrl in urlList:
            fileName = urllib.parse.unquote(episodeUrl)
            logging.info("Downloading {}".format(fileName))
            completeUrl = anime["animeBaseUrl"] + episodeUrl
            episodeCurlObj = getCurlObj(completeUrl)
            download(fileName, "wb", episodeCurlObj)
    return

if __name__ == "__main__":
    create_logger(debug=True)
    main()