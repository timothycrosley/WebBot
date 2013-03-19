"""
    Name:
        PageUtils.py
    Description:
        Provides utilities for app engine page url discovery
"""

from django.conf.urls import patterns
import os
from glob import glob

basePackage = ".".join(__package__.split('.')[:-1] + ["Pages"])

def autoDiscoverPages(directory):
    """
        Auto discovers pages within a directory and links to the url that matches their directory name
    """
    pages = patterns('')
    firstPage = None
    for page in glob(os.path.abspath(directory) + "/*"):
        if os.path.isdir(page):
            pageName = os.path.basename(page)
            pageModule = __import__("%s.%s.Servlet" % (basePackage, pageName), globals(), locals(), [pageName], -1)
            servlet = getattr(pageModule, pageName)
            pages += patterns('', (r'^%s/$' % pageName, servlet.djangoView()), )
            if not firstPage:
                firstPage = servlet.djangoView()

    pages += patterns('', (r'^$', firstPage))

    return pages
