# -*- coding: utf-8 -*-

###########################################################################################
#
# Author: astips - (animator.well)
#
# Date: 2017.03
#
# Url: https://github.com/astips
#
# Description: studio url template
#              - modify this file to meet your studio's requirements
#
###########################################################################################
import os

from url import URL as _URL


class StudioUrl(_URL):
    """
    This class inherit from url.URL to support urls which defined by ourselves.
    Also you should give a url string to init a BURL object.
    Then it will translate the url string to some objects or some paths.
    You can get them, if they are valid.
    """

    def __init__(self, url):
        super(StudioUrl, self).__init__(url)
        self._extend_parse = None

    @property
    def extend_parse(self):
        """
        do parse url to get more informations what you need.
        """
        if not self._extend_parse:
            self._extend_parse = self.query
        return self._extend_parse

    @property
    def entity(self):
        """
        """
        return self.extend_parse.get("entity", None)

    @property
    def asset(self):
        """
        """
        return self.extend_parse.get("asset", None)

    @property
    def version(self):
        """
        """
        return self.extend_parse.get("version", None)

    @property
    def project(self):
        return self.extend_parse.get("project", None)

    @property
    def real_path(self):
        """
        """
        real_path = []
        if self.project:
            real_path += ['${project}'.format(project=self.project[0])]

        real_path += [self.path]
        abs_path = os.path.expandvars(''.join(real_path))
        return abs_path

    @property
    def real_paths(self):
        """
        """
        return self.result["real_paths"]

    @property
    def is_valid(self):
        """
        rtype : bool
        """
        return True
