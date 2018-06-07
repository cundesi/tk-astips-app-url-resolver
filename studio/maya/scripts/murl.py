# -*- coding: utf-8 -*-

###########################################################################################
#
# Author: astips - (animator.well)
#
# Date: 2017.03
#
# Url: https://github.com/astips
#
# Description: demo of maya url
#
###########################################################################################
import re
import maya.OpenMaya as OpenMaya
from studiourl import StudioUrl


class MURL(StudioUrl):
    def __init__(self, url):
        if isinstance(url, OpenMaya.MURI):
            url_string = url.asString()
        else:
            url_string = url

        self.frame = None
        split_url_string = re.split("\.(\d+)$", url_string)
        if len(split_url_string) > 1:
            url_string = split_url_string[0]
            self.frame = split_url_string[1]

        super(MURL, self).__init__(url_string)

    @property
    def real_path(self):
        real_path = super(MURL, self).real_path
        if self.frame:
            hash_count = real_path.count("#")
            frame_count = len(self.frame)
            if hash_count < frame_count:
                real_path = real_path.replace("#" * hash_count, self.frame)
            else:
                real_path = real_path.replace(
                    "#" * hash_count, "0" * (hash_count - frame_count) + self.frame
                )

        return real_path
