import boto3
from datetime import timedelta
from datetime import datetime
from math import ceil
from pprint import pprint

# import subprecess


client = boto3.client('s3')
response = client.list_buckets()
pprint(response)

# def get_bucket_size():
# 	# Size returned in GB
# 	s3_r = boto3.resource('s3')
# 	bucket_list = [bucket.name for bucket in s3_r.buckets.all()]
# 	cloudwatch = boto3.client('cloudwatch')
# 	result = {}
# 	for bucket_name in bucket_list:
# 		response = cloudwatch.get_metric_statistics(
# 	    Namespace="AWS/S3",
# 	    MetricName="BucketSizeBytes",
# 	    Dimensions=[
# 	        {
# 	            "Name": "BucketName",
# 	            "Value": bucket_name
# 	        },
# 	        {
# 	            "Name": "StorageType",
# 	            "Value": "StandardStorage"
# 	        }
# 	    ],
# 	    StartTime=datetime.now() - timedelta(days=1),
# 	    EndTime=datetime.now(),
# 	    Period=86400,
# 	    Statistics=['Average']
# 		)
# 		for item in response.get("Datapoints"):
# 			result[bucket_name] = item.get("Average")/(1024.0*1024.0*1024.0)
# 	return result

# def get_untagged_buckets():
# 	session = botocore.session.get_session()

# 	result = {}
# 	s3_r = boto3.resource('s3')
# 	bucket_list = [bucket.name for bucket in s3_r.buckets.all()]
# 	s3 = session.create_client('s3')
# 	client = session.create_client('s3')

# 	for item in bucket_list:
# 		get_r = s3.list_objects(Bucket = item)

# 		try:
# 			response = client.get_bucket_tagging(Bucket = item)
# 		except Exception, e:
# 			resp = client.get_bucket_acl(Bucket = item)
# 			result[get_r.get('Name')] = resp.get("Owner").get("ID")
# 	return result

# def get_items_per_bucket():
# 	client = boto3.client('cloudwatch')
# 	resource = boto3.resource('s3')
# 	bucket_list = [bucket.name for bucket in resource.buckets.all()]
# 	result = {}
# 	for bucket in bucket_list:

# 		response = client.get_metric_statistics(
# 		    Namespace='AWS/S3',MetricName='NumberOfObjects',
# 		    StartTime=datetime.utcnow() - timedelta(days=2) ,
# 		    EndTime=datetime.utcnow(), Period=86400,
# 		    Statistics=['Average'],
# 		    Dimensions=[
# 		        {'Name': 'BucketName', 'Value': bucket},
# 		        {u'Name': 'StorageType', u'Value': 'AllStorageTypes'}
# 		    ])
# 		for dp in response.get("Datapoints"):
# 			result[bucket] = dp.get("Average")
# 	return result
# def get_cost_per_bucket():
# 	# Monthly Cost:
# 	a = get_bucket_size().keys()
# 	# cost in GB // bytes/(1024*1024*1024):
# 	temp = get_bucket_size().values()
# 	b = []
# 	result = {}

# 	for val in temp:
# 		longcost = val * 0.023
# 		# round result up to the nearest cent:
# 		b.append(ceil(longcost * 100) / 100)
# 	result = dict(zip(a,b))
# 	return result

# # if __name__=="__main__":
# 	# pprint(get_cost_per_bucket())
# 	# print"____Get_Untagged_Bucket_______"
# 	# pprint(get_untagged_buckets())
# 	# print"____Get_Size_of_Buckets_(MBs)_"
# 	# pprint(get_bucket_size())
# 	# print"____Get_Num_Items_____________"
# 	# pprint(get_items_per_bucket())
# 	# print"________END___________________"


	