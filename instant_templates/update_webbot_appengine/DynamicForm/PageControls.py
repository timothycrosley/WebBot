'''
    PageControls.py

    Defines the most basic PageControls that can be subclassed to control sections of a page

    Copyright (C) 2013  Timothy Edmund Crosley

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import re
import copy

from . import HTTP
from .RequestHandler import RequestHandler
from WebElements import UITemplate
from WebElements.All import Factory
from WebElements import Base
from WebElements.Base import WebElement, TemplateElement
from WebElements.Layout import Center, Horizontal, Flow
from WebElements.Display import Image, Label, FormError
from WebElements.Resources import ScriptContainer
from WebElements.StringUtils import scriptURL
from WebElements import ClientSide


class PageControl(RequestHandler, WebElement):
    """
        Defines the concept of a page control: The merger of a request handler and a WebElement
    """
    properties = WebElement.properties.copy()
    properties['autoLoad'] = {'action':'classAttribute', 'type':'bool'}
    tagName = "section"
    autoLoad = True
    autoReload = False
    silentReload = True
    elementFactory = Factory

    class ClientSide(WebElement.ClientSide):

        def getAll(self, controls, silent=False, timeout=None, fresh=True, **kwargs):
            return ClientSide.call("DynamicForm.get", controls, silent, scriptURL(kwargs), timeout, fresh)

        def get(self, silent=False, timeout=None, fresh=True, **kwargs):
            return ClientSide.call("DynamicForm.get", self, silent, scriptURL(kwargs), timeout, fresh)

        def postAll(self, controls, silent=False, fresh=False, timeout=None, **kwargs):
            return ClientSide.call("DynamicForm.post", controls, silent, scriptURL(kwargs), timeout, fresh)

        def post(self, silent=False, timeout=None, fresh=False, **kwargs):
            return ClientSide.call("DynamicForm.post", self, silent, scriptURL(kwargs), timeout, fresh)

        def putAll(self, controls, silent=False, fresh=False, timeout=None):
            return ClientSide.call("DynamicForm.put", controls, silent, scriptURL(kwargs), timeout, fresh)

        def put(self, silent=False, timeout=None, fresh=False, **kwargs):
            return ClientSide.call("DynamicForm.put", self, silent, scriptURL(kwargs), timeout, fresh)

        def delteAll(self, controls, silent=False, fresh=False, timeout=None, **kwargs):
            return ClientSide.call("DynamicForm.get", controls, silent, scriptURL(kwargs), timeout, fresh)

        def delete(self, silent=False, timeout=None, fresh=False, **kwargs):
            return ClientSide.call("DynamicForm.delete", self, silent, scriptURL(kwargs), timeout, fresh)

    class Loading(Center):
        """
            Defines how the element will look like while an AJAX call is being performed (unless silent loading is used)
            NOTE: you can override this whole class to modify the appearance - just replace with a different WebElement
        """
        def __init__(self, id, name, parent, **kwargs):
            Center.__init__(self, id, name, parent, **kwargs)
            self.addClass("WLoading")

            layout = self.addChildElement(Horizontal())
            layout.addClass("WContent")
            layout.addChildElement(Image(src="images/throbber.gif"))
            label = layout.addChildElement(Label())
            label.setText(self.parent.loadingText)

    def __init__(self, id=None, name=None, parent=None, parentHandler=None, initScripts=None, request=None,
                 **kwargs):
        if parentHandler:
            self.elementFactory = parentHandler.elementFactory

        RequestHandler.__init__(self, parentHandler=parentHandler, initScripts=initScripts)
        WebElement.__init__(self, id=id or self.accessor, name=name, parent=None, **kwargs)
        self.attributes['handler'] = self.accessor
        self.request = request

        self._loading = self.Loading(self.id + ":Loading", self.name + ":Loading", parent=self, hide=True).toHTML()

        self.initScripts.append(self.setScriptContainer(ScriptContainer()).content())

    def __call__(self, id, request, fields=None, method="GET", **kwargs):
        """
            Call this to create a new instance of the page control - passing in a unique id
            and optionally a request or a dictionary of request fields
        """
        request = copy.copy(request)
        request.method = method
        if fields:
            request.fields = HTTP.FieldDict(request.fields.copy())
            request.fields.update(fields)

        return self.__class__(id=id, request=request, parentHandler=self.parentHandler, **kwargs)

    @property
    def loadingText(self):
        """
            Defines the default text to display while this controller is loading
        """
        return "Loading %s..." % (self.__class__.__name__, )

    def toHTML(self, formatted=False, *args, **kwargs):
        """
            Override toHTML to draw loading section in addition to controller placement
        """
        return "".join([self._loading, WebElement.toHTML(self, formatted, *args, **kwargs)])

    def buildElement(self, className, id=None, name=None, parent=None, scriptContainer=None, **kwargs):
        """
            Builds a WebElement using the factory attached to this controller
        """
        element = self.elementFactory.build(className, id, name, parent)
        if scriptContainer != None:
            element.setScriptContainer(scriptContainer)
        if kwargs:
            element.setProperties(kwargs)

        return element

    def buildTemplate(self, template):
        """
            Creates a WebElement from a template based on the pageControl's element factory
        """
        return TemplateElement(template=template, factory=self.elementFactory)

    def content(self, formatted=False, request=None, *args, **kwargs):
        """
            Overrides the WebElement content to include an initial response if autoLoad is set to true
        """
        request = request or HTTP.Request()
        if self.autoLoad == "AJAX":
            request.response.scripts.addScript("DynamicForm.get('%s');" % self.fullId())
        elif self.autoLoad is True:
            return self.renderResponse(request)

        return ""

    def __str__(self):
        """
            Use the RequestHandler str implementation
        """
        return RequestHandler.__str__(self)

    def renderResponse(self, request):
        request = self.request or request

        ui = self.buildUI(request)
        self.initUI(ui, request)
        if self.autoReload:
            ui.clientSide(self.clientSide.get(silent=self.silentReload, timeout=self.autoReload))

        if request.method == "GET" and self.validGet(ui, request):
            self.processGet(ui, request)
        elif request.method == "POST" and self.validPost(ui, request):
            self.processPost(ui, request)
        elif request.method == "DELETE" and self.validDelete(ui, request):
            self.processDelete(ui, request)
        elif request.method == "PUT" and self.validPut(ui, request):
            self.processPut(ui, request)

        self.setUIData(ui, request)
        if not self.canEdit(request):
            ui.setEditable(False)
        if not request.response.scripts:
            request.response.scripts = ScriptContainer()
            ui.setScriptContainer(request.response.scripts)
            return ui.toHTML(request=request) + request.response.scripts.toHTML(request=request)
        else:
            ui.setScriptContainer(request.response.scripts)
            return ui.toHTML(request=request)



class ElementControl(PageControl):
    """
        Defines a PageControl that is rendered using WebElements
    """
    def buildUI(self, request):
        return Flow()

    def initUI(self, ui, request):
        return

    def setUIData(self, ui, request):
        return

    def valid(self, ui, request):
        """
            The default validation method for all non get requests if validate(requestType) is not defined
        """
        return True

    def validPost(self, ui, request):
        """
            Returns true if the post data is valid
        """
        return self.valid(ui, request)

    def validGet(self, ui, request):
        """
            Returns true if the get data is valid - defaults to True should very rarely be overridden
        """
        return True

    def validDelete(self, ui, request):
        """
            Returns true if the delete data is valid
        """
        return self.valid(ui, request)

    def validPut(self, ui, request):
        """
            Returns true if the put data is valid
        """
        return self.valid(ui, request)

    def processPost(self, ui, request):
        """
            Override to define the processing specific to a post
        """
        pass

    def processGet(self, ui, request):
        """
            Override to define the processing specific to a get
        """
        pass

    def processDelete(self, ui, request):
        """
            Override to define the processing specific to a delete
        """
        pass

    def processPut(self, ui, request):
        """
            Override to define the processing specific to a put
        """
        pass


class TemplateControl(ElementControl):
    """
        Defines an ElementControl that is rendered from a WUI Template
        NOTE: When subclassing set the template attribute - aka template = UITemplate.fromFile("myFile.wui")
    """
    template = UITemplate.Template("empty")

    def __init__(self, id=None, name=None, parent=None, parentHandler=None, initScripts=None, **kwargs):
        ElementControl.__init__(self, id, name, parent, parentHandler, initScripts, **kwargs)

        templateDefinition = TemplateElement(template=self.template, factory=self.elementFactory)

        for control in templateDefinition.allChildren():
            if isinstance(control, PageControl):
                self.registerControl(control.__class__)

    def buildUI(self, request):
        return TemplateElement(template=self.template, factory=self.elementFactory)
