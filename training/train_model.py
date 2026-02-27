from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import time

def train_model():

    data = load_breast_cancer()
    X = data.data
    y = data.target

    start_time = time.time()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    training_time = time.time() - start_time

    probabilities = model.predict_proba(X_test)
    confidence_variance = np.var(np.max(probabilities, axis=1))

    return {
        "accuracy": accuracy,
        "training_time": training_time,
        "confidence_variance": confidence_variance
    }