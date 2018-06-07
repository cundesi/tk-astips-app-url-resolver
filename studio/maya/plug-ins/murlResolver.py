# -*- coding: utf-8 -*-

###########################################################################################
#
# Author: astips - (animator.well)
#
# Date: 2017.03
#
# Url: https://github.com/astips
#
# Description: demo of maya url resolver plugin
#
###########################################################################################
import sys
from maya import OpenMaya, OpenMayaMPx
from murl import MURL

_CACHE = {}


class MUrlResolver(OpenMayaMPx.MPxFileResolver):
    fileResolverName = "astipsFileResolver"
    uriSchemeName = "astips"

    def decode(self, uriValue):
        url_string = uriValue.asString()
        if url_string not in _CACHE:
            murl = MURL(uriValue)
            _CACHE[url_string] = murl.real_path
        return _CACHE[url_string]

    def resolveURI(self, uriValue, mode, ReturnStatus=None):
        return self.decode(uriValue)

    def resolveURIWithContext(self, uriValue, mode, contextNodeFullName, ReturnStatus=None):
        return self.decode(uriValue)

    @classmethod
    def className(cls):
        return cls.__name__

    def resolverName(self):
        return self.fileResolverName

    def uriScheme(self):
        return self.uriSchemeName

    @classmethod
    def resolverCreator(cls):
        return cls()


def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "astips", "1.0")
    try:
        mplugin.registerURIFileResolver(
            MUrlResolver.fileResolverName, MUrlResolver.uriSchemeName, MUrlResolver.resolverCreator
        )
    except:
        sys.stderr.write("Error loading")
        raise


def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterURIFileResolver(MUrlResolver.fileResolverName)
    except:
        sys.stderr.write("Error removing")
        raise
