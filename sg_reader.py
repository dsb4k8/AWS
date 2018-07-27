# -*- coding: utf-8 -*-
import json
import boto3
from chainmap import ChainMap as cm
from datetime import *
from pprint import pprint
##For 2.7: $`pip install ChainMap` before importing


def get_untagged_sgs(data):
##  PRE:  Requires a dictionary
##  POST: Returns smaller dictionary of untagged instances 
    untagged1 = []
    untagged2 = []

    for obj in data.keys():
        # describe-instances
        if obj == "Reservations":
            for item in data.get("Reservations"):
                Instances = item.get("Instances")
                for sub in Instances:
                    nw = sub.get("NetworkInterfaces")#[1].get("GroupId")
                    for d in nw:
                        sg = d.get("Groups")[0].get("GroupId")
                        tags = sub.get("Tags")
                        
                        if not tags:
                            if sg not in untagged1:
                                untagged1.append(sg)
                            else: 
                                pass
                        else:
                            for tag in tags:
                                if tag.get("Key") == "Product" or tag.get("Key") == "Team":
                                    pass
                                else:
                                    if sg not in untagged1:
                                        untagged1.append(sg)
                                    else:
                                        pass
        # describe_security_groups
        if obj == "SecurityGroups":
            for item in data.get("SecurityGroups"):
                tags = item.get("Tags")
                sg = item.get("GroupId")
                if not tags:
                    untagged2.append(sg)
                else:
                    if tag.get("Key") == "Product" or tag.get("Key") == "Team":
                        pass
                    else:
                        untagged2.append(sg)

    untagged = untagged1 + untagged2
    return untagged

def get_used_sgs(data):
##    PRE:  Requires a dictionary of data 
##    POST: Returns a list of unique security groups present in the provided dataset

    dsg = []
##  from ec2 describe-security-groups
    for item in data.get("SecurityGroups"):
        for sub_item in item.get("IpPermissions"):
            user = sub_item.get("UserIdGroupPairs")
            if user:
                for i in user:
                    is_used = i.get("GroupId")
                    if is_used:
                        if is_used not in dsg:
                            dsg.append(is_used)
                            
                        else:
                            pass
                    else:
                        pass
            else:
                pass
##  from elasticache describe-cache-clusters
    for item in data.get("CacheClusters"):
        only = item.get("SecurityGroups")
        for sg in only:
            if sg.get("SecurityGroupId")not in dsg:
                dsg.append(sg.get("SecurityGroupId"))
            else:
                pass

##from ec2 describe-instances
    for item in data.get("Reservations"):
        for instance in item.get("Instances"):
            for contributor in instance.get("SecurityGroups"):
                if contributor.get("GroupId") not in dsg:
                    dsg.append(contributor.get("GroupId"))
                else:
                    pass

##  flatten out compound lists:
    l = []
    for sublist in dsg:
        l.append(sublist)
        
    return l
##    from elasticache describe-cache-clusters

def get_outside_subnet(data):
##  FROM: ec2 describe-securtiy-groups
##  PRE:  Requires dictionary of security groups
##  POST: Returns a list of security group ids that allow traffic from ports
##        other than 80 and 443
    
    sgs_outside_subnet = []
    for item in data.get("SecurityGroups"):
        for subitem in item.get("IpPermissions"):
            target = subitem.get("FromPort")
            if isinstance(target, (int, long)):
            #to handle possible 'None' instances
                if target != 80 and target != 443:
                    sgID = item.get("GroupId")
                    if sgID not in sgs_outside_subnet:
                        sgs_outside_subnet.append(sgID)
                    else:
                        pass
                else:
                    pass
            else:
                pass
    return sgs_outside_subnet

if __name__=="__main__":
# Clients
    b3c  = boto3.client('ec2')
    b3elc= boto3.client("elasticache")
    b3rds= boto3.client("rds")
# Resopnses
    response_ins = b3c.describe_instances()#.get("Reservations")
    response_sgs  = b3c.describe_security_groups()#.get("SecurityGroups")
    response_elc = b3elc.describe_cache_clusters()#.get("CacheClusters")
    response_rds = b3rds.describe_db_security_groups()#.get("DBSecurityGroups")

    data = dict(cm(response_ins, response_elc, response_sgs, response_sgs))
# Function Calls
    # pprint(get_untagged_sgs(data))
    # pprint(get_used_sgs(data))
    # pprint(get_outside_subnet(data))
    pass