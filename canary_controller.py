import boto3
import time
from datetime import datetime, timedelta

lambda_client = boto3.client("lambda", region_name="ap-southeast-2")
cloudwatch = boto3.client("cloudwatch", region_name="ap-southeast-2")

FUNCTION_NAME = "secure-ml-deploy"
ALIAS_NAME = "prod"
MONITOR_SECONDS = 60
ERROR_THRESHOLD = 1

import boto3
from datetime import datetime, timedelta

cloudwatch = boto3.client("cloudwatch")

def get_error_count():

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=1)

    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/Lambda",
        MetricName="Errors",
        Dimensions=[
            {
                "Name": "FunctionName",
                "Value": FUNCTION_NAME
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=60,
        Statistics=["Sum"]
    )

    datapoints = response["Datapoints"]

    if not datapoints:
        return 0

    return int(datapoints[0]["Sum"])
def perform_canary_release():

    import time

    print("Publishing new version...")

    publish_response = lambda_client.publish_version(
        FunctionName=FUNCTION_NAME
    )

    new_version = publish_response["Version"]
    print("New version:", new_version)

    # Get current alias state
    alias = lambda_client.get_alias(
        FunctionName=FUNCTION_NAME,
        Name=ALIAS_NAME
    )

    current_version = alias["FunctionVersion"]

    # If already pointing to same version → skip
    if current_version == new_version:
        print("Version already active. Skipping canary.")
        return "SKIPPED"

    print("Shifting 10% traffic to new version...")
    print("Invoking function to generate traffic...")

    for _ in range(20):
      lambda_client.invoke(
        FunctionName=FUNCTION_NAME,
        Qualifier=ALIAS_NAME,
        InvocationType="RequestResponse"
     )

    lambda_client.update_alias(
        FunctionName=FUNCTION_NAME,
        Name=ALIAS_NAME,
        RoutingConfig={
            "AdditionalVersionWeights": {
                new_version: 0.1
            }
        }
    )

    print("Monitoring for errors for 60 seconds...")
    time.sleep(60)

    # ---- Monitor Errors ----
    # (Assuming you already have CloudWatch logic here)
    error_count = get_error_count()  # your existing function

    print("Error count during canary:", error_count)

    if error_count > 0:
        print("Errors detected. Rolling back...")

        lambda_client.update_alias(
            FunctionName=FUNCTION_NAME,
            Name=ALIAS_NAME,
            FunctionVersion=current_version,
            RoutingConfig={}
        )

        return "ROLLED_BACK"

    else:
        print("No errors detected. Promoting new version...")

        lambda_client.update_alias(
            FunctionName=FUNCTION_NAME,
            Name=ALIAS_NAME,
            FunctionVersion=new_version,
            RoutingConfig={}
        )

        return "PROMOTED"