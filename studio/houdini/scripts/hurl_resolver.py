# -*- coding: utf-8 -*-

###########################################################################################
#
# Author: astips (animator.well)
#
# Date: 2017.05
#
# Url: https://github.com/astips
#
# Description: Houdini url resolver scripts
#     
###########################################################################################
from studiourl import StudioUrl


def hurl_checker(burl):
    return StudioUrl(burl).is_valid


def hurl_helper(burl):
    return StudioUrl(burl).real_path
