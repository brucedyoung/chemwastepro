#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *


def cwpeditlink(controller,layout): 
   result =  "hye"#"""<a href ="""+URL("%s","%s")+"""/%s class="fa fa-fw fa-edit"></a>""" %  controller,layout
   return result
   
def ip(): return current.request.client


