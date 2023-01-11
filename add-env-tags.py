import boto3
from boto3 import ec2

ec2_client_paris = boto3.client('ec2', region_name = "eu-west-3")
ec2_resource_paris = boto3.resource('ec2', region_name = "eu-west-3")

ec2_client_franfurt = boto3.client('ec2', region_name = "eu-central-1")
ec2_resource_frankfurt = boto3.resource('ec2', region_name = "eu-central-1")

instance_ids_paris = []
instance_ids_frankfurt = []

reservation_paris = ec2_client_paris.describe_instance()['Reservations']

for res in reservation_paris:
    instances = res["Instances"]
    for ins in instances:
        instance_ids_paris.append(ins['InstanceId'])


response = ec2_resource_paris.create_tags(
    Resources=[
        'string',
    ],
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)
reservation_frankfurt = ec2_resource_frankfurt.describe_instance()['Reservations']

for res in ec2_resource_frankfurt:
    instances = res["Instances"]
    for ins in instances:
        ec2_resource_frankfurt.append(ins['InstanceId'])


response = ec2_resource_frankfurt.create_tags(
    Resources=[
        'string',
    ],
    Tags=[
        {
            'Key': 'environment',
            'Value': 'dev'
        },
    ]
)