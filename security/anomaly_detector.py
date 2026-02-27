from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyDetector:

    def __init__(self):
        self.model = IsolationForest(contamination=0.1)

    def train(self, normal_data):
        self.model.fit(normal_data)

    def score(self, sample):
        score = self.model.decision_function([sample])[0]
        return -score  # higher = more anomalous