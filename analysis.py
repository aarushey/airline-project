import pandas as pd

# Load the core files
loyalty = pd.read_csv('Customer Loyalty History.csv')
activity = pd.read_csv('Customer Flight Activity.csv')

print("=== COMPREHENSIVE DATA AUDIT: 16,700 DATASET ===")

# 1. SALARY ANOMALIES (Missing or Zero)
missing_sal = loyalty['Salary'].isnull().sum()
zero_sal = (loyalty['Salary'] == 0).sum()
print(f"[1] Salary Issues: {missing_sal} missing, {zero_sal} are zero.")

# 2. FINANCIAL ANOMALIES (Negative CLV)
neg_clv = (loyalty['CLV'] < 0).sum()
print(f"[2] Negative CLV: {neg_clv} rows found.")

# 3. DATE LOGIC ANOMALIES (Cancelled before Enrolled)
# We convert to a date format to compare
loyalty['Enroll_Date'] = pd.to_datetime(loyalty['Enrollment Year'].astype(str) + '-' + loyalty['Enrollment Month'].astype(str) + '-01')
loyalty['Cancel_Date'] = pd.to_datetime(loyalty['Cancellation Year'].astype(str) + '-' + loyalty['Cancellation Month'].astype(str) + '-01', errors='coerce')

date_errors = loyalty[loyalty['Cancel_Date'] < loyalty['Enroll_Date']]
print(f"[3] Logical Date Errors: {len(date_errors)} members cancelled before joining.")

# 4. ACTIVITY ANOMALIES (Distance without Flights)
ghost_flights = activity[(activity['Total Flights'] == 0) & (activity['Distance'] > 0)]
print(f"[4] Ghost Flights: {len(ghost_flights)} rows show distance traveled but 0 flights.")

# 5. DUPLICATE CHECK
dupes = loyalty['Loyalty Number'].duplicated().sum()
print(f"[5] Duplicate Loyalty IDs: {dupes} duplicates found.")

# 6. CANCELLATION SUMMARY
# Note: Missing values here are normal (it means they haven't cancelled)
active_members = loyalty['Cancellation Year'].isnull().sum()
print(f"[6] Active Members (No cancellation date): {active_members}")