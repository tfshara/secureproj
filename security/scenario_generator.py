import numpy as np
import pandas as pd
import random

def generate_scenarios(n=500):

    data = []

    for _ in range(n):

        # --- ML Metrics ---
        accuracy = np.random.uniform(0.85, 0.99)
        accuracy_drift = np.random.uniform(-0.2, 0.05)
        confidence_variance = np.random.uniform(0.01, 0.05)
        entropy = np.random.uniform(0.1, 0.6)
        training_time = np.random.uniform(0.1, 0.5)

        # --- Cloud Signals ---
        dataset_public = random.choice([0,1])
        cpu_spike = random.choice([0,1])
        permission_change = random.choice([0,1])
        abnormal_retraining = random.choice([0,1])

        # --- Ground Truth Logic (Define Unsafe Conditions) ---
        unsafe = 0

        if dataset_public == 1:
            unsafe = 1
        elif accuracy_drift < -0.15 and abnormal_retraining == 1:
            unsafe = 1
        elif cpu_spike == 1 and permission_change == 1:
            unsafe = 1

        row = [
            accuracy,
            accuracy_drift,
            confidence_variance,
            entropy,
            training_time,
            dataset_public,
            cpu_spike,
            permission_change,
            abnormal_retraining,
            unsafe
        ]

        data.append(row)

    columns = [
        "accuracy",
        "accuracy_drift",
        "confidence_variance",
        "entropy",
        "training_time",
        "dataset_public",
        "cpu_spike",
        "permission_change",
        "abnormal_retraining",
        "unsafe"
    ]

    df = pd.DataFrame(data, columns=columns)
    return df