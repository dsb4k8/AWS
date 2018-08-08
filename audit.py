import argparse
import boto3
from pprint import pprint
from ami_reader import *
from ec2_reader import *
from s3_reader import *
from sg_reader import *
from snapshot_reader import *
from volume_reader import *
from volumevisual import *
from cpm_pie_visual import *

# **** For Tracking Computer-Dependent Runtime ****
import time
start_time = time.time()
# **************************************************

parser = argparse.ArgumentParser(prog= "***This module was designed to increase visibility of Veriship's allocated resources in real time. SubModules: AMI, EC2, S3, SECURITY GROUPS, and VOLUMES have their respecive -h/HELP options.")
# for subparsers:
# subami
parser.add_argument('-amiunt')
parser.add_argument('-amigt')
parser.add_argument('-amigp')
# subecc
parser.add_argument('-nat')
parser.add_argument('-odcpi')
parser.add_argument('-odcpm')
parser.add_argument('-rescpi')
parser.add_argument('-rescpm')
parser.add_argument('-ec2unt')
parser.add_argument('-ec2gt')
parser.add_argument('-ec2gp')
parser.add_argument('-norm')
parser.add_argument('-tcpm')
parser.add_argument('-pcpm')
parser.add_argument('-ttlte')
parser.add_argument('-ttlpe')
parser.add_argument('-ttlode')
parser.add_argument('-ttlrese')
# subs3
parser.add_argument('-gbsize')
parser.add_argument('-s3unt')
parser.add_argument('-ipb')
parser.add_argument('-cpb')
# subsg
parser.add_argument('-sgunt')
parser.add_argument('-used')
parser.add_argument('-outsidesubnet')
# subsnp
parser.add_argument('-snpunt')
parser.add_argument('-snpgt')
parser.add_argument('-snpgp')
parser.add_argument('-snpgami')
parser.add_argument('-snpsize')
parser.add_argument('-snpcost')
# subvol
parser.add_argument('-volunt')
parser.add_argument('-unused')
parser.add_argument('-avguse')
parser.add_argument('-unusedcpm')
parser.add_argument('-cpm')

# vusual
parser.add_argument('-vunt')
parser.add_argument('-ec2cpm')


subparsers = parser.add_subparsers()

# AMIs
subami = subparsers.add_parser('ami', help = "contains all methods pertaining to Veriship's amazon machine images.")
subami.add_argument('-amiunt','-ami-untagged', action = "store_true", help = "<List> returns all AMIs which have NO team or product associated.")
subami.add_argument('-amigt','-ami-group-by-team', action = "store_true", help = "<DICT> 'group by team' returns teams and the AMI ids associated with each.")
subami.add_argument('-amigp','-ami-group-by-product', action = "store_true", help = "<DICT> 'group by product' returns products and the AMI ids associated with each.")

# EC2
subecc = subparsers.add_parser('ec2', help = "contains all methods pertaining to ec2 resources owned by Veriship. All referenced costs are in USD.")
subecc.add_argument('-nat','-network-attach-time', action = "store_true", help = "<LIST TUPLE> returns, in datetime format, INSTANCE CREATION TIME as first element, and associated INSTANCE ID as second element")
subecc.add_argument('-odcpi','-od-cost-per-instance', action = "store_true", help = "<DICT> returns INSTNACE ID as Key, and associated ON DEMAND price per HOUR as Value.")
subecc.add_argument('-odcpm','-od-cost-per-month', action = "store_true", help = "<DICT> returns INSTANCE ID as Key, and associated ON DEMAND price per MONTH as Value.")
subecc.add_argument('-rescpi','-res-cost-per-instnace', action = "store_true", help = "<DICT> returns INSTANCE ID as Key, and associated RESERVATION price per HOUR as Value.")
subecc.add_argument('-rescpm','-res-cost-per-month', action = "store_true", help = "<DICT> returns INSTANCE ID as Key, and associated RESERVATION price per MONTH as Value.")
subami.add_argument('-ec2unt','-ec2-untagged', action = "store_true", help = "<LIST> returns all AMIs which have NO team or product associated.")
subecc.add_argument('-ec2gt','-ec2-group-by-team', action = "store_true", help = "<DICT> 'group by team' returns TEAMNAME as Key, and associated INSTANCE IDS  as Value.")
subecc.add_argument('-ec2gp','-ec2-group-by-product', action = "store_true", help = "<DICT> 'group by product' returns PRODUCT NAME as Key, and associated INSTANCE IDS as Value.")
subecc.add_argument('-norm','-get-normalization-factors', action = "store_true", help = "<DICT> returns INSTANCE IDS as Key, and associated NORMALIZATION FACTOR as Value.")
																		# DETAILS 
subecc.add_argument('-tcpm','-team-cost-per-month', action = "store_true", help = "<DICT> returns TEAM NAME as Key, and associated PROJECTED monthly cost as Value.")
subecc.add_argument('-pcpm','-product-cost-per-month', action = "store_true", help = "<DICT> returns PRODUCT NAME as Key, and associated PROJECTED monthly cost as Value.")
																		# SUMMATIONS
subecc.add_argument('-ttlte','-total-team-expense', action = "store_true", help = "<FLOAT> returns total PROJECTED sum of ALL TEAM cost of the current month.")
subecc.add_argument('-ttlpe','-total-product-expense', action = "store_true", help = "<FLOAT> returns total PROJECTED sum of ALL PRODUCT cost of the current month.")
subecc.add_argument('-ttlode','-total-od-expense', action = "store_true", help = "<FLOAT> returns total PROJECTED sum of ALL INSTANCE costs of the current month ASSUMING ON DEMAND PRICING.")
subecc.add_argument('-ttlrese','-total-res-expense', action = "store_true", help = "<FLOAT> *Potential* returns total PROJECTED sum of ALL INSTANCE cost of the current month ASSUMING RESERVATION PRINCING.")

# s3
subs3 = subparsers.add_parser('s3', help = "contains all methods pertaining to Veriship's s3 buckets")
subs3.add_argument('-gbsize','-get-bucket-size', action = "store_true", help = "<DICT> returns BUCKET NAME as Key, and BUCKET SIZE in terms of GB as Value.")
subs3.add_argument('-s3unt','-get-untagged-buckets', action = "store_true", help = "<DICT> reutrns S3 BUCKET NAME not associated with team or product as Key and asociated OWNER ID as Value.")
subs3.add_argument('-ipb','-get-items-per-bucket', action = "store_true", help = "<DICT> reutrns S3 BUCKET NAME as Key and associated ITEM COUNT as Value.")
subs3.add_argument('-cpb','-get-cost-per-bucket', action = "store_true", help = "<DICT> reutrns S3 BUCKET NAME as Key and associated COST PER MONTH given bucket capacity as Value.")

# SecurityGroups
subsg = subparsers.add_parser('securitygroups', help = "contains all methods pertaining to Veriship's security groups")
subsg.add_argument('-sgunt','-get-untagged-securitygroups', action = "store_true", help = "<LIST> returns all SECURITY GROUPS which have NO team or product associated.")
subsg.add_argument('-used','-get-used-securitygroups', action = "store_true", help = "<LIST> returns all SECURITY GROUPS currently being used ")
subsg.add_argument('-outsidesubnet','-get-securitygroups-outside-subnet', action = "store_true", help = "<LIST> returns a list of SECURITY GROUP IDs that allow traffic from ports OTHER THAN 80 and 443")

#Snapshots
subsnp = subparsers.add_parser('snapshots', help = "contains all methods pertaining to Veriship's SNAP SHOTS")
subsnp.add_argument('-snpunt','-get-untagged-snapshots', action = "store_true", help = "<LIST>     returns all SNAPSHOT IDs which have NO team or product associated.")
subsnp.add_argument('-snpgt','-group-snapshots-by-team', action = "store_true", help = "<DICT>     returns TEAM NAME as Key, and associated SNAPSHOT IDs as Value.")
subsnp.add_argument('-snpgp','-group-snapshots-by-product', action = "store_true", help = "<DICT>     returns PRODUCT NAME as Key, and associated INSTANCE IDS  as Value.")
subsnp.add_argument('-snpgami','-group-snapshots-by-ami', action = "store_true", help = "<DICT LIST>     returns AMI id as Key, and LIST of associated SNAPSHOT IDS as Value.")
subsnp.add_argument('-snpsize','-list-snapshots-by-size', action = "store_true", help = "<LIST DICT> returns LIST of dictionaries ordered by Key -- reutrns VOLUME SIZE as Key, and a LIST associated SNAPSHOT IDs as Value")
subsnp.add_argument('-snpcost','-get-cost-per-snapshot', action = "store_true", help = "<DICT>     returns SNAPSHOT IDs as Key, and the associated COST as Value.")


# Volumes
subvol = subparsers.add_parser('volumes', help = "contains all methods pertaining to Veriship's security groups")
subvol.add_argument('-volunt','-get-untagged-volumes', action = "store_true", help = "<LIST> returns all VOLUMES which have NO team or product associated.")
subvol.add_argument('-unused','-get-unused-volumes', action = "store_true", help = "<LIST> returns TEAMNAME as Key, and associated INSTANCE IDS  as Value.")
subvol.add_argument('-avguse','-get-average-usage', action = "store_true", help = "<FLOAT> returns all VOLUMES where STATUS is 'AVAILIBLE' divided by TOTAL VOLUMES.")
subvol.add_argument('-unusedcpm','-get-unused-cost-per-month', action = "store_true", help = "<FLOAT> returns total summed COST PER MONTH of all VOLUMES where STATUS is 'AVAILIBLE'.")
subvol.add_argument('-cpm','-get-cost-per-month', action = "store_true", help = "<DICT> returns VOLUME TYPE as key, and associated COST PER MONTH for each as Value.")

# Visualize
visualize = subparsers.add_parser("visualize", help = "contanis all metods pertaining to visualizing current AWS service data")
visualize.add_argument ("-ec2cpm", "-ec2costpermonth",action = "store_true", help = "<EC2: Pie Chart> Depicting cost per (team | product) / month.")
visualize.add_argument ("-vunt", "-vunused",action = "store_true", help = "<Volumes: Bar Graph> Depicting Untagged and Unused expences.")

args = parser.parse_args()

# print args


# Logic
def main():
	b3r = boto3.resource("ec2")
	b3c = boto3.client("ec2")
	b3elc= boto3.client("elasticache")
	b3rds= boto3.client("rds")
	amis = amis = preprocess_str(b3r)
	response_ami = b3c.describe_images(ImageIds = amis)["Images"]
	response_ec2 = b3c.describe_instances().get("Reservations")
	response_vol = b3c.describe_volumes().get("Volumes")
	response_snp = b3c.describe_snapshots(OwnerIds=["self"]).get('Snapshots')
# 	
	# Compilation response for Security Groups below #
	response_ins = b3c.describe_instances()
	response_sgs  = b3c.describe_security_groups()
	response_elc = b3elc.describe_cache_clusters()
	response_rds = b3rds.describe_db_security_groups()
	response_sg = dict(cm(response_ins, response_elc, response_sgs, response_sgs))
	##############################################################################

	# NOTE: tested 30 cases:
	# Concluded: Nesting subcommand conditionals in while loop had better performance(Max ~4.3s) than listing if / elif statemtnes
	# in the global scope(Max ~5.7s) 

	# AMIs
	# while args:
	# 	# ami
	if args.amiunt:
		pprint(get_untagged_amis(response_ami))
		
	elif args.amigt:
		pprint(group_amis_by_team(response_ami))
		
	elif args.amigp:
		pprint(group_amis_by_product(response_ami))
		
	# ec2
	elif args.nat:
		pprint(get_network_attach_times(response_ec2))
		
	elif args.odcpi:
		pprint(get_unreserved_cpi(response_ec2))
		
	elif args.odcpm:
		pprint(get_team_cpm(response_ec2))
		
	elif args.rescpi:
		pprint(get_reserved_cpi(response_ec2))
		
	elif args.rescpm:
		pprint(get_team_cpm(response_ec2))
		
	elif args.ec2gt:
		pprint(get_instances_by_team(response_ec2))
		
	elif args.ec2gp:
		pprint(get_instances_by_product(response_ec2))
		
	elif args.norm:
		pprint(get_norm_factor(response_ec2))
		
	elif args.tcpm:
		pprint(get_team_cpm(response_ec2))
		
	elif args.pcpm:
		pprint(get_product_cpm(response_ec2))
		
	elif args.ttlte:
		pprint(get_total_team_cpm(response_ec2))
		
	elif args.ttlpe:
		pprint(get_total_product_cpm(response_ec2))
		
	elif args.ttlode:
		pprint(get_total_unreserved_cpm(response_ec2))
		
	elif args.ttlrese:
		pprint(get_total_reserved_cpm(response_ec2))
		
	# s3
	elif args.gbsize:
		pprint(get_untagged_buckets())
		
	elif args.s3unt:
		pprint(get_untagged_buckets())
		
	elif args.ipb:
		pprint(get_items_per_bucket())
		
	elif args.cpb:
		pprint(get_cost_per_bucket())
		
	# SecurityGroups
	elif args.sgunt:
		pprint(get_untagged_sgs(response_sg))
		
	elif args.used:
		pprint(get_used_sgs(response_sg))
		
	elif args.outsidesubnet:
		pprint(get_outside_subnet(response_sg))
		
	# Snapshots
	elif args.snpunt:
		pprint(get_untagged_snapshots(response_snp))
		
	elif args.snpgt:
		pprint(group_by_team(response_snp))
		
	elif args.snpgp:
		pprint(group_by_product(response_snp))
		
	elif args.snpgami:
		pprint(group_by_ami(response_snp))
		
	elif args.snpsize:
		pprint(list_snapshots_by_size(response_snp))
		
	elif args.snpcost:
		pprint(cost_per_snapshot(response_snp))
		
	# VOLUMES
	elif args.volunt:
		pprint(get_untagged_volumes(response_vol))
		
	elif args.unused:
		pprint(get_unused_volumes(response_vol))
		
	elif args.avguse:
		pprint(get_average_usage(response_vol))
		
	elif args.unusedcpm:
		pprint(get_unused_cost_per_month(response_vol))
		
	elif args.cpm:
		pprint(get_costs_per_month(response_vol))
	#visual
	elif args.vunt:
		pprint(visualcpm())
	elif args.ec2cpm:
		pprint(ec2visual())


	print("--- %s seconds ---" % (time.time() - start_time))
#Commenting here to test webhook feature. Please disregard.
if __name__=="__main__":
	main()


