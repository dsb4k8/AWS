# AWS Response Parsing Methods
## Definitions
- Amazon Web Services (AWS) is a subsidiary of Amazon.com that provides on-demand cloud computing platforms to individuals, companies and governments, on a paid subscription basis.
- AMI: An Amazon Machine Image (AMI) provides the information required to launch an instance.
- EC2 instance: An EC2 instance is a virtual server in Amazon's Elastic Compute Cloud (EC2) for running applications on the Amazon Web Services (AWS) infrastructure. AWS is a comprehensive, evolving cloud computing platform; EC2 is a service that allows business subscribers to run application programs in the computing environment.
- ECR: Amazon ECR is a managed AWS Docker registry service. Customers can use the familiar Docker CLI to push, pull, and manage images. Amazon ECR provides a secure, scalable, and reliable registry.
- ENI: An elastic network interface (referred to as a network interface in this documentation) is a virtual network interface that can include the following attributes:
    -- a primary private IPv4 address
    -- one or more secondary private IPv4 addresses
    -- one Elastic IP address per private IPv4 address
    -- one public IPv4 address, which can be auto-assigned to the network interface for eth0 when you launch an instance
    -- one or more IPv6 addresses
    -- one or more security groups
    -- a MAC address
    -- a source/destination check flag
    -- a description
- S3: Amazon S3 is a cloud computing web service offered by Amazon Web Services. Amazon S3 provides object storage through web services interfaces.
- SG: A security group is a set of IP filter rules that define how to handle incoming (ingress) and outgoing (egress) traffic to both the public and private interfaces of a virtual server instance.
- Snapshot: Snapshots are incremental backups, which means that only the blocks on the device that have changed after your most recent snapshot are saved. This minimizes the time required to create the snapshot and saves on storage costs by not duplicating data.
- Volumes: An Amazon EBS volume is a durable, block-level storage device that you can attach to a single EC2 instance. After a volume is attached to an instance, you can use it like any other physical hard drive.
## Motivaton
Since cloud computing serices are becoming more affordable compared to hosting services locally, it is beneficial to enterprises to build and integrate solutions on top of this existing the exising infastructure. 
###### AWS Pros:
- Services offer on demand pricing which can curb overspending of services
- Services are turn-key; majority of impleentation will be at configuration level
- Many modules and libraries have already been created to retreive information 
###### AWS Cons:
- At scale, poor accounting of resources can potentially cost the enduser thousands without contributing to business and development objectives
## Outcome
A practical implementation of AWS parsing methods using the Boto3 module.
