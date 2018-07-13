import boto3
from pprint import pprint


# pprint(response)



class Eni:
	def untagged(self, response):
		l = []
		for obj in response:
			hastags = obj.get("TagSet")
			print "hastag"
			if not hastags:
				l.append(obj.get("NetworkInterfaceId"))
			else:
				for item in hastags:
					if not item.get("Keys").lower() == "team" or item.get("Keys").lower() == "product":
						l.append(obj.get("NetworkInterfaceId"))
					else:
						pass
		return l
	def unused(self, response):
		l = []
		for obj in response:
			if obj.get("Status"):
				if obj.get("Status") == "available" or obj.get("Status") == 'detaching':
					l.append(obj.get("NetworkInterfaceId"))
				else: 
					pass
			else:
				pass
		return l
	# Teams are not provided in response
	def byteam(self, response):
		result = {}
		for obj in response:
			filledtagset = obj.get("TagSet")
			if filledtagset:
				for item in filledtagset:
					if item.get("Key").lower() == "team":
						team = item.get("Value")
						if team not in result.keys():
							result[team] = []
							result[team].append(obj.get("NetworkInterfaceId"))
						else:
							result[team].append(obj.get("NetworkInterfaceId"))
					else:
						pass
			else:
				pass
		return result

	def byproduct(self, response):
		result = {}
		for obj in response:
			filledtagset = obj.get("TagSet")
			if filledtagset:
				for item in filledtagset:
					if item.get("Key").lower() == "product":
						team = item.get("Value")
						if team not in result.keys():
							result[team] = []
							result[team].append(obj.get("NetworkInterfaceId"))
						else:
							result[team].append(obj.get("NetworkInterfaceId"))
					else:
						pass
			else:
				pass
		return result
	




if __name__=="__main__":
	client = boto3.client('ec2')
	response = client.describe_network_interfaces().get("NetworkInterfaces")
	x = Eni()
	# pprint(response)
	# print x.untagged(response)
	print x.byteam(response)
	print"++++++++++++++++++++"
	print x.byproduct(response)






	# print x.unused(response)
	# pprint(response)


