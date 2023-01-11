import boto3
import schedule

ec2_client = boto3.client('ec2', region_name = "eu-west-3")


def create_volume_snapshots():
    volumes = ec2_client.describe_volumes()
    for volume in volumes['Volumes']:
        new_snapshot = ec2_client.create_snapshot(
            volumeId = volume['VolumeId']
        )

        print(new_snapshot)

schedule.every().day.do(create_volume_snapshots)
# schedule.every().monday.at("12:00")

while True:
    schedule.run_pending()