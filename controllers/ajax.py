# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from ajax.py")


def echo():
    return request.vars.test
    #return "jQuery('#target').html(%s);" % repr(request.vars.name)
