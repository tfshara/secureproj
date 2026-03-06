# import boto3

# def monitor_cloud():

#     s3 = boto3.client("s3")
#     cloudtrail = boto3.client("cloudtrail")

#     bucket_name = "ml-dataset-bucket-demo-unique123"

#     signals = {}

#     # ----------------------------
#     # 1️⃣ S3 Public Exposure Check
#     # ----------------------------
#     try:
#         status = s3.get_bucket_policy_status(Bucket=bucket_name)
#         is_public = status["PolicyStatus"]["IsPublic"]
#         signals["dataset_public"] = 1 if is_public else 0
#     except Exception as e:
#         signals["dataset_public"] = 0

#     # ----------------------------
#     # 2️⃣ IAM Change Detection
#     # ----------------------------
#     events = cloudtrail.lookup_events(
#         LookupAttributes=[
#             {"AttributeKey": "EventSource", "AttributeValue": "iam.amazonaws.com"}
#         ],
#         MaxResults=5
#     )

#     signals["permission_change"] = 1 if events["Events"] else 0
#     signals["cpu_spike"] = 0

#     return signals

import boto3
from datetime import datetime, timedelta

def monitor_cloud():

    s3 = boto3.client("s3")
    cloudtrail = boto3.client("cloudtrail")
    cloudwatch = boto3.client("cloudwatch")

    bucket_name = "ml-dataset-bucket-demo-unique123"

    signals = {}

    # --------------------------------
    # 1️⃣ S3 Public Exposure Check
    # --------------------------------
    try:
        status = s3.get_bucket_policy_status(Bucket=bucket_name)
        is_public = status["PolicyStatus"]["IsPublic"]
        signals["dataset_public"] = 1 if is_public else 0
    except Exception:
        signals["dataset_public"] = 0

    # --------------------------------
    # 2️⃣ IAM Change Detection
    # --------------------------------
    try:

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=5)

        events = cloudtrail.lookup_events(
            LookupAttributes=[
                {
                    "AttributeKey": "EventSource",
                    "AttributeValue": "iam.amazonaws.com"
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            MaxResults=10
        )

        signals["permission_change"] = 1 if events["Events"] else 0

    except Exception:
        signals["permission_change"] = 0

    # --------------------------------
    # 3️⃣ CPU Spike Detection
    # --------------------------------
    try:

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=5)

        metrics = cloudwatch.get_metric_statistics(
            Namespace="AWS/Lambda",
            MetricName="Duration",
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=["Average"]
        )

        if metrics["Datapoints"]:

            avg = metrics["Datapoints"][0]["Average"]

            # threshold example
            signals["cpu_spike"] = 1 if avg > 2000 else 0

        else:
            signals["cpu_spike"] = 0

    except Exception:
        signals["cpu_spike"] = 0

    return signals