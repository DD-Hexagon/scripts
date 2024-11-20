import csv
import json

def load_excluded_logins(my_users_file):
    # Load login names to be excluded from myUsers.json
    with open(my_users_file, 'r', encoding='utf-8') as file:
        excluded_logins = json.load(file)
    return set(excluded_logins)

def extract_name_from_email(email):
    if '@' in email:
        local_part = email.split('@')[0]
        if '.' in local_part:
            first_name, last_name = local_part.split('.', 1)
            return first_name.capitalize(), last_name.upper()
    return email.split('@')[0].capitalize(), email.split('@')[0].upper()  # Return the name before @ if no dot

def filter_users_by_org_id(json_file, org_id, output_csv, excluded_logins):
    with open(json_file, 'r', encoding='utf-8') as file:
        user_data = json.load(file)

    if isinstance(user_data, dict):
        user_data = [user_data]  

    columns = ["Login name", "First Name", "Last Name", "E-mail address", "OrganizationId"]
    filtered_users = []  # List to capture users with the specified organization ID

    for item in user_data:
        if isinstance(item, dict):
            login_name = (item.get("Login") or "").strip()

            # Skip the user if their login name is in the excluded logins set
            if login_name in excluded_logins:
                continue

            # Extract first and last names, fallback to parsing from email if needed
            first_name = (item.get("FirstName") or "").strip()
            last_name = (item.get("LastName") or "").strip()
            email = (item.get("Email") or "").strip()

            if not first_name or not last_name:
                # extracted_first_name, extracted_last_name = extract_name_from_email(email)
                # first_name = first_name or extracted_first_name
                # last_name = last_name or extracted_last_name

            # Check if user belongs to the specified organization ID
                organization_id = item.get("OrganizationId", "")
                filtered_users.append({
                    "Login name": login_name,
                    "First Name": first_name,
                    "Last Name": last_name,
                    "E-mail address": email,
                    "OrganizationId": organization_id
                })

    # Write filtered users to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(filtered_users)

# File paths
json_file = 'users.json'
output_csv = 'users_withot_name.csv'  # Output file for users with the specific organization ID
my_users_file = 'myUsers.json'

# Target organization ID
target_org_id = 'e9c1532a-5faa-4877-a373-45caec204853'

# Load excluded logins
excluded_logins = load_excluded_logins(my_users_file)

# Process data and write only users with the target organization ID to CSV
filter_users_by_org_id(json_file, target_org_id, output_csv, excluded_logins)
