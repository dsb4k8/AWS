import json
import boto3
from chainmap import ChainMap as cm
import calendar
from datetime import datetime
import decimal
from pprint import pprint


def get_network_attach_times(response):
##    PRE:    Requires datetime method from datetime module 
##            Requires dictionary of active instances from aws ec2 describe instances
##    POST:   Returns a list of tuples,t, where t[0] is instance attach time and t[1] is instanceID
    from_id = []
    before = []
    after = []
    for obj in response:
        for item in obj.get("Instances"):
            instance = item.get("InstanceId")
            current_state = item.get("State")
            net = item.get("NetworkInterfaces")
            if net:
                for detail in net:
                    attachment = detail.get("Attachment")
                    from_id.append(instance)
                    before.append(attachment.get("AttachTime"))
            else:
                pass
    after = sorted(zip(before, from_id))

    return after


def get_unreserved_cpi(response):
##  PRE: Function requires a dictionary of current instances from aws ec2 describe instances
##  POST: Returns a dictionary Key = instance id, Value = Cost Per Hour
##  NOTE: First "if" conditional: only running instnaces are billalbe from AWS and therefore
##        non-running instnaces will be treated as 0 cost.
    
    pricing = {
        "t2.nano":   0.0081,   "c5.large":    0.177,  "r4.4xlarge":  1.8,
        "t2.micro":  0.0162,   "c5.xlarge":   0.354,  "r4.8xlarge":  3.6,
        "t2.small":  0.032,    "c5.2xlarge":  0.708,  "r4.16xlarge": 7.2,
        "t2.medium": 0.0644,   "c5.4xlarge":  1.416, 
        "t2.large":  0.1208,   "c5.9xlarge":  3.186, 
        "t2.xlarge": 0.2266,   "c5.18xlarge": 6.372, 
        "t2.2xlarge":0.4332,   "c5d.large":   1.88,
        "m5.large":  0.188,    "c5d.xlarge":  0.376,
        "m5.xlarge": 0.376,    "c5d.2xlarge": 0.752,
        "m5.2xlarge":0.752,    "c5d.4xlarge": 1.504, 
        "m5.4xlarge":1.504,    "c5d.9xlarge": 3.384,
        "m5.12xlarge":4.512,   "c5d.18xlarge":6.768,
        "m5.24xlarge":9.024,   "c4.large":    0.192,
        "m4.large":  0.192,    "c4.xlarge":   0.383,
        "m4.xlarge": 0.384,    "c4.2xlarge":  0.766,
        "m4.2xlarge":0.768,    "c4.4xlarge":  1.532,
                               "c4.8xlarge":  3.091,
        "m4.4xlarge":1.536,    "r4.large" :   0.225,
        "m4.10xlarge":3.84,    "r4.xlarge" :  0.45,
        "m4.16xlarge":6.144,   "r4.2xlarge":  0.9,
        }
    ## get machine type eg: t2.large, m4, etc
    cost_per_instance_hour = {}
    for obj in response:
        for item in obj.get("Instances"):
            state = item.get("State")
            instance_id = item.get("InstanceId")
            instance_type = item.get("InstanceType")
            instance_cost = pricing.get(instance_type)
            if state.get("Name")== "running":
                if instance_id not in cost_per_instance_hour:
                    cost_per_instance_hour[instance_id]= instance_cost
                else:
                    cost_per_instance_hour[instance_id].instance_cost
            else:
                pass
    return cost_per_instance_hour   


def get_reserved_cpi(response):
    stand_no_upfront  = {
        "t2.nano":    0.006, "c5.large":    0.146, "r4.4xlarge":  1.408,
        "t2.micro":   0.012, "c5.xlarge":   0.291, "r4.8xlarge":  2.816,
        "t2.small":   0.024, "c5.2xlarge":  0.582, "r4.16xlarge": 5.632,
        "t2.medium":  0.047, "c5.4xlarge":  1.164, 
        "t2.large":   0.086, "c5.9xlarge":  2.620, 
        "t2.xlarge":  0.156, "c5.18xlarge": 5.240, 
        "t2.2xlarge": 0.292, "c5d.large":   0.153,
        "m5.large":   0.153, "c5d.xlarge":  0.305,
        "m5.xlarge":  0.307, "c5d.2xlarge": 0.610,
        "m5.2xlarge": 0.613, "c5d.4xlarge": 1.220, 
        "m5.4xlarge": 1.227, "c5d.9xlarge": 2.746,
        "m5.12xlarge":3.680, "c5d.18xlarge":5.492,
        "m5.24xlarge":7.360, "c4.large":    0.155,
        "m4.large":   0.154, "c4.xlarge":   0.310,
        "m4.xlarge":  0.308, "c4.2xlarge":  0.620,
        "m4.2xlarge": 0.616, "c4.4xlarge":  1.240,
                             "c4.8xlarge":  2.664,
        "m4.4xlarge": 1.232, "r4.large" :   0.176,
        "m4.10xlarge":3.079, "r4.xlarge" :  0.352,
        "m4.16xlarge":4.926, "r4.2xlarge":  0.704
        }
    cost_per_instance_hour = {}
    for obj in response:
        for item in obj.get("Instances"):
            state = item.get("State")
            instance_id = item.get("InstanceId")
            instance_type = item.get("InstanceType")
            instance_cost = stand_no_upfront.get(instance_type)
            if state.get("Name")== "running":
                if instance_id not in cost_per_instance_hour:
                    cost_per_instance_hour[instance_id]= instance_cost
                else:
                    cost_per_instance_hour[instance_id].instance_cost
            else:
                pass
    return cost_per_instance_hour

def get_instances_by_team(response):
##  PRE:    Requires dictionary
##  POST:   Returns a searchable dictionary displaying list instanceId of all instances belonging to each team
##  FORMAT: {'Str': [list]}
##  NOTE:   access with: `instances.JSON` or `aws ec2 describe-instances`
    
    result = {}
    
    for obj in response:
        instance = obj.get("Instances")
        for section in instance:
            Id = section.get("InstanceId")
            has_tags = section.get("Tags")
            if has_tags:
                for item in has_tags:
                    has_team = item.get("Key") == "Team"
                    team_name = item.get("Value")
                    if has_team:
                        if team_name not in result.keys():
                            result[team_name] = []
                            result[team_name].append(Id)
                        else:
                            result[team_name].append(Id)
                    else:
                        pass
            else:
                pass
    return result

def get_instances_by_product(response):
##    PRE:  Requires a dictionary
##    POST: Returns a dictionary with product name as key and a list of
##          corresponding instance IDs
##    NOTE: This method can be used as a search function that returns a list
##            Example: search = get_instances_by_product(your_dictionary)
##                     search["Audit"]

    d = {}
    for item in response:
        for subitem in item.get("Instances"):
            instance = subitem.get("InstanceId")
            has_tag = subitem.get("Tags")
            if has_tag:
            #in case of tagless instance:
               for tag in has_tag:
##                   target = tag.get("Key") == "Product"
##                   if tag.get("Key") == "Product":
                   corresponding_prod = tag.get("Value")
                   if tag.get("Key") == "Product":
                       if corresponding_prod not in d:
                           d[corresponding_prod] = []
                           d[corresponding_prod].append(instance)
                       else:
                           d[corresponding_prod].append(instance)
                   else:
                        pass
            else:
                pass
    return d


def get_norm_factor(response):
##  PRE:  Requires a dictionary. Data from aws ec2 describe instances
##  POST: Returns a dictionary of factor (Computing Magnitude) assigned to each instance
##  NOTE: Created list "factor_keys" in reverse order because large factor keys share less comonality with the set than small ones.
##        ie: substring "24xlarge" is not contained in substring "18xlarge" but large is. This would be problematic if
##            searching iteratively.
    
    factor_keys = ["32xlarge" , "24xlarge", "18xlarge","16xlarge",
                   "12xlarge", "10xlarge", "9xlarge", "8xlarge",
                   "4xlarge",  "2xlarge",  "xlarge",  "large",
                   "medium",   "small",    "micro",   "nano"]

    factor_values = [256.00 ,192.00, 144.00, 128.00, 96.00, 80.00, 72.00, 64.00, 32.00, 16.00, 8.00, 4.00, 2.00, 1.00 , 0.50, 0.25]
    factors = dict(zip(factor_keys, factor_values))
    result = {}
    for obj in response:
        for item in obj.get("Instances"):
            instance_type = item.get("InstanceType")
            instance_id = item.get("InstanceId")
            for getter in factor_keys:
                if getter in instance_type:
                    result[instance_id] = factors.get(getter)
                    break
                else:
                    pass
    return result


###### Start: Compiled functions from proto-functions for export_json(d)
######__________________________________________________________________
def get_total_unreserved_cpm(response):
##  PRE:  Function takes in dictionary from aws ec2 describe-instnaces.
##  POST: Returns a dict with instanceId as key and the projected monthly cost as value.
    now = datetime.now()
    u = get_unreserved_cpi(response)
    total_unreserved_costs = []
    for total in u.values():
        total_unreserved_costs.append(total)
    total_cpm = sum(total_unreserved_costs) * (24 * calendar.monthrange(now.year, now.month)[1])
    return round(total_cpm,2)
    
def get_total_reserved_cpm(response):
##  PRE:  Function takes in dictionary from aws ec2 describe-instnaces.
##  POST: Returns a dict with instanceId as key and the projected monthly cost as value.
    now = datetime.now()
    r = get_reserved_cpi(response)
    total_reserved_costs = []
    for total in r.values():
        total_reserved_costs.append(total)
    return sum(total_reserved_costs) * (24 * calendar.monthrange(now.year, now.month)[1])


def get_team_cpm(response):
##  PRE:  Function takes in dictionary from aws ec2 describe-instnaces.
##  POST: Returns a dict with team names as key and the projected monthly cost as value.
##  NOTE: (1)Team BI's cost per monthly is $0 because all associated are status "Terminated",
##        and therefore are not billible from AWS.
##        For logic: Please check `get_unreserved_cpi` NOTE section.
##        (2)`sum(instnace_price_list)` only returns each team's cost per hour thus,
##            additional operations gets the projected total cost for number of days
##            in the CURRENT month ie:(28 <= days <= 31).
    
    result = {}
    now = datetime.now()
    t_i = get_instances_by_team(response)
    i_c = get_unreserved_cpi(response)
    now = datetime.now()
    for t in t_i:
        instance_list = t_i.get(t)
        instance_price_list = []
        for instance in instance_list:
            if instance in i_c:
            #not always true
                instance_price_list.append(i_c.get(instance))
            else:
                pass
        team_cpm = sum(instance_price_list) * (24 * calendar.monthrange(now.year, now.month)[1])
        #Trim 
        result[t] = round(team_cpm,2)
    return result

def get_total_team_cpm(response):
##  PRE:  Function takes in dictionary from aws ec2 describe-instnaces.
##  POST: Returns a dict with team tags as key and the projected monthly cost as value.
    c = get_team_cpm(response)
    total_team_costs = []
    for total in c.values():
        total_team_costs.append(total)
    return sum(total_team_costs)

def get_product_cpm(response):
##  PRE:  Function takes in dictionary from aws ec2 describe-instnaces.
##  POST: Returns a dict with product tags as key and the projected hourly cost as value.
    result = {}
    now = datetime.now()
    p_i = get_instances_by_product(response)
    i_c = get_unreserved_cpi(response)
    for p in p_i:
        instance_list = p_i.get(p)
        instance_prices = []
        for instance in instance_list:
            if instance in i_c:
                instance_prices.append(i_c.get(instance))
            else:
                pass
        product_cpm = sum(instance_prices) * (24 * calendar.monthrange(now.year, now.month)[1])
        result[p] = round(product_cpm,2)
    return result
def get_total_product_cpm(response):
##  PRE:  Function takes in dictionary from aws ec2 describe-instnaces.
##  POST: Returns a dict with product tags as key and the projected monthly cost as value.
    c = get_product_cpm(response)
    total_product_costs = []
    for total in c.values():
        total_product_costs.append(total)
        result = sum(total_product_costs)
    return round(result,2)

######End compilation files.
######__________________________________________________________________


def export_json(response):
##  PRE:  Calls other funtions. Params = False
##  POST: returns a JSON file with:
##           Factor, InstanceCost Per Hour, Total Monthly Cost,
##           Total Cost Per Team, Reservation Cost By Product

##compartment #1 Totals
    TotalCostPerProduct   = get_total_product_cpm(response)
    TotalTeamCost         = get_total_team_cpm(response)
    TotalODCost           = get_total_unreserved_cpm(response)
    TotalResCost          = get_total_reserved_cpm(response)   
##compartment #2 Details
    ComputingFactor       = get_norm_factor(response)
    ODCostPerInstance     = get_unreserved_cpi(response)
    ResCostPerInstance    = get_reserved_cpi(response)
    CostPerTeam           = get_team_cpm(response)
    CostPerProduct        = get_product_cpm(response)
    MountTime             = get_network_attach_times(response)
##Meta-Dictionaries    
    
    json_totals_data = {
        "TotalMonthlyProductCost" : TotalCostPerProduct, #Sum of Monthly costs
        "TotalMonthlyTeamCost"    : TotalTeamCost,       #Sum of team costs per month
        "TotalOnDemandCost"       : TotalODCost,         #Sum of Unreserved cost per month
        "TotalReservedCost"       : TotalResCost         #sum of Reserved costs
        
        }
    json_perbasis_data = {
        # "ComputingFactors"  : ComputingFactor,
        # "DemandCostHourly"  : ODCostPerInstance,
        # "ReservedCostHourly": ResCostPerInstance,
        "MonthlyCostByTeam"       : CostPerTeam,
        "MonthlyCostByProduct"    : CostPerProduct #Monthly cost per month
        }
    
##NOTE: Dictionaries are unsorted and therefore presented could be in a differenct order each time this functhin
##      is ran. Therefore these dicts sored in an ordered data structure
##      such as a list.
    presentation_totals = [json_totals_data]
    presentation_details =[json_perbasis_data]
    
##Wrap into a single object
    json_outer_data = {
        "Totals" : presentation_totals,
        "Details": presentation_details
        }
##Structure inner items
    outer_list_wrapper = [json_outer_data]
    dataset_wrapper = {
        "Ec2Expenses": outer_list_wrapper
        } 
##Export to file
##NOTE: since open mode 'w', file must be closed.
    with open("Ec2Expenses.json", "w") as fp:
        json.dump(dataset_wrapper, fp, indent = 4)
        fp.close()

if __name__=="__main__":
    b3c = boto3.client('ec2')
    response = b3c.describe_instances().get("Reservations")
    ###TESTING FUCTIONS HERE###
    #pprint(get_team_cpm(response))
    # pprint(get_network_attach_times(response))
    # pprint(get_unreserved_cpi(response))
    #pprint(get_reserved_cpi(response))
    # pprint(get_instances_by_team(response))
    #pprint(get_instances_by_product(response))
    #pprint(get_norm_factor(response))
    #pprint(get_total_product_cpm(response))
    #pprint(get_norm_factor(response))
    export_json(response)

