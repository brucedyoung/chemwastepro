# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from manifest.py")


def generate():
    #We want to have a preview mode, where the values are overlaid on the Uniform Hazardous Waste Management PDF form supplied by the EPA
    #Sample is here: https://www.epa.gov/hwgenerators/hazardous-waste-manifest-system
    #One option is to use PyPDF2, add the blank PDF form as a watermark, and combine the PDF generated by pyfpdf. But that requires loading the PyPDF2 library
    #What we are doing is converting the EPA PDF into a PNG offline.
    #Then we can just use the PNG as a background with pyfpdf included with web2py.

    from gluon.contrib.pyfpdf import Template
    import os.path
    printpreview = 1
    elements = [ ]
    #Add all elements and positioning to form from the database
    #See  http://pyfpdf.readthedocs.io/en/latest/Templates/
         #letter paper =  215.9 mm x 279.4 m
    for row in db(db.manifest_layout.element<2000).select():
        elements.append({ 'name': row.name, 'type': row.type, 'x1': row.x1, 'y1': row.y1, 'x2':  row.x2, 'y2': row.y2, 'font': row.font, 'size': row.size, 'bold': row.bold, 'italic': row.italic, 'underline': row.underline, 'foreground': row.foreground, 'background': row.background, 'align': row.align, 'text': '', 'priority': row.priority, 'multiline' : row.multiline},)


        
        
        
    elements.append({ 'name': 'Page_1_of', 'type': 'T', 'x1': 105.0, 'y1': 40.5, 'x2': 12.0, 'y2': 12.0, 'font': 'Arial', 'size': 0.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2 })
        
#    elements.append({ 'name': 'Emergency_Response_Phone', 'type': 'T', 'x1': 115.0, 'y1': 40.5, 'x2': 12.0, 'y2': 12.0, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, })
#TESTING TESTING TESTING TESTING TESTING TESTING TESTING TESTING 
    #elements.append({ 'name': 'Emergency_Response_Phone', 'type': 'T', 'x1': 25, 'y1': 172.00, 'x2': 25.0, 'y2': 30.0, 'font': 'Arial', 'size': 12.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, })
    

    
    #elements.append( { 'name': 'Generator_Name_Address', 'type': 'T', 'x1': 20.0, 'y1': 40, 'x2': 100.0, 'y2': 37.0, 'font': 'Arial', 'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, 'multiline' : 3 },)
#    elements.append( { 'name': 'Generator_Site_Address', 'type': 'T', 'x1': 115.0, 'y1': 40, 'x2': 180.0, 'y2': 37.0, 'font': 'Arial', 'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, 'multiline' : 3 },)
#    elements.append( { 'name': 'Generator_Name_Phone', 'type': 'T', 'x1': 35.0, 'y1': 49, 'x2': 180.0, 'y2': 37.0, 'font': 'Arial', 'size': 10.0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '', 'priority': 2, 'multiline' : 3 },)
    #SAMPLE LINE
#    elements.append( { 'name': 'line1', 'type': 'L', 'x1': 100.0, 'y1': 25.0, 'x2': 100.0, 'y2': 57.0, 'font': 'Arial', 'size': 0, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': None, 'priority': 3, },)
    #SAMPLE BARCODE
#    elements.append({ 'name': 'barcode', 'type': 'BC', 'x1': 20.0, 'y1': 246.5, 'x2': 140.0, 'y2': 254.0, 'font': 'Interleaved 2of5 NT', 'size': 0.75, 'bold': 0, 'italic': 0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': '200000000001000159053338016581200810081', 'priority': 3, },)

    if (printpreview==1):
        elements.append({ 'name': 'background', 'type': 'I', 'x1': 3.3, 'y1': 3.3, 'x2': 212.6, 'y2': 276.1, 'font': None, 'size': 0.0, 'bold': 0, 'italic':    0, 'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', 'text': 'logo', 'priority': 0, },)
    # self.image("logo.png", x=10, y=8, w=23)
    f = Template(format="A4",
             elements = elements,
             title="Sample Manifest", author="ChemWastePro",
             subject="Sample Manifest", keywords="Sample Manifest Number")
    f.add_page()

    #logo=os.path.join(request.env.web2py_path,"static","images","manifest.png")
     #self.image(logo,10,8,33)

    #f["company_logo"] = os.path.join(request.env.web2py_path, "gluon", "contrib", "pyfpdf", "tutorial", "logo.png"
    #os.path.join(request.env.web2py_path,request.folder,"static","images","g3001.png")

    #if print preview, then add background
    if (printpreview==1):
        f["background"] = os.path.join(request.env.web2py_path,request.folder,"static","images","manifest.png")
    f["Generator_ID_Number"] = "123456789"
    f["Page_1_of"] = "2"
    f["Emergency_Response_Phone"] = "510-642-6908"
    f["Manifest_Tracking_Number"] = "NYB54321"
    f["Generator_Name_Address"] = "Somewhere, CA, USA\n123 Anywhere Rd.\nMain CampusAddress"
    f["Generator_Name_Phone"] = "510-642-6073"
    f["Generator_Site_Address"] = "Somewhere, CA, USA\n123 Anywhere Rd.\nMain Site"
    f["Transporter_1_Company_Name"] = "Transporter1"
    f["Transporter_2_Company_Name"] = "Transporter2"
    f["Transporter_1_Company_EPAID"] = "TransEPAID1"
    f["Transporter_2_Company_EPAID"] = "TransEPAID2"
    f["DesignatedFacilityName_Address"] = "Somewhere, CA, USA\n123 Anywhere Rd.\nMain Campus"
    f["DesignatedFacilityEPAID"] = "NYPD411512412"
    f["DesignatedFacilityPhone"] = "510-642-6073"
    f["9a1_HM"] = "X"
    f["9a2_HM"] = "X"
    f["9a3_HM"] = "X"
    f["9a4_HM"] = "X"
    f["Special_Handing_Instructions"] = "Special Handling Instructions"
    f["Generator_Site_Address"] = "Somewhere, CA, USA\n123 Anywhere Rd.\nMain Campus Site"
    f["9b1_HM"] = XML("UN2811 Waste Toxic solids, organic, n.o.s.,\n\(Phenol/Chloroform\),\n6.1,PG III")
    f["9b2_HM"] = XML("UN1992, 3, PGIII\nWaste Flammable Liquid\nAcetone n.o.s")
    f["9b3_HM"] = "UN1992, 3, PGIII\nWaste Flammable Liquid\nAcetone n.o.s"
    f["9b4_HM"] = "UN1992, 3, PGIII\nWaste Flammable Liquid\nAcetone n.o.s"
    f["10_1ContainersNo"] = "145"
    f["10_2ContainersNo"] = "165"
    f["10_3ContainersNo"] = "16"
    f["10_4ContainersNo"] = "40"
    f["10_1ContainersType"] = "DF"
    f["10_2ContainersType"] = "DM"
    f["10_3ContainersType"] = "CF"
    f["10_4ContainersType"] = "TT"
    response.headers['Content-Type']='application/pdf'
    return f.render('invoice.pdf', dest='S')
