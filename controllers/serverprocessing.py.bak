# -*- coding: utf-8 -*-
# This is for the Datatables Service Side Processing
# Expects ajax calls, returns json

import json
import cwp_functions
def chemindex(): 
    tablecount = db(db.chemindex).count()
    fields=['id','chemname','group_','state','disposalcode','tsdf','treatment','hazardlistabbrev','hazwastecodes']#this sets what fields are available using query, and determines inital sort order, Could use Datatables return instead
    sel=[db.chemindex[field] for field in fields] 
    textfields=['chemname']#determines which fields are searchable
    orderby = [db.chemindex[fields[1]]] #inital sort
    #Receive datatables parameters
    if(request.vars.draw):#pass this back to increment
        drawint=int(request.vars.draw)#cast to int to avoid XSS
    else:
        drawint=0
    if(request.vars.start):#beginning of display set
        dtstart = int(request.vars.start)
    else:
        dtstart=10
    if(request.vars.length):#how many records to display
        dtlength = int(request.vars.length)
    else:
        dtlength=10
    #Search Value is contains
    searchval=request.vars.get('search[value]', None) 
    if(searchval):
        dtsearch = searchval
    else:
        dtsearch=''
    #Order Column
    ordercol=request.vars.get('order[0][column]', None) 
    if(ordercol):

        #Order Direction
        orderdir=request.vars.get('order[0][dir]', None) 
        if (orderdir=="asc"):
            #build order statement - this is for single sort. Could implement multisort
           orderby = [db.chemindex[fields[int(ordercol)]]]
        else:
           orderby = [~db.chemindex[fields[int(ordercol)]]]
        
    #Sample Custom Query
    #''.join('%s dtsearch % level for level in fields)
    #Custom Query
    if (dtsearch):
        query=[db.chemindex[field].contains(dtsearch) for textfield in textfields] 
    else: #Default Query
        query=[db.chemindex]
    rowsc = db(*query).select(*sel, orderby=orderby)#, limitby=(dtstart,dtlength)
    rows = db(*query).select(*sel, orderby=orderby, limitby=(dtstart,dtstart+dtlength))
    rowscount=len(rowsc)
    #icon="""<a href="""+URL('inventory','shipmentedit')+"""/%s><div class="col-md-3 col-sm-4"><i class="fa fa-fw fa-edit"></i></div></a>"""
    icon = str(ordercol)+"%s"  
    chemindex = """{"draw": """+str(drawint)+""", "recordsTotal": """+str(tablecount)+""", "recordsFiltered": """+str(rowscount)+""","data":"""
    chemindex += json.dumps([dict(id=r.id,chemname=r.chemname,group_=r.group_,state=r.state,disposalcode=r.disposalcode,tsdf=r.tsdf,treatment=r.treatment,hazardlistabbrev=r.hazardlistabbrev,hazwastecodes=r.hazwastecodes,editlink=icon  % r.id) for r in rows.render()])#adding render to use represented view of fields
    chemindex += """}"""              
    return (chemindex)
def shipment():
    tablecount = db(db.shipment).count()
    fields=['id','manifest']#this sets what fields are available using query, and determines inital sort order, Could use Datatables return instead
    sel=[db.shipment[field] for field in fields] 
    textfields=['manifest']#determines which fields are searchable
    orderby = [db.shipment[fields[1]]] #inital sort
    #Receive datatables parameters
    if(request.vars.draw):#pass this back to increment
        drawint=int(request.vars.draw)#cast to int to avoid XSS
    else:
        drawint=0
    if(request.vars.start):#beginning of display set
        dtstart = int(request.vars.start)
    else:
        dtstart=10
    if(request.vars.length):#how many records to display
        dtlength = int(request.vars.length)
    else:
        dtlength=10
    #Search Value is contains
    searchval=request.vars.get('search[value]', None) 
    if(searchval):
        dtsearch = searchval
    else:
        dtsearch=''
    #Order Column
    ordercol=request.vars.get('order[0][column]', None) 
    if(ordercol):

        #Order Direction
        orderdir=request.vars.get('order[0][dir]', None) 
        if (orderdir=="asc"):
            #build order statement - this is for single sort. Could implement multisort
           orderby = [db.shipment[fields[int(ordercol)]]]
        else:
           orderby = [~db.shipment[fields[int(ordercol)]]]
        
    #Sample Custom Query
    #''.join('%s dtsearch % level for level in fields)
    #Custom Query
    if (dtsearch):
        query=[db.shipment[field].contains(dtsearch) for textfield in textfields] 
    else: #Default Query
        query=[db.shipment]
    rowsc = db(*query).select(*sel, orderby=orderby)#, limitby=(dtstart,dtlength)
    rows = db(*query).select(*sel, orderby=orderby, limitby=(dtstart,dtstart+dtlength))
    rowscount=len(rowsc)
    #icon="""<a href="""+URL('inventory','shipmentedit')+"""/%s><div class="col-md-3 col-sm-4"><i class="fa fa-fw fa-edit"></i></div></a>"""
    icon = str(ordercol)+"%s"  
    shipment = """{"draw": """+str(drawint)+""", "recordsTotal": """+str(tablecount)+""", "recordsFiltered": """+str(rowscount)+""","data":"""
    shipment += json.dumps([dict(id=r.id,manifest=r.manifest,editlink=icon  % r.id) for r in rows.render()])#adding render to use represented view of fields
    shipment += """}"""              
    return (shipment)
