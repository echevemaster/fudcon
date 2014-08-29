# -*- coding: utf-8 -*-
"""
fudcon.ui.frontend.utils
~~~~~~~~~~~~~~~~~~~~~~~~
Utils for frontend
"""

import hashlib
import urllib

def avatar_url(username, size=64, default='retro'):
    openid = "http://%s.id.fedoraproject.org/" % username
    return avatar_url_from_openid(openid, size, default)

def avatar_url_from_openid(openid, size=64, default='retro', dns=False):
    if dns:
        import libravatar
        return libravatar.libravatar_url(
            openid=openid,
            size=size,
            default=default,)
    else:
        query = urllib.urlencode({'s': size, 'd': default})
        hash = hashlib.sha256(openid).hexdigest()
        return "https://seccdn.libravatar.org/avatar/%s?/%s" % (hash, query)
