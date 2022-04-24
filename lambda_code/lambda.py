import boto3
import json 
import os 

asg_client = boto3.client('autoscaling')

response = asg_client.describe_auto_scaling_groups( 
    Filters=[
        {
            'Name': 'tag:lambda_scale_down',
            'Values': [
                'True',
            ]
        },
    ]
)

# Pull down current list of ASGs that are tagged for shutdown cycle
asg_list = [] 
for x in range(len(response["AutoScalingGroups"])):
    asg_name = response["AutoScalingGroups"][x]["AutoScalingGroupName"]
    asg_list.append([asg_name, x])


def lambda_handler(event, context):
    for group in asg_list:
        asg_group = str(group[0])

        # Confirm the current status of the group
        asg_group_current_status(group)
        
        # Action accordingly to the current status
        if asg_group_current_status(group):
            action = "Starting"
            min_size = 1
            max_size = 2
            desired_capacity = 1
        else:
            action = "Stopping"
            min_size = 0
            max_size = 0
            desired_capacity = 0

        print (action + ": " + asg_group)
        asg_update = asg_client.update_auto_scaling_group(
            AutoScalingGroupName= asg_group,
            MinSize = min_size,
            MaxSize = max_size,
            DesiredCapacity = desired_capacity,
        )

        print (asg_update)


# Checks the current group State
def asg_group_current_status(group):
    min_group_size = response["AutoScalingGroups"][group[1]]["MinSize"]
    if min_group_size == 0:
        return True
    else:
        return False
    