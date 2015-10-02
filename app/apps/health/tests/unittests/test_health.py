# -*- coding: utf-8 -*-
"""Unit tests for the health view."""

# We need some environment variable setting
import os

# We'll extend the basic TestCase.
from django.test import TestCase
# from unittest import TestCase

# We'll need to look up some URLs.
from django.core.urlresolvers import reverse

# We'll test the headers with this tool:
from apps.tests.headers import HeaderTests


class TestHealth(TestCase):

    """Tests the health page."""

    @classmethod
    def get_env_vars(cls, keys):
        """Get a dictionary of env vars."""
        result = {}
        for key in keys:
            result[key] = os.environ.get(key)
        return result

    @classmethod
    def set_env_vars(cls, dictionary):
        """Set environment vars from a dictionary."""
        for key, value in dictionary.items():
            if value is None:
                del os.environ[key]
            else:
                os.environ[key] = value

    def test_headers(self):
        """Make sure the right headers are present."""
        # Instantiate the header tests tool.
        header_tests = HeaderTests()

        # Load the xyzzy page.
        url = reverse('health')
        response = self.client.get(url)

        # Test the content type header.
        header_tests.check_content_type_header(response)

        # Test the security headers.
        header_tests.check_security_headers(response)

    def test_response_code(self):
        """Make sure the response code is 200."""
        # Load the xyzzy page.
        url = reverse('health')
        response = self.client.get(url)

        # Does it 200?
        self.assertEqual(response.status_code, 200)

    def test_response_copy(self):
        """Make sure the copy is correct."""
        # Load the xyzzy page.
        url = reverse('health')
        response = self.client.get(url)

        # Is the copy correct?
        expected = 'Its healthy!'
        self.assertContains(response, expected)

    def test_obfuscate_quarter_length(self):
        """Test env vars are obfuscated."""
        # store original env vars.
        original_env_vars = self.get_env_vars(['TEST_PASSWORD'])

        # Set a fake env variable.
        os.environ['TEST_PASSWORD'] = "TEST"

        # Load the xyzzy page, but with DEBUG mode on.
        with self.settings(DEBUG=True):
            url = reverse('health')
            response = self.client.get(url)

        # The expected result should be "T•••"
        self.assertContains(response, "TEST_PASSWORD : T•••")

        # Restore original env vars
        self.set_env_vars(original_env_vars)

    def test_obfuscate_zero_length(self):
        """Test env vars are not obfuscated if the length is zero."""
        # store original env vars.
        original_env_vars = self.get_env_vars(['TEST_PASSWORD'])

        # Set a fake env variable.
        os.environ['TEST_PASSWORD'] = ""

        # Load the xyzzy page, but with DEBUG mode on.
        with self.settings(DEBUG=True):
            url = reverse('health')
            response = self.client.get(url)

        # The expected result should be "T•••".
        self.assertContains(response, "TEST_PASSWORD : ")

        # Restore original env variables.
        self.set_env_vars(original_env_vars)

    def test_production_has_no_env_vars(self):
        """Test that production environments contain no sensitive env vars."""
        # Store the original environment variables.
        original_env_vars = self.get_env_vars(['ENV_NAME'])

        # Set a fake env variable
        os.environ['ENV_NAME'] = "prod"
        os.environ['ENV_PASSWORD'] = "password"

        # Load the xyzzy page.
        url = reverse('health')
        response = self.client.get(url)

        # The expected result should not contain passwords, secrets or keys.
        self.assertNotContains(response, "ENV_SECRET_KEY")

        # Restore original env variables.
        self.set_env_vars(original_env_vars)
