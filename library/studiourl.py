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
from .url import URL as _URL


class StudioUrl(_URL):
    """
    This class inherit from url.URL to support urls which defined by ourselves.
    Also you should give a url string to init a BURL object.
    Then it will translate the url string to some objects or some paths.
    You can get them, if they are valid.
    """

    def extend_parse(self):
        """
        do parse url to get more informations what you need.
        """
        pass

    @property
    def entity(self):
        """
        """
        return self.result["entity"]

    @property
    def asset(self):
        """
        """
        return self.result["asset"]

    @property
    def version(self):
        """
        """
        return self.result["version"]

    @property
    def real_path(self):
        """
        """
        return self.result["real_path"]

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
