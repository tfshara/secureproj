def compute_risk(ml_score, cloud_signals):

    # Critical override
    if cloud_signals["dataset_public"] == 1:
        return 0.9

    cloud_risk = (
        cloud_signals["dataset_public"] * 0.5 +
        cloud_signals["permission_change"] * 0.2 +
        cloud_signals["cpu_spike"] * 0.2 +
        cloud_signals["abnormal_retraining"] * 0.1
    )

    final_risk = 0.5 * ml_score + 0.5 * cloud_risk

    return final_risk