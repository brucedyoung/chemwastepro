#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *


#http://www.web2pyslices.com/slice/show/1374/full-breadcrumbs
def breadcrumb(arg_title=None):
        "Create breadcrumb links for current request"
        # make links pretty by capitalizing and using 'home' instead of 'default'
        #pretty = lambda s: s.replace('default', 'Início').replace('_', ' ').capitalize()
        menus = [A('Início', _href=URL(r=request, c='default', f='index'))]
        if request.controller != 'default':
            # add link to current controller
            menus.append(A(T(pretty(request.controller)), _href=URL(r=request, c=request.controller, f='index')))
            if request.function == 'index':
                # are at root of controller
                menus[-1] = A(T(pretty(request.controller)), _href=URL(r=request, c=request.controller, f=request.function))
            else:
                try:
                    for parent in session.bc[request.function]['parents']: 
                        url = session.bc[request.function]['parents'][parent]['url']
                        title = session.bc[request.function]['parents'][parent]['title']
                        menus.append(A(T(title),  _href=url))

                except :
                     pass
                # except HTTP, e:
                     #print 'error', e, 'occurred'

                finally:
                    try:
                        if not session.blockfunction:
                            menus.append(A(T(pretty(request.function)), 
                                   _href=URL(r=request, c=request.controller, f=request.function)))
                    except:
                        pass
            if request.args and arg_title:
                args=request.args
                menus.append(A(T(arg_title), _href=URL(r=request,f=request.function,args=args)))
        else:
            #menus.append(A(pretty(request.controller), _href=URL(r=request, c=request.controller, f='index')))
            if request.function != 'index':
                # are at root of controller
                # are at function within controller
                #menus.append(A(T(pretty(request.function)), _href=URL(r=request, c=request.controller, f=request.function)))
            # you can set a title putting using breadcrumbs('My Detail Title')
                try:
                    for parent in session.bc[request.function]['parents']: 
                        url = session.bc[request.function]['parents'][parent]['url']
                        title = session.bc[request.function]['parents'][parent]['title']
                        menus.append(A(T(title),  _href=url))

                except :
                     pass
                # except HTTP, e:
                     #print 'error', e, 'occurred'

                finally:
                    try:
                        if not session.blockfunction:
                            menus.append(A(T(pretty(request.function)), 
                                   _href=URL(r=request, c=request.controller, f=request.function)))
                    except:
                        pass

            if request.args and arg_title:
                args=request.args
                menus.append(A(T(arg_title), _href=URL(r=request, f=request.function,args=args)))

        return XML(' > '.join(str(m) for m in menus))
