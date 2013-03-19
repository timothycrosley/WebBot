"""
    This is an example app engine data store model
    Modify freely to fit your purposes.
"""

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import search
from google.appengine.api import files

class Example(search.SearchableModel):
    owner = db.UserProperty(required=True)
    text = db.StringProperty(required=True)
    last_updated = db.DateTimeProperty(auto_now=True)
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def create(cls, **kwargs):
        """
            Will create an instance of the model, automatically setting the user to the
            currently logged in user.
        """
        cls(owner=users.get_current_user(), **kwargs).save()
