from operator import itemgetter

import boto3


ec2_client = boto3.client('ec2', region_name = "eu-west-3")

snapshots = ec2_client.describe_snapshots(
    OwnerIds = ['self'] #only snapshots created by us
)

sortedBYDate = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

# snapshot deletion logic

for snap in sortedBYDate[2:]: #select every snapshot excluding lastest 2
    ec2_client.delete_snapshot(
        SnapshotId=snap['SnapshotId']
    )
