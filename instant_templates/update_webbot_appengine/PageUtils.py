"""
    Name:
        PageUtils.py
    Description:
        Provides utilities for app engine page url discovery
"""

import webapp2

import os
from glob import glob

def autoDiscoverPages(directory, defaultPage="Home"):
    """
        Auto discovers pages within a directory and links to the url that matches their directory name
    """
    class MainHandler(webapp2.RequestHandler):
        def get(self):
            self.redirect("/" + defaultPage)

    pages = [('/', MainHandler)]
    for page in glob(directory + "/*"):
        if os.path.isdir(page):
            pageName = os.path.basename(page)
            pageModule = __import__("%s.%s.Servlet" % (directory, pageName), globals(), locals(), [pageName], -1)
            servlet = getattr(pageModule, pageName)
            pages.append(("/" + pageName, servlet))

    return pages
