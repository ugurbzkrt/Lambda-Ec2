import json
import boto3

region = 'us-east-1'

ec2 = boto3.client('ec2', region_name=region)

def get_instance_ids(instance_names):

    all_instances = ec2.describe_instances()
    
    instance_ids = []
    
    # find instance-id based on instance name
    # many for loops but should work
    for instance_name in instance_names:
        for reservation in all_instances['Reservations']:
            for instance in reservation['Instances']:
                if 'Tags' in instance:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name' \
                            and tag['Value'] == instance_name:
                            instance_ids.append(instance['InstanceId'])
                            
    return instance_ids

def lambda_handler(event, context):
    
    instance_names = event["instances"].split(',')
    action = event["action"]

    instance_ids = get_instance_ids(instance_names)

    print(instance_ids)
