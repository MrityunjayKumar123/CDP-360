# identity_resolution/dedupe_job.py
import dedupe
import pandas as pd

data = pd.DataFrame([
    {"customer_id": "CUST123", "name": "Ravi Sharma", "phone": "9999999999"},
    {"customer_id": "CUST124", "name": "R. Sharma", "phone": "9999999999"}
])

fields = [
    {'field': 'name', 'type': 'String'},
    {'field': 'phone', 'type': 'String'}
]

deduper = dedupe.Dedupe(fields)
deduper.sample(data.to_dict('records'), 10)

deduper.train()
clusters = deduper.partition(data.to_dict('records'), threshold=0.5)

print("Identity Resolution Clusters:", clusters)
