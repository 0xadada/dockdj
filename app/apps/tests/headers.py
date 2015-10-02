# -*- coding: utf-8 -*-
"""Utilities for testing Django ``HttpResponse`` headers."""

# We'll extend the basic TestCase.
from django.test import TestCase


class HeaderTests(TestCase):

    """Some common tests to ensure the proper HTTP headers.

    Note that some methods here are named `check_*` rather
    than `test_*`. That prevents the test runner from
    running it. Other classes can call this manually and
    pass in an HTTP response of their choosing.

    """

    def check_content_type_header(self, response):
        """Make sure the right Content-Type headers are present."""
        # What are the headers?
        headers = response._headers

        # Do we have the the right content type and charset?
        actual = headers.get('content-type')
        expected = ('Content-Type', 'text/html; charset=utf-8')
        self.assertEqual(actual, expected)

    def check_security_headers(self, response):
        """Make sure the right security headers are present."""
        # What are the headers?
        headers = response._headers

        # Do we have the x-frame-options?
        actual = headers.get('x-frame-options')
        expected = ('X-Frame-Options', 'DENY')
        self.assertEqual(actual, expected)

        # Do we have the x-xss-protection?
        actual = headers.get('x-xss-protection')
        expected = ('x-xss-protection', '1; mode=block')
        self.assertEqual(actual, expected)

        # Do we have the x-content-type-options?
        actual = headers.get('x-content-type-options')
        expected = ('x-content-type-options', 'nosniff')
        self.assertEqual(actual, expected)
