import random

previous_accuracy = 0.95  # simulate previous run

def analyze_ml_behaviour(metrics):

    accuracy_drift = metrics["accuracy"] - previous_accuracy

    entropy = random.uniform(0.1, 0.5)  # simulate

    return {
        "accuracy": metrics["accuracy"],
        "accuracy_drift": accuracy_drift,
        "confidence_variance": metrics["confidence_variance"],
        "entropy": entropy,
        "training_time": metrics["training_time"]
    }