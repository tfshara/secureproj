import json
from datetime import datetime

def log_event(ml_metrics, cloud_signals, risk_score, decision):

    log_entry = {
        "timestamp": str(datetime.now()),
        "ml_metrics": ml_metrics,
        "cloud_signals": cloud_signals,
        "risk_score": float(risk_score),
        "decision": decision
    }

    with open("deployment_logs.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")