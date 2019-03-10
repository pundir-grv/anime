#!/usr/bin/env python

__author__ = "Gaurav Pundir"


import bs4
import logging
import pycurl
from bs4 import BeautifulSoup
from io import BytesIO


def getHtmlData(curlObj):
    """Return the html data from given url"""
    buffer = BytesIO()
    curlObj.setopt(pycurl.WRITEDATA, buffer)
    curlObj.perform()
    curlObj.close()
    return buffer.getvalue().decode("utf-8")

def getHrefTag(item,hrefTag=[]):
    if type(item) != bs4.element.Tag:
        return None
    if len(list(item.children)) == 0:
        return None
    if item.has_attr("href"):
        hrefTag.append(item.get_attribute_list("href")[0])
    items = list(item.children)
    for tag in items:
        getHrefTag(tag, hrefTag=hrefTag)
    


def getUrlList(curlObj):
    try:
        htmlData = getHtmlData(curlObj)
    except Exception as e:
        logging.critical("Unable to get list of episodes, error {}".format(e))
        return None
    item = list(BeautifulSoup(htmlData,"html.parser").children)[0]
    hrefTag = []
    getHrefTag(item, hrefTag)
    hrefTag.pop(hrefTag.index("../"))
    return list(set(hrefTag))