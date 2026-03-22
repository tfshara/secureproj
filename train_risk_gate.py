#RANDOM FOREST

# import joblib

# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# from security.scenario_generator import generate_scenarios


# def train_model():

#     print("\nGenerating dataset (10000 scenarios)...")

#     df = generate_scenarios(10000)

#     X = df.drop("unsafe", axis=1)
#     y = df["unsafe"]

#     X_train, X_test, y_train, y_test = train_test_split(
#         X,
#         y,
#         test_size=0.2,
#         random_state=42,
#         stratify=y
#     )

#     print("\nTraining Risk Model...")

#     model = RandomForestClassifier(
#         n_estimators=400,
#         max_depth=12,
#         min_samples_split=6,
#         min_samples_leaf=2,
#         class_weight="balanced",
#         random_state=42
#     )

#     model.fit(X_train, y_train)

#     y_pred = model.predict(X_test)

#     print("\nConfusion Matrix:")
#     print(confusion_matrix(y_test, y_pred))

#     print("\nClassification Report:")
#     print(classification_report(y_test, y_pred))

#     accuracy = accuracy_score(y_test, y_pred)

#     print("\nFinal Model Accuracy:", round(accuracy, 3))

#     joblib.dump(model, "risk_model.pkl")

#     print("\nModel saved as risk_model.pkl")


# if __name__ == "__main__":
#     train_model()


#XGBOOST

# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, confusion_matrix
# from xgboost import XGBClassifier
# import joblib

# from security.scenario_generator import generate_scenarios

# print("\nGenerating dataset (10000 scenarios)...")
# df = generate_scenarios(10000)

# X = df.drop("unsafe", axis=1)
# y = df["unsafe"]

# # Train/test split
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42
# )

# print("\nTraining XGBoost Risk Model...")

# model = XGBClassifier(
#     n_estimators=400,
#     max_depth=6,
#     learning_rate=0.05,
#     subsample=0.8,
#     colsample_bytree=0.8,
#     random_state=42
# )

# model.fit(X_train, y_train)

# # Evaluation
# y_pred = model.predict(X_test)

# print("\nConfusion Matrix:")
# print(confusion_matrix(y_test, y_pred))

# print("\nClassification Report:")
# print(classification_report(y_test, y_pred))

# accuracy = (y_pred == y_test).mean()
# print("\nFinal Model Accuracy:", accuracy)

# # Save model
# joblib.dump(model, "risk_model.pkl")
# print("\nModel saved as risk_model.pkl")

#3

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from xgboost import XGBClassifier

from security.scenario_generator import generate_scenarios


def train_model():

    print("\nGenerating dataset (10000 scenarios)...")

    # Generate dataset
    df = generate_scenarios(10000)

    # 🔥 Remove non-numeric / meta columns
    df = df.drop(columns=['_scenario_type', '_risk_score'])

    # Split features and target
    X = df.drop("unsafe", axis=1)
    y = df["unsafe"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("\nTraining XGBoost Risk Model...")

    # 🔥 XGBoost with imbalance handling
    model = XGBClassifier(
       n_estimators=600,
       max_depth=7,
       learning_rate=0.04,
       subsample=0.9,
       colsample_bytree=0.9,
       scale_pos_weight=4,   # 🔥 unsafe ko importance
       random_state=42
    )

    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)
    # y_prob = model.predict_proba(X_test)[:, 1]
    # y_pred = (y_prob > 0.4).astype(int)

    # Evaluation
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    accuracy = accuracy_score(y_test, y_pred)
    print("\nFinal Model Accuracy:", round(accuracy, 3))

    # Save model
    joblib.dump(model, "risk_model.pkl")
    print("\nModel saved as risk_model.pkl")


if __name__ == "__main__":
    train_model()