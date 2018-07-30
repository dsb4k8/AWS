import boto3
from math import ceil
from datetime import datetime
import json
from pprint import pprint
import re


def get_untagged_snapshots(response):
	tagless = []
	for item in response:
		if not item.get("Tags"):
			tagless.append(item.get("SnapshotId"))
		else:
			tags = item.get("Tags")
			for tag in tags:
				if not tag.get("Key") == "Team" and not tag.get("Key") == "Product":
					tagless.append(item.get("SnapshotId"))
				else:
					pass
	return tagless

def group_by_team(response):
	result = {}
	for item in response:
		ID = item.get("SnapshotId")
		has_tags = item.get("Tags")
		# Team details are nested in tags dict:
		if not has_tags:
			pass
		else:
			for obj in has_tags:
				team = obj.get("Key") == "Team"
				t_team = obj.get("Value")
				if team:
					if t_team not in result.keys():
						result[t_team] = []
						result[t_team].append(ID)
					else:
						result[t_team].append(ID)
				else:
					pass
	return result

def group_by_product(response):
 	result = {}
	for item in response:
		ID = item.get("SnapshotId")
		has_tags = item.get("Tags")
		if not has_tags:
			pass
		else:
			for obj in has_tags:
				has_prod_tag = obj.get("Key") == "Product"
				prod = obj.get("Value")
				if has_prod_tag:
					if prod not in result.keys():
						result[prod] = []
						result[prod].append(ID)
					else:
						result[prod].append(ID)
				else:
					pass
	return result

def group_by_ami(response):
	result = {}
	for item in response:
		snId = item.get("SnapshotId")
		desc = item.get("Description")
		# To isolate amiId from descriptions where amiId is present:
		has_aId = [word for word in desc.split() if word.startswith("ami-")]
		if has_aId:
			extractedAmi = has_aId[0]

			if extractedAmi not in result.keys():
				result[extractedAmi] = []
				result[extractedAmi].append(snId)
			else:
				result[extractedAmi].append(snId)
		else:
			pass
	return result

def list_snapshots_by_size(response):
	# Returns an orderd list of disctionaries-->(int : listofsnapIds) ordered by key(int size)
	base = {}
	grp = {}
	sorted_base = []
	for item in response:
		snId = item.get("SnapshotId")
		size = item.get("VolumeSize")
		if snId not in base:
			base[snId] = []
			base[snId] = size
	for key, value in sorted(base.iteritems(), key=lambda (k,v): (v,k)):
		if value not in grp:
			grp[value] = []
			grp[value].append(key)
		else:
			grp[value].append(key)
	sorted_base.append(grp)
	return sorted_base

def cost_per_snapshot(response):
	# PER MONTH
	result = {}
	for item in response:
		snId = item.get("SnapshotId")
		size = float(item.get("VolumeSize"))
		cost = size * 0.05
		result[snId] = round(cost, 3)
	return result

def rollup(response):
	now = datetime.now()

	SnapshotInfoDeatils = {
		'GroupByTeam': group_by_team(),
		'GroupByProduct': group_by_product(),
		'GroupByAMI': group_by_ami(),
		'ListBySize': list_snapshots_by_size()
		}
	SnapshotCosts = {'TotalMonthlyCost': round(float(sum(cost_per_snapshot().values())),2)}
	rollup_report = {'SnapshotSummary': [SnapshotCosts, SnapshotInfoDeatils]}
	pprint(rollup_report)

# Testing method calls:
if __name__=='__main__':

	b3c = boto3.client('ec2')
	response = b3c.describe_snapshots(OwnerIds=["self"]).get('Snapshots')

	# pprint(get_untagged_snapshots(response))
# 	#pprint(group_by_team(response))
# 	#pprint(group_by_product(response))
# 	#pprint(group_by_ami(response))
# 	#pprint(list_snapshots_by_size(response))
# 	#pprint(cost_per_snapshot(response))
# 	#rollup(response)




