"""
    Defines an AppEngine compatible version of DynamicForm
"""

import webapp2
from . import HTTP, PageControls
from .DynamicForm import DynamicForm as BaseDynamicForm

class DynamicForm(webapp2.RequestHandler, BaseDynamicForm):
    """
        Overrides handler methods of the DynamicForm class to enable it to run seamlessly on AppEngine
    """
    def __init__(self, request=None, response=None):
        webapp2.RequestHandler.__init__(self, request, response)
        BaseDynamicForm.__init__(self)

    def get(self):
        response = self.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "GET"))
        return response.toAppEngineResponse(self.response)

    def post(self):
        response = self.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "POST"))
        return response.toAppEngineResponse(self.response)

    def put(self):
        response = self.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "PUT"))
        return response.toAppEngineResponse(self.response)

    def head(self):
        response = self.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "HEAD"))
        return response.toAppEngineResponse(self.response)

    def options(self):
        response = self.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "OPTIONS"))
        return response.toAppEngineResponse(self.response)

    def delete(self):
        response = self.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "DELETE"))
        return response.toAppEngineResponse(self.response)

    def trace(self):
        response = self.handleRequest(HTTP.Request.fromAppEngineRequest(self.request, "TRACE"))
        return response.toAppEngineResponse(self.response)
