# -*- coding: utf-8 -*-

###########################################################################################
#
# Author: astips - (animator.well)
#
# Date: 2017.03
#
# Url: https://github.com/astips
#
# Description: nuke url resolver
#
###########################################################################################
import nuke
from studiourl import StudioUrl


nuke.addFilenameFilter(nurl_resolver)


def nurl_resolver(url) :
    studio_url = StudioUrl(url)
    real_path = studio_url.real_path
    """
    do get the real path
    """
    return real_path
