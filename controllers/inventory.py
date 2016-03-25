# -*- coding: utf-8 -*-
# try something like
from gluon.custom_import import track_changes; track_changes(True)
from cwp_htmlhelpers import cwpeditlink

#must use this for list fields to show rendered value, instead of record ids
def render_docs(ids,row):
      doc=""
      for id in ids:
         doc = doc+db.hazard(id).hazardabbrev+" "#db.wbdocuments(id)
      return doc

def index():
    PageHeader = ""
    #grid = SQLFORM.grid(db.item)

    return dict(PageHeader=PageHeader,grid=grid)
import json
def item():
    PageHeader = "Item"
    addbutton = """<a href ="""+URL("inventory","itemedit")+""" class="btn btn-block btn-success">Add </a>"""
    editlink = """<a href ="""+URL("inventory","itemedit")+"""/%s class="fa fa-fw fa-edit"></a>"""
    #datatables
    #http://www.pyguy.com/web2py/web2py-tutorial-using-the-datatable-jquery-grid-plugin-with-web2py/
    #Cannot use this:
    #item = json.dumps(db(db.item).select().as_list())
    #Because we need the represented value, like "chemical Name"
    #So we do this:
    rows = db(db.item.id>0).select()
    item = json.dumps([dict(id=r.id,name=r.name,disposalcode=r.disposalcode,pounds=r.pounds,container=r.container,shelf=r.shelf,editlink=editlink  % r.id) for r in rows.render()])#adding render to use represented view of fields

    return dict(PageHeader=PageHeader,addbutton=XML(addbutton),results=XML(item))


def itemedit():
    PageHeader = "Item"
    chemname=""
    chemid = 0
    cancelbutton = XML( """<a href ="""+URL("inventory","item")+""" class="btn btn-block btn-warning">Cancel </a>""")
    fields=['name', 'quantity', 'receptacle', 'condition_', 'capacity', 'amount', 'units', 'components', 'comments', 'container', 'shelf']
    if (request.args(0)): #UPDATE RECORD or INSERT RECORD
        record = db.item(request.args(0)) or redirect(URL('error'))
        disposalcode = record.disposalcode #<<<<TODO Add onchange event
        chemname = record.name.chemname
        chemid = record.name
        form = SQLFORM(db.item, record,fields=fields)

    #FIX if there is no shelf
    # labeltext = "Hazardous Waste    Accum. Date: "+"1-1-1907"+"\n"+"Item: "+str(record.id)+"       "+"Shelf:"+str(record.shelf.shelfcode)+"\n"+str(record.name.chemname)+"\n"+str(record.disposalcode)#Dymo Label
        labeltext =''
    else: # ADD RECORD
        form = SQLFORM(db.item,fields=fields)
        disposalcode  = ''
        labeltext = ''
    form.add_button('Back', URL('other_page'))
    #disposalcode = record.disposalcode #<<<<TODO Add onchange event
    #Eplicitly list fields. When using {{=form.custom.widget.Ireceptacle}}, it will only show and edit listed fields
    #By restricting edit fields, you avoid errors
    #form = SQLFORM(db.item, record,fields=fields)

    if form.process().accepted:
        response.flash = 'form accepted'
        try:
            record.update_record(**dict(form.vars))#record is updated
            redirect(URL('item'))
        except NameError:
            response.flash = 'record added'
            redirect(URL('item'))
    elif form.errors: #name is None
       redirect(URL('item'))
    return dict(PageHeader=PageHeader,cancelbutton=cancelbutton,form=form,disposalcode=disposalcode, labeltext=labeltext,chemname=chemname,chemid=chemid)

def container():
    PageHeader = "Container"
    rows = db(db.container.id>0).select()
    #icon="""<a href="""+URL('inventory','containeredit')+"""/%s><div class="col-md-3 col-sm-4"><i class="fa fa-fw fa-edit"></i></div></a>"""
    addbutton = """<a href ="""+URL("inventory","containeredit")+""" class="btn btn-block btn-success">Add </a>"""
    editlink = """<a href ="""+URL("inventory","containeredit")+"""/%s class="fa fa-fw fa-edit"></a>"""
    container = json.dumps([dict(id=r.id,contnum=r.contnum,psn=r.psn,opendate=str(r.opendate),closedate=str(r.closedate),disposalcode=r.disposalcode,shipment=r.shipment,editlink=editlink  % r.id) for r in rows.render()])#adding render to use represented view of fields
    #form = SQLFORM(db.shipment,editable=True,)

    return dict(PageHeader=PageHeader,addbutton=XML(addbutton),results=XML(container))

def containeredit():
    cancelbutton = XML( """<a href ="""+URL("inventory","container")+""" class="btn btn-block btn-warning">Cancel </a>""")
    fields=['psn', 'opendate', 'closedate', 'chemweight', 'grossweight', 'disposalcode', 'profile', 'tsdf', 'containertype', 'containersize', 'containerstyle','containervolume','containerconstruction','closedby','shipment','generator','statewastecode','fedwastecode','accumulationstartdate','contentscomposition','cstate', 'hazardousproperties','rq','unna','descriptor','technicalname','hazdivision','pggroup','psndescriptor','contnum']
    if (request.args(0)): #UPDATE RECORD
        record = db.container(request.args(0)) or redirect(URL('error'))
        form = SQLFORM(db.container, record,fields=fields)
    else: #or INSERT RECORD
        form = SQLFORM(db.container,fields=fields)
    form.add_button('Back', URL('other_page'))
    #process form
    if form.process().accepted:
       response.flash = 'form accepted'
       try:
            record.update_record(**dict(form.vars))#record is updated
            redirect(URL('container'))
       except NameError:
            response.flash = 'record added'
            redirect(URL('container'))
    elif form.errors:
       redirect(URL(form.errors))
       response.flash = 'form has errors'




    return dict(form=form,cancelbutton=cancelbutton,)

def shipment():
    PageHeader = "Shipment"
    rows = db(db.shipment.id>0).select()
    addbutton = """<a href ="""+URL("inventory","shipmentedit")+""" class="btn btn-block btn-success">Add </a>"""
    icon="""<a href="""+URL('inventory','shipmentedit')+"""/%s><div class="col-md-3 col-sm-4"><i class="fa fa-fw fa-edit"></i></div></a>"""
    shipment = json.dumps([dict(id=r.id,manifest=r.manifest,editlink=icon  % r.id) for r in rows.render()])#adding render to use represented view of fields
    #form = SQLFORM(db.shipment,editable=True,)

    return dict(PageHeader=PageHeader,results=XML(shipment), addbutton=XML(addbutton))
def shipmentedit():
    fields=['manifest',]
    if (request.args(0)):
        record = db.shipment(request.args(0)) or redirect(URL('error'))
        form = SQLFORM(db.shipment, record,fields=fields)
        #redirect(URL('container'))
    else:
        form = SQLFORM(db.shipment,fields=fields)
        disposalcode  = ''
        #redirect(URL('container'))
    form.add_button('Back', URL('other_page'))

    if form.process().accepted:
       response.flash = 'form accepted'
       try:
            record.update_record(**dict(form.vars))#record is updated
            redirect(URL('shipment'))
       except NameError:
            response.flash = 'record added'
            redirect(URL('shipment'))
    elif form.errors:
       redirect(URL(form.errors))
       response.flash = 'form has errors'

    return dict(PageHeader=PageHeader,cancelbutton=cancelbutton,form=form)

def chemindex():
    PageHeader = "Chemical Index"
    icon="""<a href="""+URL('inventory','chemindexedit')+"""/%s><div class="col-md-3 col-sm-4"><i class="fa fa-fw fa-edit"></i></div></a>"""
    addbutton = """<a href ="""+URL("inventory","chemindexedit")+""" class="btn btn-block btn-success">Add </a>"""
    db.chemindex.hazard.represent = render_docs # list fields to show rendered value, instead of record ids
    rows = db(db.chemindex.id>0).select()
    chemindex = json.dumps([dict(id=r.id,chemname=r.chemname,group=r.group,state=r.state,disposalcode=r.disposalcode,tsdf=r.tsdf,treatment=r.treatment,hazwastecodes=r.hazwastecodes,hazard=r.hazard,editlink=icon  % r.id) for r in rows.render()])#adding render to use represented view of fields
    return dict(PageHeader=PageHeader,results=XML(chemindex),addbutton=XML(addbutton))


def chemindexedit():

    PageHeader = "Chemical Index"
    fields=['chemname', 'prefix', 'casnum', 'group', 'state', 'disposalcode', 'packtype', 'treatment', 'hazwastecodes', 'hazard', 'components','comments']
    if (request.args(0)): #UPDATE RECORD or INSERT RECORD
        record = db.chemindex(request.args(0)) or redirect(URL('error'))
        #disposalcode = record.Idisposalcode #<<<<TODO Add onchange event
        form = SQLFORM(db.chemindex, record,fields=fields)

        hprint=''
        #hlist=str(record.hazard)
        for number in record.hazard:
            #row = db(db.chemindex.id == int(request.vars.name)).select().first()
            row = db(db.hazard.id == int(number)).select().first()
            hprint=hprint+row.hazardabbrev
        #hazrows = db.hazard.id.contains(hlist, all=True)
        #recid = row.group[:2].upper()+'-'+row.state.upper()+hprint


    else:
        form = SQLFORM(db.chemindex,fields=fields)
        disposalcode  = ''
    form.add_button('Back', URL('other_page'))
    cancelbutton = XML( """<a href ="""+URL("inventory","container")+""" class="btn btn-block btn-warning">Cancel </a>""")


    #response.files.append(URL(r=request,c='static/multiselect',f='jquery.multiSelect.js'))
    #response.files.append(URL(r=request,c='static/multiselect',f='jquery.multiSelect.css'))

    if form.process().accepted:
       response.flash = 'form accepted'
       try:
            record.update_record(**dict(form.vars))#record is updated
            redirect(URL('chemindex'))
       except NameError:
            response.flash = 'record added'
            redirect(URL('chemindex'))
    elif form.errors:
       redirect(URL(form.errors))
       response.flash = 'form has errors'
    return dict(PageHeader=PageHeader,cancelbutton=cancelbutton,form=form,hprint=hprint)
