import os

from django.conf.urls import patterns

from WebBot import PageUtils
from Pages.Home.Servlet import Home

urlpatterns = patterns('',)
urlpatterns += PageUtils.autoDiscoverPages(os.path.dirname(__file__) + '/Pages')
