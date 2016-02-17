# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    addbutton =""
    PageHeader = "Dashboard"
    #response.flash = T("Hello World")
    itemcount = db(db.item.id > 0).count()
    containercount = db(db.container.id > 0).count()
    shipmentcount = db(db.shipment.id > 0).count()
    chemindexcount = db(db.chemindex.id > 0).count()
    return dict(PageHeader=PageHeader,message=T('Welcome to OHWM!'),itemcount=itemcount,containercount=containercount,shipmentcount=shipmentcount,chemindexcount=chemindexcount,addbutton=addbutton)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())
#pyfpdf elements:
#name: placeholder identification
#type: 'T': texts, 'L': lines, 'I': images, 'B': boxes, 'BC': barcodes
#x1, y1, x2, y2: top-left, bottom-right coordinates (in mm)
#font: ie "Arial"
#size: text size in points, ie. 10
#bold, italic, underline: text style (non-empty to enable)
#foreground, background: text and fill colors, ie. 0xFFFFFF
#align: text aling, 'L': left, 'R': right, 'C': center
#text: default string, can be replaced at runtime
#priority: Z-Order
#multiline: None for single line (default), True to for multicells (multiples lines), False trims to fit exactly the space defined

def generate():
    from gluon.contrib.pyfpdf import Template
    import os.path
    elements = [ 
     #letter paper =  215.9 mm x 279.4 mm
    { 'name': 'background', 'type': 'I', 'x1': 3.3, 'y1': 3.3, 'x2': 212.6, 'y2': 276.1, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'logo', 'priority': 0, },
    { 'name': 'Generator_ID_Number', 'type': 'T', 'x1': 50.0, 'y1': 40.5, 'x2': 12.0, 'y2': 12.0, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
    { 'name': 'Page_1_of', 'type': 'T', 'x1': 105.0, 'y1': 40.5, 'x2': 12.0, 'y2': 12.0, 'font': 'Arial', 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
    { 'name': 'Emergency_Response_Phone', 'type': 'T', 'x1': 120.0, 'y1': 40.5, 'x2': 12.0, 'y2': 12.0, 'font': 'Arial', 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
    { 'name': 'Manifest_Tracking_Number', 'type': 'T', 'x1': 157.0, 'y1': 40.5, 'x2': 12.0, 'y2': 12.0, 'font': 'Arial', 'size': 12.0, 'bold': 1, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, },
    { 'name': 'Generator_Name_Address', 'type': 'T', 'x1': 20.0, 'y1': 40, 'x2': 100.0, 'y2': 37.0, 'font': 'Arial', 'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, 'multiline' : 3 },
    { 'name': 'Generator_Site_Address', 'type': 'T', 'x1': 115.0, 'y1': 40, 'x2': 180.0, 'y2': 37.0, 'font': 'Arial', 'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, 'multiline' : 3 },
    { 'name': 'Generator_Name_Phone', 'type': 'T', 'x1': 35.0, 'y1': 49, 'x2': 180.0, 'y2': 37.0, 'font': 'Arial', 'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, 'multiline' : 3 },
    { 'name': 'line1', 'type': 'L', 'x1': 100.0, 'y1': 25.0, 'x2': 100.0, 'y2': 57.0, 'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 3, },
    { 'name': 'barcode', 'type': 'BC', 'x1': 20.0, 'y1': 246.5, 'x2': 140.0, 'y2': 254.0, 'font': 'Interleaved 2of5 NT', 'size': 0.75, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '200000000001000159053338016581200810081', 'priority': 3, },
]
    # self.image("logo.png", x=10, y=8, w=23)
    f = Template(format="A4",
             elements = elements,
             title="Sample Invoice", author="Sample Company",
             subject="Sample Customer", keywords="Electronic TAX Invoice")
    f.add_page()
    
    #logo=os.path.join(request.env.web2py_path,"static","images","manifest.png")
     #self.image(logo,10,8,33)

    #f["company_logo"] = os.path.join(request.env.web2py_path, "gluon", "contrib", "pyfpdf", "tutorial", "logo.png"
    #os.path.join(request.env.web2py_path,request.folder,"static","images","g3001.png")
    f["background"] = os.path.join(request.env.web2py_path,request.folder,"static","images","manifest.png")
    #f["background"] = URL('static', 'images', args="manifest.png")
    #f["Generator_ID_Number"] = "123456789"
    #f["company_logo"] = "pyfpdf/tutorial/logo.png"
    f["Generator_ID_Number"] = "123456789"
    f["Page_1_of"] = "2"
    f["Emergency_Response_Phone"] = "510-642-6908"
    f["Manifest_Tracking_Number"] = "NYB54321"
    f["Generator_Name_Address"] = "Somewhere, CA, USA\n123 Anywhere Rd.\nMain Campus"
    f["Generator_Name_Phone"] = "510-642-6073"
    f["Generator_Site_Address"] = "Somewhere, CA, USA\n123 Anywhere Rd.\nMain Site"


    
    response.headers['Content-Type']='application/pdf'
    return f.render('invoice.pdf', dest='S')


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
