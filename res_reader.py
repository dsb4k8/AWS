import boto3
from pprint import pprint
from ec2_reader import *

# ec2 = boto3.resource('ec2')
# client = boto3.client('ec2')


# instances = ec2.instances.filter()
# ec2response = client.describe_instances().get("Reservations")
# resbuckets = client.describe_reserved_instances().get("ReservedInstances")
# # # list of len 45
# instances = ec2.instances.filter()

# # pprint(resbuckets)
# # print "===================="
# # print get_norm_factor(ec2response)
# # print "===================="
# # for i in instances:
# # 	print i.id

# factor_keys = ["32xlarge" , "24xlarge", "18xlarge","16xlarge",
#                "12xlarge", "10xlarge", "9xlarge", "8xlarge",
#                "4xlarge",  "2xlarge",  "xlarge",  "large",
#                "medium",   "small",    "micro",   "nano"]

# factor_values = [256.00 ,192.00, 144.00, 128.00, 96.00, 80.00, 72.00, 64.00, 32.00, 16.00, 8.00, 4.00, 2.00, 1.00 , 0.05, 0.25]
# factors = dict(zip(factor_keys, factor_values))

# pprint(factors)
class ReservationBucket:
	def __init__(self, singlebucket): #one dict out of list of dicts from resbuckets
		self.ftarget = singlebucket.get("InstanceType").split(".")[1]
		self.factor = factors.get(self.ftarget)
		self.count = singlebucket.get("InstanceCount")
		self.capacity = self.factor * self.count
		self.name = singlebucket.get("ReservedInstancesId")
		self.inst_family = singlebucket.get("InstanceType")
		if self.is_full():
			print "FULL!"
	def can_except(self,mass):
		return mass <= self.capacity
	def is_full(self):
		return self.capacity <= 0




class ReservationObject:
	def __init__(self, instance):
		self.name = instance
		mapping = get_norm_factor(ec2response)
		self.mass = mapping.get(instance)
		self.inst_family = instance.get("InstanceType")
	def deposit(self, to):
		to.capacity -= self.mass


if __name__=="__main__":
	"""Algorithm:
	1)make an array of reservation bucket objects:
	2)iterate through reservation objects while filling up the bucket
	3)when each bucket is filled: move to next bucket in array"""


	ec2 = boto3.resource('ec2')
	client = boto3.client('ec2')


	instances = ec2.instances.filter()
	ec2response = client.describe_instances().get("Reservations")
	# pprint(ec2response)
	resbuckets = client.describe_reserved_instances().get("ReservedInstances")
	# # list of len 45
	instances = ec2.instances.filter()
	# pprint(resbuckets)

	factor_keys = ["32xlarge" , "24xlarge", "18xlarge","16xlarge",
	               "12xlarge", "10xlarge", "9xlarge", "8xlarge",
	               "4xlarge",  "2xlarge",  "xlarge",  "large",
	               "medium",   "small",    "micro",   "nano"]

	factor_values = [256.00 ,192.00, 144.00, 128.00, 96.00, 80.00, 72.00, 64.00, 32.00, 16.00, 8.00, 4.00, 2.00, 1.00 , 0.50, 0.25]
	factors = dict(zip(factor_keys, factor_values))



	allinstances = get_norm_factor(ec2response).keys()
	i = 0
	skipped= []
	# print type(allinstances)

	while i <= len(resbuckets)-1:
		bucket = ReservationBucket(resbuckets[i])
		print "++++++++++++++++  %s   +++++++++++++++++++++" %bucket.name
		for instance in instances:
			proto = instance
			ins = ReservationObject(instance)
			if bucket.inst_family == ins.inst_family:
				print "Yes"
				continue
			else:
				print "No"
		break




			# ins = ReservationObject(inst)
			# print ins.mass
			






		
		

	# while i <= len(resbuckets)-1:

	# 	bucket = ReservationBucket(resbuckets[i])
	# 	print
	# 	print
	# 	print len(deposited)
	# 	print (len(instances_skipped),[x.name for x in instances_skipped])
	# 	print "_________________%s" %bucket.name.upper()
	# 	# print bucket.name #when bucket is changed
	# 	for instanceobject in allinstances:
			
	# 		instanceparam = str(instanceobject)			

	# 		instance = ReservationObject(instanceobject)

	# 		print "instance mass: {}, bucket capacity: {}, instnace name: {}, bucket name: {}".format(instance.mass, bucket.capacity, instance.name, bucket.name)

	# 		while bucket.can_except(instance.mass) and bucket.capacity != 0:
	# 			instance.deposit(bucket)
	# 			print "Deposited %s size %d. Bucket Remaining %d" %(instance.name, instance.mass, bucket.capacity)
	# 			deposited.append(instance)
	# 			print "instance removed"
	# 			break
	# 		if bucket.is_full():
	# 			print "FULL! NEXT BUCKET"
	# 			break

	# 		elif (bucket.capacity > 0) and (len(instances_skipped) > 0):
	# 			for skipped in instances_skipped:
	# 				if skipped.mass == bucket.capacity:
	# 					print "ooooooooo"
	# 					print"INSTANCE FROM LIST DEPOSITED %s" %skipped.name
	# 					skipped.deposit(bucket)
	# 					print "deposited"
	# 					instances_skipped.remove(skipped)
	# 				else:
	# 					print "did not deposit"
	# 					continue

	# 		else:
	# 			print "%s too large. Skip" %instance.name
	# 			if instance not in instances_skipped:
	# 				instances_skipped.append(instance)
	# 				print"instances_skipped added %s" %instance.name
	# 			else:
	# 				pass
	# 		# continue
	# 	i+=1 




