# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# try something like
def index(): return dict(message="hello from ajax.py")


@service.soap('WSAdditem',returns={'result':int},args={'FourD_arg1':str,'otp_container_id':int,'otp_person_uid':str,'otp_person_first':str,'otp_person_last':str,'otp_department':str,'otp_container_condition_id':int,'otp_phys_state_id':int,'otp_container_condition_id':int,'otp_bottle_type':str,'otp_container_size_unit':str,'otp_container_size':str,'otp_container_size_unit':str,'otp_container_size':float,'otp_accumulation_start_date':str,'otp_pickup_date':str,'otp_primary_component':int,'otp_components':str,'otp_primary_component':int,'srs_chartstring':str,'srs_project_id':int,'otp_primary_component':int,'building':str,'room':str,'HWPComments':str,'HWPepa_hw_no':str})

def WSAdditem(a,b):
    return (a+b)
