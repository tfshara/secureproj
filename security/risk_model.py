from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import matplotlib.pyplot as plt
def train_risk_model(df):

    X = df.drop("unsafe", axis=1)
    y = df["unsafe"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Risk Model Evaluation")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

    joblib.dump(model, "risk_model.pkl")

    return model, X.columns
def show_feature_importance(model, feature_names):

    importances = model.feature_importances_

    sorted_indices = importances.argsort()[::-1]

    print("\nFeature Importance Ranking:")
    for idx in sorted_indices:
        print(f"{feature_names[idx]}: {importances[idx]:.4f}")

    plt.figure()
    plt.title("Feature Importance")
    plt.bar(range(len(importances)), importances[sorted_indices])
    plt.xticks(range(len(importances)),
               [feature_names[i] for i in sorted_indices],
               rotation=45)
    plt.tight_layout()
    plt.show()