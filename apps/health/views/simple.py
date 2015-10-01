# -*- coding: utf-8 -*-
"""The view for the /health page."""

import os
from math import floor

# We'll extend Django's base generic view.
from django.views.generic.base import View

# We need to render templates.
from django.shortcuts import render

# We're going to do some stuff, only if DEBUG mode is on.
from django.conf import settings


class Simple(View):

    """A very simple generic view that renders a template."""

    @classmethod
    def obfuscate(cls, input_string="", show_chars=4):
        """Obfuscate the end of a string."""
        return_string = ""
        if len(input_string) > show_chars:
            return_string = input_string[0:show_chars] + \
                "•" * len(input_string[show_chars:len(input_string)])
        else:
            return_string = input_string
        return return_string

    def get(self, request):
        """Handle requests for GET /health."""
        # What template should we use?
        template = 'health/default.html'

        # Add environment variables to the list if we're in dev mode.
        env_vars = []
        if settings.DEBUG:
            for key in os.environ.keys():
                filters = ['password', 'secret', 'user']
                # Obfuscate any username or passwords.
                key_value = os.environ[key]
                for item in filters:
                    if item in key.lower():
                        shown_chars = floor(len(key_value) / 4)
                        key_value = self.obfuscate(key_value, shown_chars)
                        break
                env_vars.append(key + " : " + key_value)

        # Add Django settings to the list.
        env_vars.append("settings.STATIC_URL: " + settings.STATIC_URL)
        env_vars.append("settings.DEBUG: " + str(settings.DEBUG))

        # Sort the list.
        env_vars.sort(key=str.lower)

        # What data should we send to the template?
        template_data = {
            'foo': 'bar',
            'message': 'Its healthy!',
            'env_vars': env_vars,
        }

        # Now render the data and the template.
        return render(request, template, template_data)
