# import random
# import psutil

# def monitor_cloud():

#     cpu_usage = psutil.cpu_percent(interval=1)
#     # cpu_spike = 1 if cpu_usage > 80 else 0

#     # dataset_public = random.choice([0,1])
#     # permission_change = random.choice([0,1])
#     # abnormal_retraining = random.choice([0,1])
#     dataset_public = 1
#     permission_change = 1
#     abnormal_retraining = 1
#     cpu_spike = 1

#     return {
#         "dataset_public": dataset_public,
#         "cpu_spike": cpu_spike,
#         "permission_change": permission_change,
#         "abnormal_retraining": abnormal_retraining
#     }

import boto3

def monitor_cloud():

    s3 = boto3.client("s3")
    cloudtrail = boto3.client("cloudtrail")

    bucket_name = "ml-dataset-bucket-demo-unique123"

    signals = {}

    # ----------------------------
    # 1️⃣ S3 Public Exposure Check
    # ----------------------------
    try:
        status = s3.get_bucket_policy_status(Bucket=bucket_name)
        is_public = status["PolicyStatus"]["IsPublic"]
        signals["dataset_public"] = 1 if is_public else 0
    except Exception as e:
        signals["dataset_public"] = 0

    # ----------------------------
    # 2️⃣ IAM Change Detection
    # ----------------------------
    events = cloudtrail.lookup_events(
        LookupAttributes=[
            {"AttributeKey": "EventSource", "AttributeValue": "iam.amazonaws.com"}
        ],
        MaxResults=5
    )

    signals["permission_change"] = 1 if events["Events"] else 0
    signals["cpu_spike"] = 0

    return signals