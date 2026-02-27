import json
import boto3
import joblib
import os
import numpy as np

s3 = boto3.client("s3")
sns = boto3.client("sns")

MODEL_BUCKET = os.environ["MODEL_BUCKET"]
MODEL_KEY = os.environ["MODEL_KEY"]
SNS_TOPIC = os.environ["SNS_TOPIC"]

THRESHOLD = 0.7


def load_model():
    s3.download_file(MODEL_BUCKET, MODEL_KEY, "/tmp/risk_model.pkl")
    return joblib.load("/tmp/risk_model.pkl")


def get_cloud_signals():
    # Example minimal real signal
    s3_client = boto3.client("s3")
    status = s3_client.get_bucket_policy_status(
        Bucket=os.environ["DATA_BUCKET"]
    )
    dataset_public = 1 if status["PolicyStatus"]["IsPublic"] else 0

    return {
        "dataset_public": dataset_public,
        "permission_change": 0,
        "cpu_spike": 0
    }


def lambda_handler(event, context):

    model = load_model()

    ml_signals = event["ml_metrics"]
    cloud_signals = get_cloud_signals()

    combined = {**ml_signals, **cloud_signals}

    feature_names = event["feature_names"]
    sample = [combined.get(f, 0) for f in feature_names]

    risk_score = model.predict_proba([sample])[0][1]

    if cloud_signals["dataset_public"] == 1:
        decision = "BLOCKED_POLICY"
    elif risk_score > THRESHOLD:
        decision = "BLOCKED_ML_RISK"
    else:
        decision = "APPROVED"

    if decision != "APPROVED":
        sns.publish(
            TopicArn=SNS_TOPIC,
            Message=f"Deployment BLOCKED. Reason: {decision}"
        )

    return {
        "statusCode": 200,
        "risk_score": float(risk_score),
        "decision": decision
    }