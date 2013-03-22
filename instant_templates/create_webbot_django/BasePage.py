import os

from DynamicForm import DynamicForm, PageControls
from WebElements import UITemplate
from WebElements import Base
from django.conf import settings

from django.template import Context, Template, RequestContext

Base.Settings.STATIC_URL = settings.STATIC_URL

class Page(DynamicForm.DynamicForm):
    """
        Defines the base behavior of all pages within the WebBot app.
    """
    def title(self, request):
        """
            Returns the title of the app plus the title of current page.
        """
        return "%(label)s - %(description)s - " + DynamicForm.DynamicForm.title(self, request)

    class MainControl(PageControls.TemplateControl):
        template = UITemplate.fromFile(os.path.dirname(__file__) + "/Page.wui")

        def initUI(self, ui, request):
            ui.pageContents.replaceWith(self.contentControl)

        def initUI(self, ui, request):
            """
                On initializing the main control frame per-request a content control is added which must be
                defined on a per-page basis to define the content of the page.
            """
            ui.pageContents.replaceWith(self.contentControl)
