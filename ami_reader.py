import boto3
from datetime import timedelta
from datetime import datetime
from pprint import pprint


def preprocess_str(resourcecall):
 	# gets amiId container and extracts substring.
 	# returns list of amiIds
 	im = str(list(boto3.resource("ec2").images.filter(Owners=["self"])))
 	l = list(im.split(","))
 	result = []
 	for i in l:
 		separator = "'"
 		extraction = i.split(separator, 1)[1].split(separator, 1)[0]
 		result.append(extraction)
 	return result

def get_untagged_amis(response):
	untagged = []
	for obj in response:
		# pprint(obj.get("Tags"))
		has_tags = obj.get("Tags")
		if not has_tags:
			untagged.append(obj.get('ImageId'))
		else:
			for tag in has_tags:
				# To avoid dups:
				if (not tag.get("Key") == "Team" and not tag.get("Key") == "Product") and obj.get("ImageId") not in untagged:
					untagged.append(obj.get("ImageId"))
				else:
					pass
	return untagged

def group_amis_by_team(response):
	# Returns a dict. Key = ,<str> owner ... Value = ,<list> Value
	to_avoid = get_untagged_amis(response)
	result = {}
	for header in response:
		target = header.get("ImageId")
		has_tags = header.get("Tags")
		if has_tags:
			for tag in has_tags:
				is_team = tag.get("Key")== "Team"
				t_team = tag.get("Value")
				if is_team:
					if tag.get("Value") not in result.keys():
						result[t_team] = []
						result[t_team].append(target)
					else:
						result[t_team].append(target)
				else:
					pass
		else:
			pass
	return result

def group_amis_by_product(response):
	ids_to_avoid = get_untagged_amis(response)
	result = {}
	for header in response:
		target = header.get("ImageId")
		has_tags = header.get("Tags")
		if has_tags:
			for tag in has_tags:
				if tag.get("Key") == "Product":
					prod = tag.get("Value")
					if prod not in result.keys():
						result[prod] = []
						result[prod].append(target)
					else:
						result[prod].append(target)
				else:
					pass
		else:
			pass
	return result





# Test Funtions Here
# if __name__=="__main__":
# # 	###KEEP BOTO CALLS HERE###
	# b3r = boto3.resource("ec2")
	# b3c = boto3.client("ec2")
	# amis = amis = preprocess_str(b3r)
	# response = b3c.describe_images(ImageIds = amis)["Images"]


###Demo Call
# 	pprint(get_untagged_amis(response))









