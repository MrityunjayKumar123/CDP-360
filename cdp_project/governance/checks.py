# governance/great_expectations_checks.py
import great_expectations as ge

df = ge.dataset.PandasDataset({
    "loan_id": ["L001", "L002"],
    "customer_id": ["CUST123", "CUST456"],
    "bureau_score": [720, 650]
})

df.expect_column_values_to_not_be_null("loan_id")
df.expect_column_values_to_be_between("bureau_score", min_value=300, max_value=850)

results = df.validate()
print(results)
