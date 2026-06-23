# identity_resolution/dedupe_job.py
import pandas as pd
from fuzzywuzzy import fuzz
from collections import defaultdict

data = pd.DataFrame([
    {"customer_id": "CUST123", "name": "Ravi Sharma", "phone": "9999999999"},
    {"customer_id": "CUST124", "name": "R. Sharma", "phone": "9999999999"}
])

clusters = defaultdict(list)
matched = set()
threshold = 0.85

for i, row1 in data.iterrows():
    if i in matched:
        continue
    cluster = [row1.to_dict()]
    for j, row2 in data.iterrows():
        if i != j and j not in matched:
            score = max(
                fuzz.token_set_ratio(row1['name'], row2['name']),
                fuzz.token_set_ratio(row1['phone'], row2['phone'])
            )
            if score >= threshold * 100:
                cluster.append(row2.to_dict())
                matched.add(j)
    clusters[i] = cluster

print("Identity Resolution Clusters:", list(clusters.values()))
