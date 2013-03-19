"""
    Name:
        main.py

    Description:
        Links URLS to specific request handlers
"""

import webapp2

from WebBot.PageUtils import autoDiscoverPages

app = webapp2.WSGIApplication(autoDiscoverPages("Pages"), debug=True)
