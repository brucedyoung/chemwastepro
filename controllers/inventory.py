# -*- coding: utf-8 -*-
# try something like
from gluon.custom_import import track_changes; track_changes(True)
from cwp_htmlhelpers import cwpeditlink
import cwp_functions


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
    
 
    #cannot use render, because need r.name as number to calculate disposal code by function, so use direct references for remainder of fields that need represent
    #added test if related record exists, example: if r.container else "", so no error if there is no related record
    item = json.dumps([dict(id=r.id,name=r.name.chemname if r.name else "",disposalcode=cwp_functions.returndisposalcode(r.name),pounds=r.pounds,container=r.container.contnum if r.container else "",shelf=r.shelf.shelfcode if r.shelf else "",editlink=editlink  % r.id) for r in rows])# do not rows.render()
    return dict(PageHeader=PageHeader,addbutton=XML(addbutton),results=XML(item))


def itemedit():
    PageHeader = "Item"
    chemname=disposalcode=""
    chemid = 0
    cancelbutton = XML( """<a href ="""+URL("inventory","item")+""" class="btn btn-block btn-warning">Cancel </a>""")
    db.item.container.represent = lambda container, row: container+"hey"
    fields=['name', 'quantity', 'receptacle', 'condition_', 'capacity', 'amount', 'units', 'components', 'comments', 'container', 'shelf']
    if (request.args(0)): #UPDATE RECORD or INSERT RECORD
        record = db.item(request.args(0)) or redirect(URL('error'))
        
        disposalcode=cwp_functions.returndisposalcode(record.name) #get disposalcode string
        #disposalcode = record.disposalcode #<<<<TODO Add onchange event
        chemname = record.name.chemname
        chemid = record.name
        item_id = record.id
        form = SQLFORM(db.item, record,fields=fields)

    #FIX if there is no shelf
    # labeltext = "Hazardous Waste    Accum. Date: "+"1-1-1907"+"\n"+"Item: "+str(record.id)+"       "+"Shelf:"+str(record.shelf.shelfcode)+"\n"+str(record.name.chemname)+"\n"+str(record.disposalcode)#Dymo Label
        labeltext =''
    else: # ADD RECORD
        form = SQLFORM(db.item,fields=fields)
        disposalcode  = ''
        labeltext = ''
        item_id = 0
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
    
    #using web2py built-in helper "A" 
    topactionbutton1 = A(DIV(' Print Label', _class='fa fa-print'), _class='btn btn-block btn-default btn-xs', _id="printButton", target='target1')
    #ID,Chemname,DisposalCode,AccumulationStartDate,Shelf,PrimaryHazard
    #shelveAnchor is used for Javascript on page to change the chemindex id, to calculate new disposal code
    topactionbutton2 = A(DIV(' Shelve Item', _class='fa fa-sign-in'), _id='shelveAnchor', _class='btn btn-block btn-default btn-xs', component=URL('shelve'+'?item_id='+str(item_id)+'&item_chemid='+str(chemid)), target='target1')
    
    return dict(PageHeader=PageHeader,cancelbutton=cancelbutton,form=form,disposalcode=disposalcode, labeltext=labeltext,chemname=chemname,chemid=chemid,item_id=item_id,topactionbutton1=topactionbutton1,topactionbutton2=topactionbutton2)

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
import gluon.contrib.simplejson
def chemindex():
    PageHeader = "Chemical Index"
    icon="""<a href="""+URL('inventory','chemindexedit')+"""/%s><div class="col-md-3 col-sm-4"><i class="fa fa-fw fa-edit"></i></div></a>"""
    addbutton = """<a href ="""+URL("inventory","chemindexedit")+""" class="btn btn-block btn-success">Add </a>"""
    #db.chemindex.hazard.represent = render_docs # list fields to show rendered value, instead of record ids
    #Get chemical hazard list from intermediate table
    #chemassoc_rows = db(db.chemindex_hazard_association.chemindex_id == record.id).select(orderby=db.chemindex_hazard_association.hazard_order)
    
    #Normalized hazard list
     ###SO SLOW!!!!
    #Calculating disposalcode and hazard takes too long
    

    rows = db(db.chemindex.id>0).select(db.chemindex.id,db.chemindex.chemname,db.chemindex.group_,db.chemindex.state,db.chemindex.disposalcode,db.chemindex.tsdf,db.chemindex.treatment,db.chemindex.hazwastecodes,db.chemindex.hazard,db.chemindex.hazardlistabbrev).as_list()

    #rendered_row = rows.render(0, fields=[db.mytable.duetime])
    #rows = row.as_list()
    #chemindex = json.dumps([dict(id=r.id,chemname=r.chemname,group_=r.group_,state=r.state,disposalcode=r.disposalcode,tsdf=r.tsdf,treatment=r.treatment,hazwastecodes=r.hazwastecodes,hazard=r.treatment,editlink=icon) for r in cirows.render(fields=[db.chemindex.myfield])#adding render to use represented view of fields
                                        
    return dict(PageHeader=PageHeader,results=XML(json.dumps(rows)),addbutton=XML(addbutton))




def chemindexedit():
    hprint=''
    PageHeader = "Chemical Index"
    hazardlist ='' #hazard list is the potential hazads from hazard table
    chemhazardlist= '' #chemhazardlist is the actual hazards associated with the chemical reflected in the chemindex_hazard_association table
    
    
    # (1) Get available hazards - make ordered list for jquery sortable to pull from
    hazards = [(r.id, r.hazardname) for r in db(db.hazard).select(orderby=db.hazard.hazard_order)]
    hazardid, hazardname = zip(*hazards)#seperate into two lists
    #Create HTML unordered list
    for idx, r in enumerate(hazardid):
        hazardlist += str(LI(hazardname[idx], _class='ui-state-default ui-sortable-handle', _id=hazardid[idx]))
    fields=['chemname', 'casnum', 'group_', 'state', 'disposalcode', 'packtype', 'treatment','components', 'hazwastecodes', 'comments']#
    if (request.args(0)): #UPDATE RECORD or INSERT RECORD
        record = db.chemindex(request.args(0)) or redirect(URL('error'))

        #disposalcode = record.Idisposalcode #<<<<TODO Add onchange event
        
        #Add a hidden field hazard_list to return the result of the Chemical Hazard unordered list
        #Pass value = blank
        #If hazard_list gets value, it means the sortable list as changed, and associations should be updated
        form = SQLFORM(db.chemindex, record,fields=fields,hidden=dict(hazard_list=''))
        #NORMALIZED
        rows = db(db.chemindex_hazard_association.chemindex_id == record.id).select(orderby=db.chemindex_hazard_association.hazard_order)
        for row in rows:
            chemhazardlist += str(LI(row.hazard_id.hazardname, _class='ui-state-default ui-sortable-handle', _id=row.hazard_id))
            


            
        #NOT USED!!!
        #hlist=str(record.hazard)
        
        #for number in record.hazard: #build hazard list for disposal code
        #    #row = db(db.chemindex.id == int(request.vars.name)).select().first()
        #    row = db(db.hazard.id == int(number)).select().first()
        #    hprint=hprint+row.hazardabbrev
        #hazrows = db.hazard.id.contains(hlist, all=True)
        #recid = row.group[:2].upper()+'-'+row.state.upper()+hprint


    else:#ADD NEW RECORD
        form = SQLFORM(db.chemindex,fields=fields,hidden=dict(hazard_list=''))
        disposalcode  = ''
    form.add_button('Back', URL('other_page'))
    cancelbutton = XML( """<a href ="""+URL("inventory","container")+""" class="btn btn-block btn-warning">Cancel </a>""")

    if form.process().accepted:
       response.flash = 'form accepted'
       #update hazardlistabbrev
       form.vars.hazardlistabbrev = (cwp_functions.returnhazardlistabbrev(form.vars.id))
       #treatmentabbrev
       #tsdfabbrev
    
       try:

            #update hazard list
            ohazard_list = []
            hazard_list=(request.vars.hazard_list)
            if(hazard_list!=''): #the chemical hazard sortable UL was modified
                ohazard_list=hazard_list.split(",") # create ordered list
                db(db.chemindex_hazard_association.chemindex_id==form.vars.id).delete() #Delete all associations for chemindexid
                for index, hazardid in enumerate(ohazard_list):
                    db.chemindex_hazard_association.insert(chemindex_id=form.vars.id,hazard_id=hazardid,hazard_order=index)  

            record.update_record(**dict(form.vars))#record is updated
            redirect(URL('chemindex')+str(ohazard_list))

         
       except NameError:
         
        
            response.flash = 'record added'
            redirect(URL('chemindex'))
    elif form.errors: #problems with required fields
       redirect(URL(form.errors))
       response.flash = 'form has errors'


    
    return dict(PageHeader=PageHeader,cancelbutton=cancelbutton,form=form,hprint=hprint,chemhazardlist=XML(chemhazardlist),hazardlist=XML(hazardlist))


def shelve():
    #use this to control the dropdown on the item edit page.
    #That way, the user has to save the record for changes to take place.
    #otherwise, cancels
    responsestr = "no"
    chemhazardlistc=""
    item_id=request.vars.item_id
    item_chemid=request.vars.item_chemid
    if ((item_id > "") & (item_chemid > "")):
        chemindex_row = db(db.chemindex.id == int(item_chemid)).select().first() #should be only one
        disposalcode=cwp_functions.returndisposalcode(chemindex_row.id) #get disposalcode string
        row = db(db.shelf.disposalcode == disposalcode).select().first()#get the first one. Could reduce by creation date or shelf number
    if row is None:
        #user alert of change
        responsestr = "No shelf found"
        #javascript making change
        response.js = "var element = document.getElementById('item_shelf');element.value = 0;"
    else:
        #user alert of change
        responsestr = "Item shelved"
        #javascript making change
        response.js =  ("var element = document.getElementById('item_shelf');element.value = %s;" % row.id)
    return (responsestr)
