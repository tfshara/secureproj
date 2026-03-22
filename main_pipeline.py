# def full_experiment():

#     import sys
#     from training.train_model import train_model
#     from monitoring.ml_behaviour import analyze_ml_behaviour
#     from monitoring.cloud_monitor import monitor_cloud
#     from security.scenario_generator import generate_scenarios
#     from security.risk_model import train_risk_model, show_feature_importance
#     from governance.deployment_controller import deployment_decision
#     from governance.logger import log_event
#     from canary_controller import perform_canary_release

#     print("\n--- Research Mode: Full Experiment ---")

#     # ---------- Step 1: Generate Dataset ----------
#     df = generate_scenarios(500)

#     # ---------- Step 2: Train Risk Model ----------
#     risk_model, feature_names = train_risk_model(df)
#     show_feature_importance(risk_model, feature_names)

#     # ---------- Step 3: Real Current Run ----------
#     metrics = train_model()
#     ml_behavior = analyze_ml_behaviour(metrics)
#     cloud_signals = monitor_cloud()

#     combined = {**ml_behavior, **cloud_signals}
#     sample = [combined.get(feature, 0) for feature in feature_names]

#     # ---------- Hard Policy Override ----------
#     if cloud_signals.get("dataset_public", 0) == 1:
#         risk_probability = 1.0
#         decision = "BLOCKED_POLICY"
#     else:
#         risk_probability = risk_model.predict_proba([sample])[0][1]
#         decision = deployment_decision(risk_probability)

#     print("\nCurrent Deployment Evaluation")
#     print("ML Metrics:", ml_behavior)
#     print("Cloud Signals:", cloud_signals)
#     print("Risk Probability:", risk_probability)
#     print("Deployment Decision:", decision)

#     log_event(ml_behavior, cloud_signals, risk_probability, decision)

#     # ---------- Canary Simulation ----------
#     if decision == "DEPLOY":
#         result = perform_canary_release()
#         print("Canary Result:", result)
#     else:
#         print("Pipeline Status: BLOCKED")
#         sys.exit(1)

#     # ---------- 200 Run Evaluation ----------
#     false_negative = 0
#     false_positive = 0
#     correct = 0

#     for _ in range(200):
#         test_df = generate_scenarios(1)
#         X_test = test_df.drop("unsafe", axis=1)
#         true_label = test_df["unsafe"].values[0]

#         risk_prob = risk_model.predict_proba(X_test)[0][1]
#         predicted_label = 1 if risk_prob > 0.5 else 0

#         if predicted_label == true_label:
#             correct += 1
#         elif predicted_label == 0 and true_label == 1:
#             false_negative += 1
#         elif predicted_label == 1 and true_label == 0:
#             false_positive += 1

#     print("\n---- Deployment Gate Evaluation Over 200 Runs ----")
#     print("Correct Decisions:", correct)
#     print("False Negatives:", false_negative)
#     print("False Positives:", false_positive)
#     print("Gate Accuracy:", correct / 200)

#     return {
#         "decision": decision,
#         "risk_probability": float(risk_probability),
#         "accuracy": correct / 200
#     }


# def deployment_gate_only():

#     import sys
#     import joblib
#     from monitoring.ml_behaviour import analyze_ml_behaviour
#     from monitoring.cloud_monitor import monitor_cloud
#     from governance.deployment_controller import deployment_decision
#     from governance.logger import log_event
#     from canary_controller import perform_canary_release

#     print("\n--- Lambda Mode: Deployment Gate ---")

#     # Load pre-trained model
#     risk_model = joblib.load("risk_model.pkl")
#     feature_names = risk_model.feature_names_in_

#     ml_behavior = analyze_ml_behaviour({})
#     cloud_signals = monitor_cloud()

#     combined = {**ml_behavior, **cloud_signals}
#     sample = [combined.get(feature, 0) for feature in feature_names]

#     # Hard Policy Override
#     if cloud_signals.get("dataset_public", 0) == 1:
#         risk_probability = 1.0
#         decision = "BLOCKED_POLICY"
#     else:
#         risk_probability = risk_model.predict_proba([sample])[0][1]
#         decision = deployment_decision(risk_probability)

#     log_event(ml_behavior, cloud_signals, risk_probability, decision)

#     # CI/CD Gate
#     if decision == "DEPLOY":
#         perform_canary_release()
#     else:
#         sys.exit(1)

#     return {
#         "decision": decision,
#         "risk_probability": float(risk_probability)
#     }


# def run_pipeline(research_mode=False):

#     if research_mode:
#         return full_experiment()
#     else:
#         return deployment_gate_only()


# if __name__ == "__main__":
#     result = run_pipeline(research_mode=True)
#     print("\nFinal Result:")
#     print(result)



import sys
import joblib

from training.train_model import train_model
from monitoring.ml_behaviour import analyze_ml_behaviour
from monitoring.cloud_monitor import monitor_cloud
from governance.deployment_controller import deployment_decision
from governance.logger import log_event
from canary_controller import perform_canary_release


def run_pipeline():

    print("\n--- Production Deployment Gate ---")

    # Load trained risk model
    risk_model = joblib.load("risk_model.pkl")
    feature_names = risk_model.feature_names_in_

    # -----------------------------
    # Collect ML Behaviour Signals
    # -----------------------------
    metrics = train_model()
    ml_behavior = analyze_ml_behaviour(metrics)

    # -----------------------------
    # Collect Cloud Security Signals
    # -----------------------------
    cloud_signals = monitor_cloud()

    # Combine signals
    combined = {**ml_behavior, **cloud_signals}

    sample = [combined.get(feature, 0) for feature in feature_names]

    # -----------------------------
    # Policy Override
    # -----------------------------
    if cloud_signals.get("dataset_public", 0) == 1:

        risk_probability = 1.0
        decision = "BLOCKED_POLICY"

    else:

        risk_probability = risk_model.predict_proba([sample])[0][1]
        decision = deployment_decision(risk_probability)

    # -----------------------------
    # Print Evaluation
    # -----------------------------
    print("\nCurrent Deployment Evaluation")

    print("ML Metrics:", ml_behavior)
    print("Cloud Signals:", cloud_signals)

    print("Risk Probability:", risk_probability)
    print("Deployment Decision:", decision)

    # -----------------------------
    # Logging
    # -----------------------------
    log_event(ml_behavior, cloud_signals, risk_probability, decision)

    # -----------------------------
    # CI/CD Deployment Gate
    # -----------------------------
    if decision == "DEPLOY":

        print("\nPipeline Status: APPROVED")

        result = perform_canary_release()

        print("Canary Result:", result)

    else:

        print("\nPipeline Status: BLOCKED")

        sys.exit(1)

    return {
        "decision": decision,
        "risk_probability": float(risk_probability)
    }


if __name__ == "__main__":

    result = run_pipeline()

    print("\nFinal Result:")
    print(result)