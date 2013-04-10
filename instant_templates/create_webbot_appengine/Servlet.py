'''
    The Home Page for %(label)s
'''

import os

import logging as log
from WebElements import UITemplate

try:
    from WebBot import Page, PageControls
except ImportError:
    from ...WebBot import Page, PageControls

APP_DIR = os.path.dirname(__file__) + "/"

class Home(Page):
    class ContentControl(PageControls.TemplateControl):
        template = UITemplate.fromFile(APP_DIR + "Template.wui")

        def initUI(self, ui, request):
            """
                The initial setup of the interface (such as dynamically adding widgets that are not present in the
                view) should be done here.
            """
            pass

        def setUIData(self, ui, request):
            """
                Any data populating that occurs as a result of the data in the request should be done here.
            """
            pass

        def processPost(self, ui, request):
            """
                Any unique processing that needs to be done on a post should be done here.
                Note: There is corresponding process(Get|Delete|Put) methods.
            """
            pass

        def validPost(self, ui, request):
            """
                Any validation of post data should occur here: with true being returned only if the data
                is valid.
                Note: There is corresponding valid(Get|Delete|Put) methods.
            """
            return True

