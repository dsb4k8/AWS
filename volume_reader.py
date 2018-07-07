# -*- coding: utf-8 -*-
import boto3
from datetime import timedelta
from datetime import datetime
from pprint import pprint
import json


def get_untagged_volumes(response):
##    Data Type: List
##    Returns all volumes objects where "Tags" item
##    is omitted.
    
    untagged_volumes = []
    for item in response:
        tags = item.get("Tags")
        if tags:
            for tag in tags:
                if not tag.get("Product") == "Team" and not tag.get("Key") == "Product": 
                    if item.get("VolumeId") not in untagged_volumes:
                        untagged_volumes.append(item.get("VolumeId"))
                    else:
                        pass
                else:
                    pass
        else:
            untagged_volumes.append(item.get("VolumeId"))
    return untagged_volumes

def get_unused_volumes(response):
##    Data Type: List
##    returns of volume ids of objects labled "availible".
    
    unused_volumes = []
    for item in response:
        if item.get("State") == "available":
            unused_volumes.append(item.get("VolumeId"))
        else:
            pass
    return unused_volumes
        
def get_average_usage(response):
    #Data Type: Float
    #Returns total volumes in specified file divided by
    #occurences where state is "available".
    
        occurences = 0.0
        total = 0.0
        for item in response:
            total+=1
            if item.get("State") == "available":
                occurences+=1
            else:
                pass
            
        average = occurences/total
        return average

def get_unused_cost_per_month(response):
    iops_cost = 0.065
    pricing = {
    "gp2": 0.100,
    "io1": 0.125,
    "standard": 0.050
    }
        # in a 30 day month
    m_seconds = 2592000
    # one day
    d_seconds = 86400  
    gp2_price = []
    io1_price = []
    standard_price = []
    price_per_month_dictionary = {}
    for item in response:
        if item.get("State") == "available":
            size_in_GBs = item.get("Size")
            VolumeType = item.get("VolumeType")
            if VolumeType == "gp2" :
                gp2_price.append((pricing["gp2"] * size_in_GBs * m_seconds) / (d_seconds *30))
            
            elif VolumeType == "io1":
                io1_price.append(((pricing["io1"] * size_in_GBs * m_seconds) / (d_seconds *30)) + (((item.get("Iops") * iops_cost) * m_seconds)/ m_seconds))

            elif VolumeType == "standard":
                standard_price.append((pricing["standard"] * size_in_GBs * m_seconds) / (d_seconds *30))
            
            keys = ["gp2", "io1", "standard"]
            values = [round(sum(gp2_price),2), round(sum(io1_price),2), round(sum(standard_price),2)]
            
            price_per_month_dictionary = dict(zip(keys, values))
        else:
            pass
    return price_per_month_dictionary

def get_costs_per_month(response):
##    To be multiplied by total instances of io1 and added to io1 cost/mo
##    Update pricing dictionary if pricing changes
    
    iops_cost = 0.065
    pricing = {                                                     
        "gp2": 0.100,
        "io1": 0.125,
        "standard": 0.050
        }
    # in a 30 day month
    m_seconds = 2592000
    # one day
    d_seconds = 86400             
    
    gp2_price = []
    io1_price = []
    standard_price = []
    price_per_month_dictionary = {}
    for item in response:
        size_in_GBs = item.get("Size")
        VolumeType = item.get("VolumeType")
        if not item.get("State") == "available":
            if VolumeType == "gp2" :
                gp2_price.append((pricing["gp2"] * size_in_GBs * m_seconds) / (d_seconds *30))
                
            elif VolumeType == "io1":
                io1_price.append(((pricing["io1"] * size_in_GBs * m_seconds) / (d_seconds *30)) + (((item.get("Iops") * iops_cost) * m_seconds)/ m_seconds))
                
            elif VolumeType == "standard":
                standard_price.append((pricing["standard"] * size_in_GBs * m_seconds) / (d_seconds *30))
                
            keys = ["gp2", "io1", "standard"]
            values = [round(sum(gp2_price),2), round(sum(io1_price),2), round(sum(standard_price),2)]
            
            price_per_month_dictionary = dict(zip(keys, values))
        else:
            pass
    return price_per_month_dictionary
#############
def get_cost_per_hour(response):
##    To be multiplied by total instances of io1 and added to io1 cost/mo
##    Update pricing dictionary if pricing changes
    
    iops_cost = 0.065
    pricing = {                                                     
        "gp2": 0.100,
        "io1": 0.125,
        "standard": 0.050
        }
    # in a 30 day month
    m_seconds = 2592000
    # one day
    d_seconds = 86400             
    
    gp2_instances = []
    io1_instances = []
    standard_instances = []

    gcreated = []
    icreated = []
    screated = []

    cost_per_hour = {}
    for item in response:
        vol_id = item.get("VolumeId")
        size_in_GBs = item.get("Size")
        VolumeType = item.get("VolumeType")
        if not item.get("State") == "available":
            if VolumeType == "gp2" :
                gp2_instances.append(vol_id)
                gcreated.append(item.get("CreateTime").year)
                
            elif VolumeType == "io1":
                io1_instances.append(vol_id)
                icreated.append(item.get("CreateTime").year)

            elif VolumeType == "standard":
                standard_instances.append(vol_id)
                screated.append(item.get("CreateTime").year)
                
            p_keys = [pricing.get("gp2"), pricing.get("io1"), pricing.get("standard")]

            values = [list(zip(gp2_instances, gcreated)), list(zip(io1_instances,icreated)), list(zip(standard_instances,screated))]
            
            cost_per_hour = dict(zip(p_keys, values))
        else:
            pass
    return cost_per_hour
##############
if __name__=="__main__":

    b3c = boto3.client('ec2')
    response = b3c.describe_volumes().get("Volumes")

    #pprint(get_costs_per_month(response))
    #pprint(get_untagged_volumes(response))
    #pprint(get_unused_volumes(response))
    #pprint(get_average_usage(response))
    # pprint(get_unused_cost_per_month(response))
    # pprint(get_costs_per_month(response))
    # pprint(get_cost_per_hour(response))


