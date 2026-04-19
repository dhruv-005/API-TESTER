# ml_models.py
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

def classify_results(results):
    # Simple classifier: success if status_code==200
    labels = []
    for r in results:
        labels.append('Success' if r['status_code'] == 200 else 'Failure')
    return labels

def kmeans_clustering(results, n_clusters=2):
    data = []
    for r in results:
        length = len(r['response'])
        status = r['status_code'] or 0
        data.append([length, status])
    scaler = StandardScaler()
    X = scaler.fit_transform(data)
    km = KMeans(n_clusters=n_clusters, random_state=42)
    labels = km.fit_predict(X)
    return labels.tolist()
