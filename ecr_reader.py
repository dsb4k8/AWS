import boto3
from pprint import pprint

# pprint(response)

# print l
class Ecr:
	def __init__(self, client, reps):
		self.client = boto3.client('ecr')
		self.reps = client.describe_repositories().get("repositories")
	
	def untagged(self):
		unt = []
		l = [item.get("repositoryName") for item in self.reps]
		for rep_name in l:
			response = self.client.describe_images(repositoryName= "%s" % rep_name).get("imageDetails") 
			for detail in response:
				if detail.get("imageTags"):
					pass
				else:
					unt.append(detail.get("imageDigest"))
		return unt

	def sizes(self):
		# size in GB
		l = [item.get("repositoryName") for item in self.reps]
		result = {}
		for name in l:
			response = (self.client.describe_images(repositoryName= "%s" %name).get("imageDetails") )
			sl = []
			for item in response:
				size = item.get("imageSizeInBytes")
				sl.append(size)
			if name not in result.keys():
				result[name] = sum(sl)/(1024.0*1024.0*1024.0)
		return result
	def cost(self):
		# cost per month in USD
		d= self.sizes()
		d.update((x,y*0.1) for x, y in d.items())
		return d
		
if __name__=="__main__":
	client = boto3.client('ecr')
	reps = client.describe_repositories().get("repositories")
	e = Ecr(client, reps)
	# print "Image Digests returned"
	# pprint(e.untagged())
	# print "Sizes in GB:"
	# pprint(e.sizes())
	# print"Costs per month in USD"
	# pprint(enta.cost())




