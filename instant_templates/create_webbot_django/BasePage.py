from DynamicForm.AppEngine import DynamicForm, PageControls
from WebElements import UITemplate

class Page(DynamicForm):
    """
        Defines the base behavior of all pages within the WebBot app.
    """
    def title(self, request):
        """
            Returns the title of the app plus the title of current page.
        """
        return "%(label)s - %(description)s - " + DynamicForm.title(self, request)

    class MainControl(PageControls.TemplateControl):
        """
            Defines how the frame of the page will appear, you can subclass this on a per page basis to change
            the frame.
        """
        template = UITemplate.fromFile("WebBot/Page.wui")

        def initUI(self, ui, request):
            """
                On initializing the main control frame per-request a content control is added which must be
                defined on a per-page basis to define the content of the page.
            """
            ui.pageContents.replaceWith(self.contentControl)

