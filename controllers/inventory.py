# -*- coding: utf-8 -*-
# try something like
def index():
    PageHeader = ""
    #grid = SQLFORM.grid(db.item)

    return dict(PageHeader=PageHeader,grid=grid)
import json
def item():
    PageHeader = "Item"
    #enterbutton = """<button onclick="document.location=\""""+URL("admin","default","design", args=request.application)+""">admin</button>"""
    addbutton = """<a href ="""+URL("inventory","itemedit")+""" class="btn btn-block btn-success">Add </a>"""
   
  
    
    #icon="""<div class="col-md-3 col-sm-4">"""+"""<a href="""+URL('inventory','itemedit')+"""/%s><i class="fa fa-fw fa-edit"></i></div></a>"""
    #editlink=""" <a href="""+URL('inventory','containeredit')+""""class=\"fa fa-fw fa-edit\">Edit</%s>"""
    editlink = """<a href ="""+URL("inventory","itemedit")+"""/%s class="fa fa-fw fa-edit"></a>"""
    #editlink="""<a href="""+URL('inventory','containeredit')+"""/%s><div class="col-md-3 col-sm-4"><i class="fa fa-fw fa-edit"></i></div></a>"""
    #datatables
    #http://www.pyguy.com/web2py/web2py-tutorial-using-the-datatable-jquery-grid-plugin-with-web2py/
    #Cannot use this:
    #item = json.dumps(db(db.item).select().as_list())
    #Because we need the represented value, like "chemical Name"
    #So we do this:
    rows = db(db.item.id>0).select()
    item = json.dumps([dict(id=r.id,Iname=r.Iname,Idisposalcode=r.Idisposalcode,Ipounds=r.Ipounds,Icontainer=r.Icontainer,Ishelf=r.Ishelf,editlink=editlink  % r.id) for r in rows.render()])#adding render to use represented view of fields

    return dict(PageHeader=PageHeader,addbutton=XML(addbutton),results=XML(item))

def itemedit():
    PageHeader = "Item"
    fields=['Iname', 'Iquantity', 'Ireceptacle', 'Icondition', 'Icapacity', 'Iamount', 'Iunits', 'Icomponents', 'Icomments', 'Icontainer', 'Ishelf']
    cancelbutton = XML( """<a href ="""+URL("inventory","item")+""" class="btn btn-block btn-warning">Cancel </a>""")
    if (request.args(0)): #UPDATE RECORD or INSERT RECORD
        record = db.item(request.args(0)) or redirect(URL('error'))
        disposalcode = record.Idisposalcode #<<<<TODO Add onchange event
        form = SQLFORM(db.item, record,fields=fields)
    else:
        form = SQLFORM(db.item,fields=fields)
        disposalcode  = ''
    form.add_button('Back', URL('other_page'))
    #disposalcode = record.Idisposalcode #<<<<TODO Add onchange event
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
    elif form.errors:
       redirect(URL(form.errors))
       response.flash = 'form has errors'


    return dict(PageHeader=PageHeader,cancelbutton=cancelbutton,form=form,disposalcode=disposalcode)

def container():
    PageHeader = "Container"
    rows = db(db.container.id>0).select()
    #icon="""<a href="""+URL('inventory','containeredit')+"""/%s><div class="col-md-3 col-sm-4"><i class="fa fa-fw fa-edit"></i></div></a>"""
    addbutton = """<a href ="""+URL("inventory","containeredit")+""" class="btn btn-block btn-success">Add </a>"""
    editlink = """<a href ="""+URL("inventory","containeredit")+"""/%s class="fa fa-fw fa-edit"></a>"""
    container = json.dumps([dict(id=r.id,ContNum=r.ContNum,PSN=r.PSN,OpenDate=str(r.OpenDate),CloseDate=str(r.CloseDate),cdisposalcode=r.cdisposalcode,cShipment=r.cShipment,editlink=editlink  % r.id) for r in rows.render()])#adding render to use represented view of fields
    #form = SQLFORM(db.shipment,editable=True,)

    return dict(PageHeader=PageHeader,addbutton=XML(addbutton),results=XML(container))
def containeredit():
    cancelbutton = XML( """<a href ="""+URL("inventory","container")+""" class="btn btn-block btn-warning">Cancel </a>""")
    record = db.container(request.args(0)) or redirect(URL('index'))
    fields=['PSN', 'OpenDate', 'CloseDate', 'Chemweight', 'grossweight', 'cdisposalcode', 'Profile', 'tsdf', 'containertype', 'containersize', 'containerstyle','containervolume','containerconstruction','ClosedBy','cShipment','cgenerator','cCAwastecode','cstatefedwastecode','AccumulationStartDate','ccontentscomposition','cstate','chazardousproperties','RQ','UNNA','Descriptor','TechnicalName','HazDivision','PGgroup','PSNdescriptor']
    form = SQLFORM(db.container, record,fields=fields)
    if (request.args(0)):
        record = db.container(request.args(0)) or redirect(URL('error'))
        form = SQLFORM(db.container, record,fields=fields)
        #redirect(URL('container'))
    else:
        form = SQLFORM(db.container,fields=fields)
        disposalcode  = ''
        #redirect(URL('container'))
    form.add_button('Back', URL('other_page'))
    
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
    shipment = json.dumps([dict(id=r.id,Manifest=r.Manifest,editlink=icon  % r.id) for r in rows.render()])#adding render to use represented view of fields
    #form = SQLFORM(db.shipment,editable=True,)

    return dict(PageHeader=PageHeader,results=XML(shipment), addbutton=XML(addbutton))
def shipmentedit():
    record = db.shipment(request.args(0)) or redirect(URL('index'))
    form = SQLFORM(db.shipment, record)
    if form.process().accepted:
       response.flash = 'form accepted'
       record.update_record(**dict(form.vars))
    elif form.errors:
       redirect(URL('index'))
       response.flash = 'form has errors'
    return dict(form=form)

def render_docs(ids,row):
      doc=""
      for id in ids:
         doc = doc+db.hazard(id).hazardabbrev+" "#db.wbdocuments(id)


      return doc

def chemindex():
    PageHeader = "Chemical Index"
    icon="""<a href="""+URL('inventory','chemindexedit')+"""/%s><div class="col-md-3 col-sm-4"><i class="fa fa-fw fa-edit"></i></div></a>"""
    db.chemindex.chazard.represent = render_docs
    rows = db(db.chemindex.id>0).select()
    chemindex = json.dumps([dict(id=r.id,chemname=r.chemname,cgroup=r.cgroup,cstate=r.cstate,cdisposalcode=r.cdisposalcode,tsdf=r.tsdf,treatment=r.treatment,chazwastecodes=r.chazwastecodes,chazard=r.chazard,editlink=icon  % r.id) for r in rows.render()])#adding render to use represented view of fields
    return dict(PageHeader=PageHeader,results=XML(chemindex))


def chemindexedit():
    response.files.append(URL(r=request,c='static/multiselect',f='jquery.multiSelect.js'))
    response.files.append(URL(r=request,c='static/multiselect',f='jquery.multiSelect.css'))
    PageHeader = "Chemical Index"
    record = db.chemindex(request.args(0)) or redirect(URL('error'))
    form = SQLFORM(db.chemindex, record,fields=['chemname', 'cprefix', 'casnum', 'cgroup', 'cstate', 'cdisposalcode', 'cpacktype', 'treatment', 'chazwastecodes', 'chazard', 'components','comments'])
    if form.process().accepted:
       response.flash = 'form accepted'
       record.update_record(**dict(form.vars))
       redirect(URL('chemindex'))
    elif form.errors:
       redirect(URL(form.errors))
       response.flash = 'form has errors'
    return dict(form=form)
