#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *
from gluon import current

#cwp_functions

def shelveitem(item_id):
    # This process processes items with blank container or shelf number
    # 1. Check for  blank item
    # 2. Check shelves with closedflag = false
    #The item must have a complete disposal code,
    # five elements in disposal code, i.e, group_, state, hazard(s), tsdf, treatment

    # Find a shelf with an exactly matching disposal code
    # Find an empty shelf in a cabinet with matching cabinet code
    # Cabinet code corresponds to first hazard, i.e, OR-OX-ENSCO-INCIN disposal code = OX cabinet
    # shelves inside cabinets can have same hazard, but different states
    # OR
    #Find an empty cabinet and assign the cabinet code, then use the first open shelf
    #
    # Cabinets and shelves have to be assigned manually, not programmatically. They should correspond to physical layout reality.
    response = "shelf number"
    return(response)
def returndisposalcode(chemindex_id):
    db = current.db
    chemhazardlistc = "" 
    chemindex_row = db(db.chemindex.id == int(chemindex_id)).select().first() #should be only one
    if ( chemindex_row):#returned a row
        #find hazards
        rows = db(db.chemindex_hazard_association.chemindex_id == chemindex_row.id).select(orderby=db.chemindex_hazard_association.hazard_order)
        for row in rows:
            chemhazardlistc += row.hazard_id.hazardabbrev+","
        #remove trailing comma
        chemhazardlist = chemhazardlistc[:-1]
        group = "" if chemindex_row.group_ is None else chemindex_row.group_[:2].upper()
        state = "" if chemindex_row.state is None else chemindex_row.state[:1]
        #chemhazardlist
        tsdf = "" if chemindex_row.tsdf is None else chemindex_row.tsdf.tsdfname.upper()
        treatment = "" if chemindex_row.treatment is None else chemindex_row.treatment.treatnameabbrev.upper()
        if((group>"")or(state>"")or(chemhazardlist>"")or(tsdf<"")or(treatment>"")):
            disposalcode=group+"-"+state+"-"+chemhazardlist+"-"+tsdf+"-"+treatment
        else:
            disposalcode = ""
    return (disposalcode)
