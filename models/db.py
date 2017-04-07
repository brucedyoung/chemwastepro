# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)
#Put a file in the root level of web2py, alongside the applications folder, with the connection string
#example connection string = mysql://db_user:Password!@localhost/chemwastepro
file = open('chemwasteproconnectionstring.txt', 'r')
connectionstring = file.readline().rstrip('\n') #strip newline just in case
file.close()
if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    #db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
    db = DAL(connectionstring,migrate=False,lazy_tables=True)
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))
    
#add the db object to the current thread local object, which can then be imported and accessed within the modules
from gluon import current
current.db = db
## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


#Security stuff. Make sure your web server is set to HTTPS only.
response.headers['X-Frame-Options'] = "SAMEORIGIN"
response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
#session._secure=True # Sets cookies to "HTTPOnly; Secure" # this only works if the site is HTTPS
#response.headers['Strict-Transport-Security'] = "max-age=31536000" # this only works if the site is HTTPS


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
#auth.define_tables(username=False, signature=False)

## configure emails
#mail = auth.settings.mailer
#mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
#mail.settings.sender = myconf.take('smtp.sender')
#mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

##Define some globals
PageHeader = ""
topactionbutton1 = ""
topactionbutton2 = ""
topactionbutton3 = ""
topactionbutton4 = ""
enterbutton = cancelbutton = ''


#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

## This database structure uses "list:reference" which is a means to de-normalize many to many tables.
#http://web2py.com/books/default/chapter/29/6#list--type--and-contains
#This makes the database structure simpler by avoiding junction tables
#web2py the "list:reference" is a string with bar delimiters between the record id, example "|1|2|"

    #Multi-select code
    #http://www.web2pyslices.com/slice/show/1395/jquery-multi-select-widget

# Naming Scheme
# use prefix "c" for child tables, like units.


db.define_table('state', # NOT USED?
                Field('name','string'),
                format='%(name)s'
               )
db.define_table('receptacle',
                Field('name','string'),
                format='%(name)s'
               )
db.define_table('units',
                Field('name','string'),
                format='%(name)s'
               )

#'condition' is a reserved word in SQL, so we use 'condition_' per the Python style guide
db.define_table('condition_',
                Field('name','string'),
                format='%(name)s'
               )
#Conversions are needed to match shipping requirements. For example, asbestos may be collected as pounds, but shipped as yards
#Also, billing may be based on a fixed unit, like gallons
db.define_table('conversions',
                Field('unitsfrom', 'reference units'),
                Field('conversionfactor', 'decimal(65,10)'),
                format='%(name)s'
               )
#The TSDF and Treatment codes purpose are twofold.
# First to segregate chemicals for storage, lab packing and shipping
# Second to use the codes to complete the Federal Regulation Biennial Report (also known as the Hazardous Waste Report)
#TSDF = Hazardous Waste Treatment, Storage, and Disposal Facility
db.define_table('tsdf',
                Field('tsdfname','string'),
                Field('tsdfnumber','string'),

                format='%(tsdfname)s'
                )
#Treatment codes come from http://www3.epa.gov/epawaste/hazard/transportation/manifest/pdf/codes.pdf
db.define_table('treatment',
                Field('treatmentname','string'),
                #Hazardous Waste Report TreatmentCode
                Field('treatmentcode','string',length='4'),
                Field('treatnameabbrev','string',length='10'),
                format='%(treatnameabbrev)s'
                )
db.define_table('hazard',
                Field('hazardname','string'),
                Field('hazard_order','integer'),
                Field('hazardabbrev','string'),
                format='%(hazardname)s'
                )
db.define_table('fedwastecode',
                Field('code','string',length='4'),
                Field('wastedescription','string'),
                format='%(code)s%(wastedescription)s'
               )
db.define_table('unna',
                Field('name',type='string'),
                Field('unna',type='string'),
                )
import cwp_functions
db.define_table('chemindex',
                Field('id','id'),
                Field('chemname','string'),
                Field('casnum','string'),
                Field('state','string'),
                Field('group_','string'), #MYSQL reserved word, trailing underscore
                #DONT USE - Try to compute Disposal Code dynmaically in every case
                #Field('disposalcode',compute=lambda r: cwp_functions.returndisposalcode(r['id'])),
                Field('disposalcode'),
                Field('hazard',compute=lambda r: cwp_functions.returnhazardlistabbrev(r['id'])),
                Field('tsdf','reference tsdf'),
                Field('treatment','reference treatment'),
                #Field('hazwastecodes',compute=lambda r: ','.join(map(lambda v : db.fedwastecode[v].code , r['fedwastecode']))),
                Field('hazwastecodes'),
                #State Hazardous Waste Codes - http://www3.epa.gov/epawaste/inforesources/data/br13/br13-specification.pdf
                Field('fedwastecode','list:string', requires = IS_EMPTY_OR(IS_IN_DB(db,'fedwastecode.id', db.fedwastecode._format,multiple=True))), #like D001, D002
                Field('dotpsn','boolean'), #Department of Transportation Proper Shipping Name - if checked, do not edit name
                Field('packtype','string', default=''),
                Field('comments','text'),
                Field('components','text'),# similar to mixture
                Field('unna','reference unna'),# United Nations/United State List of Hazardous Materials
                Field('pg','string'), #Packing Group
                Field('hazardlistabbrev'),

                #Field('hazardlistabbrev',compute = lambda r: (str(r['id']))),
                format='%(chemname)s',
               )
               

                
db.chemindex.packtype.requires=IS_EMPTY_OR(IS_IN_SET(('','LP','BU')))
db.chemindex.tsdf.requires = IS_EMPTY_OR(IS_IN_DB(db,'tsdf.id','%(tsdfname)s'))
db.chemindex.treatment.requires = IS_EMPTY_OR(IS_IN_DB(db,'treatment.id','%(treatnameabbrev)s'))
db.chemindex.group_.requires=IS_EMPTY_OR(IS_IN_SET(('Inorganic','Organic'))) # IN = Inorganic, OR = Organic
db.chemindex.state.requires=IS_EMPTY_OR(IS_IN_SET(('Solid','Liquid','Gas')))
db.chemindex.unna.requires = IS_EMPTY_OR(IS_IN_DB(db,'unna.id','%(unna)s'))
db.chemindex.editlink = Field.Virtual('editlink', lambda row: """<a href="""+URL('inventory','chemindexedit')+"""/"""+str(row.chemindex.id)+"""><div class="col-md-3 col-sm-4"><i class="fa fa-fw fa-edit"></i></div></a>""")




#db.item.total_price =         Field.Virtual('total_price',lambda row: row.item.unit_price * row.item.quantity)


#Reference http://blog.jotbe-fx.de/articles/2522/web2py-Normalized-many-to-many-model-with-multiselect-drop-down
db.define_table('chemindex_hazard_association',
                Field('chemindex_id', 'reference chemindex'),
                Field('hazard_id', 'reference hazard'),
                Field('hazard_order', 'integer'),
               )

#db.chemindex.hazards_st = Field.Method(lambda id,row:db(db.chemindex_hazard_association.chemindex_id == row.id).select().first().hazard_id)

db.define_table('psn', # Proper Shipping Name
                Field('propershippingname',type='string',
                      required=True),
                format='%(propershippingname)s'
               )

#Physical hazardous waste storage cabinets
#TODO - should also segregate by Inorganic / Organic
#Cannot use just Hazard
db.define_table('cabinet',
                Field('name','string'),
                Field('cabinetcode','reference hazard'),
                Field('group_','string'), #MYSQL reserved word, trailing underscore
                )
# ALLOW EMPTY??? Or require cabinet group
db.cabinet.group_.requires=IS_EMPTY_OR(IS_IN_SET(('Inorganic','Organic'))) # IN = Inorganic, OR = Organic

#Physical shelves or tubs inside the cabinets
db.define_table('shelf',
                Field('shelfcode','string',default=""),
                Field('disposalcode','string'),
                Field('scabinet','reference cabinet'),
                format='%(shelfcode)s'
               )
db.shelf.scabinet.requires = IS_IN_DB(db,'cabinet.id','%(name)s')#make drop down list of cabinets

#drum, pallet, bin
db.define_table('shipment',
                Field('manifest',type='string',
                      required=True),
                format='%(manifest)s'
               )
db.define_table('containertype',
                Field('containertypecode',type='string',required=True),
                Field('name',type='string'),
                format='%(containertypecode)s - %(name)s'
               )

# If you have more than one EPA ID number site shipping Hazardous Waste Manifests
db.define_table('generator',
                Field('name',type='string'),
                Field('epaid',type='string'), #Environmental Protection Agency Identification Number
                Field('address',type='string'),
                )

db.define_table('container',
                Field('contnum','string',default="1000"),#an alphanumeric identifier for container. Regulations say drum number must be unique per shipment
                Field('psn','reference psn'), #PSN= Proper Shipping Name
                Field('opendate','date'),
                Field('closedate','date'),
                Field('accumulationstartdate','date'),
                Field('chemweight','decimal(65,2)'),
                Field('grossweight','decimal(65,2)'),
                Field('disposalcode','string'),
                Field('profile','string'), #Waste profile from TSDF
                Field('tsdf','reference tsdf'),
                Field('containertype','reference containertype'), # from regulations
                Field('containersize','string'), #standard measurement, example 55Gal drum
                Field('containervolume','integer'),
                Field('containerstyle','string'),
                Field('containerconstruction','string'),
                Field('closedby','string'),
                Field('statewastecode','string'),#california waste code
                Field('fedwastecode','list:string', requires = IS_IN_DB(db,'fedwastecode.id', db.fedwastecode._format,multiple=True)), #like D001, D002
                Field('shipment','reference shipment'),
                Field('generator','reference generator'),
                Field('contentscomposition','string'),
                Field('cstate','string'),
                Field('rq','boolean'), # Reportable Quantity
                Field('unna','reference unna'),
                Field('descriptor','string'),
                Field('technicalname','string'),
                Field('hazdivision','string',requires = IS_EMPTY_OR(IS_IN_SET(('1.1','1.2','1.3','1.4','1.5','1.6','2.1','2.2','2.3','3','4.1','4.2','4.3','5','5.1','6.1','6.2','7','8','9','NON-RCRA')))),
                Field('pggroup','string',requires = IS_EMPTY_OR(IS_IN_SET(('FORBDN','PG I','PG I-II','PG I-III','PG II','PG II-III','PG III')))), # packing group
                Field('psndescriptor','string'),
                Field('hazardousproperties','list:string', requires = IS_IN_DB(db,'hazard.id', db.hazard._format,multiple=True)),
                format='%(contnum)s'
               )
db.container.tsdf.requires = IS_EMPTY_OR(IS_IN_DB(db,'tsdf.id','%(tsdfname)s'))
db.container.containerstyle.requires=IS_EMPTY_OR(IS_IN_SET(('Bin','Box','Pail','Drum','End Dump','Pallet','Salvage','Tank Truck','Cylinder')))    
db.container.containersize.requires=IS_EMPTY_OR(IS_IN_SET(('','05G','08G','10G','12G','15G')))
db.container.containerconstruction.requires=IS_EMPTY_OR(IS_IN_SET(('NA','Plastic','Wood','Metal','Fiber')))
db.container.containertype.requires = IS_EMPTY_OR(IS_IN_DB(db,'containertype.id','%(name)s')), #allow Containertype to be empty
db.container.containertype.widget = SQLFORM.widgets.options.widget #make drop-down list    
db.container.psn.requires = IS_EMPTY_OR(IS_IN_DB(db,'psn.id','%(propershippingname)s')), #allow PSN to be empty
db.container.psn.widget = SQLFORM.widgets.options.widget #make drop-down list    
db.container.generator.requires = IS_EMPTY_OR(IS_IN_DB(db,'generator.id','%(name)s')), #allow container ID to be empty 
db.container.generator.widget = SQLFORM.widgets.options.widget #make drop-down list    
db.container.cstate.requires=IS_EMPTY_OR(IS_IN_SET(('Solid','Liquid'))),
db.container.cstate.widget = SQLFORM.widgets.options.widget #make drop-down list 
db.container.unna.requires = IS_EMPTY_OR(IS_IN_DB(db,'unna.id','%(unna)s')), #allow container ID to be empty 
db.container.unna.widget = SQLFORM.widgets.options.widget #make drop-down list    

db.define_table('item',
                Field('name','reference chemindex',required=True),
                Field('condition_','reference condition_'),#,widget=SQLFORM.widgets.options.widget,requires=[IS_IN_DB(db, db.condition_.name)]),
                Field('state','string'),
                Field('amount','decimal(65,2)'),
                Field('units', 'reference units'),
                Field('capacity','integer'),
                Field('quantity','integer'),
                Field('receptacle', 'reference receptacle'),
                Field('pounds',compute=lambda r: db.conversions(r['Iunits']).unitsfrom),
                Field('hazwastecodes','string',readable=False),
                Field('components','text'),
                Field('mixture','text'),
                Field('comments','text'),
                Field('input_id','string'),#a reference from the feeder system, example "From Dr. Bromer's lab"
                Field('inputnumber','integer'),#a reference from the feeder system, example "12345" OR otp_waste_container_id
                Field('shelf', 'reference shelf', default=0), #allow container ID to be empty
                Field('container', 'reference container'),
                format='%(name)s'
               )
db.item.state.requires=IS_IN_SET(('Solid','Liquid','Gas'))
db.item.name.requires = IS_EMPTY_OR(IS_IN_DB(db,'chemindex.id','%(chemname)s'))
db.item.container.requires = IS_EMPTY_OR(IS_IN_DB(db,'container.id','%(id)s %(contnum)s')), #allow container ID to be empty - Put ID and container key, in case container key is blank
db.item.container.widget = SQLFORM.widgets.options.widget #make drop-down list    
db.item.units.requires = IS_EMPTY_OR(IS_IN_DB(db,'units.id','%(name)s')), #allow units to be empty
db.item.units.widget = SQLFORM.widgets.options.widget #make drop-down list
db.item.receptacle.requires = IS_EMPTY_OR(IS_IN_DB(db,'receptacle.id','%(name)s')), #allow receptacle to be empty
db.item.receptacle.widget = SQLFORM.widgets.options.widget #make drop-down list
db.item.condition_.requires = IS_EMPTY_OR(IS_IN_DB(db,'condition_.id','%(name)s')), #allow condition to be empty
db.item.condition_.widget = SQLFORM.widgets.options.widget #make drop-down list  
db.item.shelf.requires = IS_EMPTY_OR(IS_IN_DB(db,'shelf.id','%(shelfcode)s %(disposalcode)s')), #allow condition to be empty
db.item.shelf.widget = SQLFORM.widgets.options.widget #make drop-down list         

#for printing manifest to PDF 
#Each record is a form layout
db.define_table('manifest_layout',
                #Number elements rom 1000 to make room from change.
                # Elements on first page start with 1000 + box number. Example: #1 Generator number = element 1001
                #Elements on page 2 start with 2000
                Field('type','string'),
                Field('name','string'),
                Field('element','integer'),
                Field('x1','double'), # x and y are botton left corner
                Field('y1','double'),
                Field('x2','double'), # x and y are botton left corner
                Field('y2','double'),
                Field('font','string'),
                Field('size','double'),
                Field('bold','integer'),
                Field('italic','integer'),
                Field('underline','integer'),
                Field('foreground','integer'),
                Field('background','integer'),
                Field('align','string'),
                Field('priority','integer'),
                Field('multiline','integer'),
                )

#FLAMMABLE LIQUIDS, N.O.S.
db.define_table('site',
                Field('sitename','string'),
                #EPA Identification Number
                Field('epaid','string'),
                format='%(sitename)s'
               )


## Fill empty tables
#if db(db.person).isempty():
    #db.chemindex.cname="Acetone"
#for row in db(db.chemindex.id > 0).select():
#    if (row.id % 2 == 0):
#        row.update_record(treatment=1)
#    else:
#        row.update_record(treatment=2)
