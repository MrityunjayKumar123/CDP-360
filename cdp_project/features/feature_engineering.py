# features/feature_engineering.py
import pandas as pd

loans = pd.DataFrame([
    {"loan_id": "L001", "customer_id": "CUST123", "bureau_score": 720, "repayment_ratio": 0.95},
    {"loan_id": "L002", "customer_id": "CUST456", "bureau_score": 650, "repayment_ratio": 0.70}
])

# Segment customers
loans['segment'] = loans['bureau_score'].apply(lambda x: 'prime' if x >= 700 else 'subprime')

print(loans)
