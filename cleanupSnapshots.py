from operator import itemgetter
import schedule
import boto3


ec2_client = boto3.client('ec2', region_name = "eu-west-3")


volumes = ec2_client.describe_volumes(
    # only create snapshots for prod / dev / testing servers
    Filter = [
        {
            'Name': 'tag:Name',
            'Values': ['prod']
        }
    ]
)

for volume in volumes['Volumes']:
    snapshots = ec2_client.describe_snapshots(
        OwnerIds = ['self'], #only snapshots created by us
        Filter = [
            {
                'Name': 'volume-id',
                'Values': [volume['VolumeId']]
            }
        ]
    )

    sortedBYDate = sorted(snapshots['Snapshots'], key=itemgetter('StartTime'), reverse=True)

    # snapshot deletion logic

    for snap in sortedBYDate[2:]: #select every snapshot excluding lastest 2
        res= ec2_client.delete_snapshot(
            SnapshotId=snap['SnapshotId']
        )
        print(res)
