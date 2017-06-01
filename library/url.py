# -*- coding: utf-8 -*-

###########################################################################################
#
# Author: astips - (animator.well)
#
# Date: 2017.03
#
# Url: https://github.com/astips
#
# Description: studio url base class
#
###########################################################################################

"""
The normal url is:

    astips://username:password@example.com:8042/over/there/asset/lay?type=animal&name=narwhal#nose
      \_/    \_______________/ \_________/ \__/\___________________/ \______________________/ \__/
       |            |               |       |           |                      |                |
       |       [userinfo]        hostname [port]        |                   [query]        [fragment]
       |     \________________________________/         |
     scheme                  |                          |
                         authority                   [path]

Which option in [] is optional.

e.g.
    astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1

"""


from . import urlparse as _urlparse


class URL(object):
    """
    This class is a wrapper of urlparse module.
    To use it, you need give a url string. Then this class will split it automatic.
    You can get any part of the url string which you want.
    """
    def __init__(self, url):
        """
        Give a url string to init a URL object.
        e.g.
            url = URL('astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1')
        """
        super(URL, self).__init__()
        self.result = {"url": url}

    @property
    def url(self):
        """
        str
        The url string which you gave.
        e.g.
            URL('astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1').url
                => 'astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1'
        """
        return self.result["url"]

    @property
    def scheme(self):
        """
        str
        The url's scheme.
        e.g.
            URL('astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1').scheme
                => 'astips'
        """
        return self.parse_result["scheme"]

    @property
    def netloc(self):
        """
        str
        The url's netloc.
        e.g.
            URL('astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1').netloc
                => 'ple:123456@show:8080'
        """
        return self.parse_result["netloc"]

    @property
    def username(self):
        """
        str
        The user's username.
        e.g.
            URL('astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1').username
                => 'ple'
        """
        return self.parse_result["username"]

    @property
    def password(self):
        """
        str
        The user's password.
        e.g.
            URL('astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1').password
                => '123456'
        """
        return self.parse_result["password"]

    @property
    def hostname(self):
        """
        str
        The server's hostname.
        e.g.
            URL('astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1').hostname
                => 'show'
        """
        return self.parse_result["hostname"]

    @property
    def port(self):
        """
        int
        The server's port.
        e.g.
            URL('astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1').port
                => 8080
        """
        return self.parse_result["port"]

    @property
    def path(self):
        """
        str
        The server's absolute path.
        e.g.
            URL('astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1').path
                => '/WHD/din'
        """
        return self.parse_result["path"]

    @property
    def query(self):
        """
        dict
        The url's query.
        e.g.
            URL('astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1').query
                => {'version': ['test/v001'], 'role': ['maya_file']}
        """
        return self.parse_result["query"]

    @property
    def fragment(self):
        """
        str
        The url's fragment.
        e.g.
            URL('astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1').fragment
                => '1'
        """
        return self.parse_result["fragment"]

    @property
    def is_valid(self):
        """
        bool
        If the url is valid.
        e.g.
            URL('astips://ple:123456@show:8080/Project_name/character_name?version=test/v001&role=orig#1').is_valid
                => True
        """
        return bool(self.scheme and self.hostname)

    @property
    def parse_result(self):
        """
        dict
        All of the url info.
        You should not use it.
        """
        if "parse_result" not in self.result:
            _parse_result = _urlparse.urlparse(self.url)
            self.result["parse_result"] = {
                "scheme": _parse_result.scheme,
                "netloc": _parse_result.netloc,
                "username": _parse_result.username,
                "password": _parse_result.password,
                "hostname": _parse_result.hostname.lower() if isinstance(_parse_result.hostname, basestring) else None,
                "port": _parse_result.port,
                "path": _parse_result.path,
                "query": _urlparse.parse_qs(_parse_result.query),
                "fragment": _parse_result.fragment
            }
        return self.result["parse_result"]
