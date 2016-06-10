# chemwastepro
Chemical Waste Management Program

 DO NOT USE. IT IS NOT IN A DEPLOYABLE STATE. I'm working on it every day.
  
 A preview of the functionality: https://brucedyoung.pythonanywhere.com/chemwastepro
  
 Sample Manifest Printing: https://brucedyoung.pythonanywhere.com/chemwastepro/manifest/generate
 Includes dynamic placement of elements
 
 Database Entity Diagram: https://brucedyoung.pythonanywhere.com/chemwastepro/static/dbgraph.pdf
 
 Sample JSON query against chemical index: https://brucedyoung.pythonanywhere.com/chemwastepro/default/getchemindex.json?q=ace
 
 Web Services: https://brucedyoung.pythonanywhere.com/chemwastepro/default/call/soap?WSDL
 
 Dymo Labelwriter printing working. Five lines fit on address label.
 http://developers.dymo.com/2010/06/02/dymo-label-framework-javascript-library-samples-print-a-label/
 
 TO DO, print multiple labels
 http://developers.dymo.com/2010/06/17/dymo-label-framework-javascript-library-print-multiple-labels/
 
 
BROWSER SECURITY
 
Content Security Policy is ON. 
See /chemwastepro/models/db.py
Content-Security-Policy:frame-ancestors 'self'

The X-Frame-Options response header is set to SAMEORIGIN
See /chemwastepro/models/db.py
X-Frame-Options:SAMEORIGIN

Secure and HTTPS only cookies are enabled under HTTPS
See /chemwastepro/models/db.py
session._secure=True