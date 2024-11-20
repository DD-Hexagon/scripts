import matplotlib.pyplot as plt

# Data for visualization
total_users = 4517
non_matching_users = 2903
manual_correction_users = 1
total_groups = 559
non_matching_groups = 105
total_applications = 313
non_matching_applications = 77

# Calculate percentages
non_matching_users_pct = (non_matching_users / total_users) * 100
manual_correction_users_pct = (manual_correction_users / total_users) * 100
non_matching_groups_pct = (non_matching_groups / total_groups) * 100
non_matching_applications_pct = (non_matching_applications / total_applications) * 100

# 1. Total Users vs Non-Matching Organizations
plt.figure(figsize=(8, 6))
plt.bar(['Total Users', 'Users with Non-Matching Organizations'], 
        [total_users, non_matching_users], color=['blue', 'orange'])
plt.title("User Data Anomalies")
plt.xlabel("Category")
plt.ylabel("Number of Users")
plt.text(1, non_matching_users, f"{non_matching_users_pct:.1f}%", ha='center', va='bottom')
plt.show()

# 2. Manual Corrections
plt.figure(figsize=(6, 6))
plt.pie([100 - manual_correction_users_pct, manual_correction_users_pct], 
        labels=['No Correction Needed', 'Manual Correction Needed'], autopct='%1.1f%%', startangle=90, colors=['lightgrey', 'red'])
plt.title("Manual Correction Requirement for Users")
plt.show()

# 3. Groups with Non-Matching Organizations
plt.figure(figsize=(8, 6))
plt.bar(['Total Groups', 'Groups with Non-Matching Organizations'], 
        [total_groups, non_matching_groups], color=['green', 'purple'])
plt.title("Group Data Anomalies")
plt.xlabel("Category")
plt.ylabel("Number of Groups")
plt.text(1, non_matching_groups, f"{non_matching_groups_pct:.1f}%", ha='center', va='bottom')
plt.show()

# 4. Applications with Non-Matching Organizations
plt.figure(figsize=(8, 6))
plt.bar(['Total Applications', 'Applications with Non-Matching Organizations'], 
        [total_applications, non_matching_applications], color=['blue', 'orange'])
plt.title("Application Data Anomalies")
plt.xlabel("Category")
plt.ylabel("Number of Applications")
plt.text(1, non_matching_applications, f"{non_matching_applications_pct:.1f}%", ha='center', va='bottom')
plt.show()
