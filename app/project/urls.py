# -*- coding: utf-8 -*-
"""The main URLconf for the project."""

# We'll use Django's tools for parsing URLs/Routes.
from django.conf.urls import include, url

# Define the URLs/Routes for the project.
urlpatterns = [

    # This pulls in the URLs for the ``health`` app.
    # It will prefix all URLs from that app with ``/health``.
    url(r'^health', include('apps.health.urls')),

]
