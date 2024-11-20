import csv
import json
from collections import defaultdict

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def load_organization_mapping(auth_server_file):
    # Load organization mapping from authorization server JSON.
    with open(auth_server_file, 'r', encoding='utf-8') as file:
        auth_servers = json.load(file)
    
    # Mapping from OrganizationId to organization name
    org_mapping = {}
    for server in auth_servers:
        organization_id = server.get("OrganizationId")
        organization_name = server.get("Name")
        if organization_id and organization_name:
            org_mapping[organization_id] = organization_name  # Map organization ID to organization name
    return org_mapping

def load_clipper_organization_mapping(clipper_orgs_file):
    # Load clipper organization mapping from clipper JSON.
    with open(clipper_orgs_file, 'r', encoding='utf-8') as file:
        orgs = json.load(file)
    
    # Mapping from OrganizationId to organization name
    clipper_org_mapping = {}
    for org in orgs["value"]:
        organization_id = org.get("Id")
        organization_name = org.get("Name")
        if organization_id and organization_name:
            clipper_org_mapping[organization_id] = organization_name  # Map organization ID to organization name
    return clipper_org_mapping

def process_json_to_csv(group_file, usergroup_file, appgroup_file, users_file, csv_file, org_mapping, clipper_org_mapping):
    # Load JSON data
    grp_data = load_json(group_file)
    usergroup_data = load_json(usergroup_file)
    appgroup_data = load_json(appgroup_file)
    users_data = load_json(users_file)

    # Create mapping dictionaries with aggregated values
    user_mapping = defaultdict(list)
    for item in usergroup_data:
        if item['UserId']:  # Ensure the value is not empty
            user_mapping[item['GroupId']].append(item['UserId'])

    app_mapping = defaultdict(list)
    for item in appgroup_data:
        if item['ApplicationName']:  # Ensure the value is not empty
            app_mapping[item['GroupId']].append(item['ApplicationName'])

    # Create a mapping from UserId to Login from users.json
    user_login_mapping = {}
    for user in users_data:
        user_id = user.get('Id')
        login = user.get('Login')
        if user_id and login:
            user_login_mapping[user_id] = login

    # Ensure data is a list
    if isinstance(grp_data, dict):
        grp_data = [grp_data]

    # CSV columns
    columns = [
        "Name",
        "Description",
        "Group ID",
        "Process Status",
        "IDP Status",
        "Organization",
        "Application",
        "User"
    ]

    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        for item in grp_data:
            if isinstance(item, dict):
                organization_id = item.get("OrganizationId", "")

                # Check if the organization ID length matches 36 characters
                if len(organization_id) == 36:
                    group_id = item.get("Id", "")
                    applications = app_mapping.get(group_id, [])

                    # Map user IDs to Login values
                    user_ids = user_mapping.get(group_id, [])
                    users = ','.join(filter(None, [user_login_mapping.get(user_id, "") for user_id in user_ids]))

                    organization_name = org_mapping.get(organization_id, "")
                    clipper_org_name = clipper_org_mapping.get(organization_id, "")
                    final_org_name = organization_name if organization_name else clipper_org_name

                    if final_org_name:
                        # Create a new row for each application in the group
                        for application in applications:
                            csv_row = {
                                "Name": (item.get("Name") or "").strip(),
                                "Description": (item.get("Description") or "").strip(),
                                "Group ID": group_id,
                                "Process Status": (item.get("ProcessStatus", "DONE") or "").strip(),
                                "IDP Status": (item.get("IDPStatus", "ACTIVE") or "").strip(),
                                "Organization": final_org_name,
                                "Application": application.strip(),
                                "User": users.strip(),
                            }

                            # Ensure only non-empty values are written
                            if any(value for key, value in csv_row.items() if key != "Group ID"):
                                writer.writerow(csv_row)

# File paths
group_file = 'groups.json'
usergroup_file = 'usergroupassignments.json'
appgroup_file = 'applicationgroupassignments.json'
users_file = 'users.json'
csv_file = 'groups.csv'

auth_server_file = 'authorizationservers.json'
clipper_organizations = 'clipperOrgs.json'

# Load organization mappings
org_mapping = load_organization_mapping(auth_server_file)
clipper_orgs_mapping = load_clipper_organization_mapping(clipper_organizations)

# Run the function
process_json_to_csv(group_file, usergroup_file, appgroup_file, users_file, csv_file, org_mapping, clipper_orgs_mapping)
