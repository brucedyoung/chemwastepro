#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gluon import *

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
