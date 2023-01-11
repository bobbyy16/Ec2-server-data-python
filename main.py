# First spin up some servers then execute this code with region

import boto3
import schedule

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

# Instance running state
reservations = ec2_client.describe_instances()
for reservation in reservations['Reservations']:
    instances = reservation['Instances']
    for instance in instances:
        print(f"Instance {instance['InstanceId']} is {instance['State']['Name']}")


# instance status and system status check
statuses = ec2_client.describe_instance_status()
for status in statuses['InstanceStatuses']:
    instance_status = status['InstanceStatus']['Status']
    system_status = status['SystemStatus']['Status']
    print(f"Instance {status['InstanceId']} status is {instance_status} and system status is {system_status}")


# print running state and status check in one call

def check_instance_status(): # This function is used to schedule a function
    statuses = ec2_client.describe_instance_status(
        IncludeAllInstances=True
    )
    for status in statuses['InstanceStatuses']:
        instance_status = status['InstanceStatus']['Status']
        system_status = status['SystemStatus']['Status']
        state = status['InstanceState']['Name']
        print(f"Instance {status['InstanceId']} is {status} with instance status {instance_status} and system status {system_status}")
        print("#############\n")

schedule.every(5).minutes.do(check_instance_status)
# schedule.every().monday.at("12:00")

while True:
    schedule.run_pending()