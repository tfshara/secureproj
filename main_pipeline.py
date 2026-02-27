import numpy as np
from training.train_model import train_model
from monitoring.ml_behaviour import analyze_ml_behaviour
from monitoring.cloud_monitor import monitor_cloud
from security.scenario_generator import generate_scenarios
from security.risk_model import train_risk_model
from governance.deployment_controller import deployment_decision
from governance.logger import log_event
from security.risk_model import show_feature_importance

# ---------- Step 1: Generate Dataset ----------
df = generate_scenarios(500)

# ---------- Step 2: Train Risk Model ----------
risk_model, feature_names = train_risk_model(df)
show_feature_importance(risk_model, feature_names)
# ---------- Step 3: Real Current Run ----------
metrics = train_model()
ml_behavior = analyze_ml_behaviour(metrics)
cloud_signals = monitor_cloud()

combined = {**ml_behavior, **cloud_signals}
sample = [combined.get(feature, 0) for feature in feature_names]

# ---------- HARD POLICY OVERRIDE ----------
if cloud_signals["dataset_public"] == 1:
    risk_probability = 1.0
    decision = "BLOCKED_POLICY"
else:
    risk_probability = risk_model.predict_proba([sample])[0][1]
    decision = deployment_decision(risk_probability)

print("\nCurrent Deployment Evaluation")
print("ML Metrics:", ml_behavior)
print("Cloud Signals:", cloud_signals)
print("Risk Probability:", risk_probability)
print("Deployment Decision:", decision)

# ---------- Logging AFTER decision ----------
log_event(ml_behavior, cloud_signals, risk_probability, decision)

# ---------- CI/CD Simulation ----------
print("\n--- CI/CD Pipeline Simulation ---")
print("Training Model...")
print("Evaluating Security...")

if decision == "DEPLOY":
    print("Pipeline Status: APPROVED")
else:
    print("Pipeline Status: BLOCKED")

# ---------- Deployment Gate Evaluation ----------
print("\n---- Deployment Gate Evaluation Over 200 Runs ----")

false_negative = 0
false_positive = 0
correct = 0

for _ in range(200):

    test_df = generate_scenarios(1)
    X_test = test_df.drop("unsafe", axis=1)
    true_label = test_df["unsafe"].values[0]

    risk_prob = risk_model.predict_proba(X_test)[0][1]
    predicted_label = 1 if risk_prob > 0.5 else 0

    if predicted_label == true_label:
        correct += 1
    elif predicted_label == 0 and true_label == 1:
        false_negative += 1
    elif predicted_label == 1 and true_label == 0:
        false_positive += 1

print("Correct Decisions:", correct)
print("False Negatives (Dangerous):", false_negative)
print("False Positives:", false_positive)
print("Gate Accuracy:", correct / 200)