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

def load_excluded_logins(my_users_file):
    # Load login names to be excluded from myUsers.json
    with open(my_users_file, 'r', encoding='utf-8') as file:
        excluded_logins = json.load(file)
    return set(excluded_logins)

def process_json_to_csv(user_file, usergroup_file, group_file, csv_file, org_mapping, clipper_org_mapping, excluded_logins):
    # Load JSON data
    user_data = load_json(user_file)
    usergroup_data = load_json(usergroup_file)
    group_data = load_json(group_file)

    # Create a mapping of UserId to GroupIds from usergroupassignments.json
    user_group_mapping = defaultdict(list)
    for item in usergroup_data:
        user_id = item.get("UserId")
        group_id = item.get("GroupId")
        if user_id and group_id:
            user_group_mapping[user_id].append(group_id)

    # Create a mapping of GroupId to GroupName from groups.json
    group_name_mapping = {group.get("Id"): group.get("Name") for group in group_data if group.get("Id") and group.get("Name")}

    # Ensure data is a list
    if isinstance(user_data, dict):
        user_data = [user_data]

    # CSV columns
    columns = [
        "First Name",
        "Last Name",
        "Description",
        "Login name",
        "E-mail address",
        "Provider Type",
        "Application Admin",
        "Organization Admin",
        "System Admin",
        "Tenant Admin",
        "User Admin",
        "Organization",
        "Group",
        "Product",
        "Status"
    ]

    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

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
                    local_part = email.split('@')[0]
                    if '.' in local_part:
                        extracted_first_name, extracted_last_name = local_part.split('.', 1)
                        first_name = first_name or extracted_first_name.capitalize()
                        last_name = last_name or extracted_last_name.upper()
                    else:
                        first_name = first_name or local_part.capitalize()
                        last_name = last_name or local_part.upper()

                # Parse admin roles from comma-separated string
                admin_roles_str = item.get("AdminRoles", "")
                admin_roles = {
                    "Application Admin": "ApplicationAdministrator" in admin_roles_str,
                    "Organization Admin": "OrganizationAdministrator" in admin_roles_str,
                    "System Admin": "SystemAdministrator" in admin_roles_str,
                    "Tenant Admin": "TenantAdministrator" in admin_roles_str,
                    "User Admin": "UserAdministrator" in admin_roles_str,
                }

                # Retrieve organization name using OrganizationId
                organization_id = item.get("OrganizationId", "")
                organization_name = org_mapping.get(organization_id, "")
                clipper_org_name = clipper_org_mapping.get(organization_id, "")
                final_org_name = organization_name if organization_name else clipper_org_name

                # Only process user if they have associated groups
                user_id = item.get("Id")
                user_groups = user_group_mapping.get(user_id, [])

                if final_org_name and user_groups:
                    # Create a new row for each group associated with the user
                    for group_id in user_groups:
                        group_name = group_name_mapping.get(group_id, "Unknown Group")

                        csv_row = {
                            "First Name": first_name,
                            "Last Name": last_name,
                            "Description": (item.get("Description") or "").strip(),
                            "Login name": login_name,
                            "E-mail address": email,
                            "Provider Type": "Federation",
                            "Status": "ACTIVE" if item.get("IsActive") else "INACTIVE",
                            "Product": "SDx MT Cloud",
                            "Application Admin": admin_roles.get("Application Admin", False),
                            "Organization Admin": admin_roles.get("Organization Admin", False),
                            "System Admin": admin_roles.get("System Admin", False),
                            "Tenant Admin": admin_roles.get("Tenant Admin", False),
                            "User Admin": admin_roles.get("User Admin", False),
                            "Organization": final_org_name,
                            "Group": group_name,
                        }
                        writer.writerow(csv_row)

# File paths
user_file = 'users.json'
usergroup_file = 'usergroupassignments.json'
group_file = 'groups.json'
csv_file = 'users_with_groups.csv'
auth_server_file = 'authorizationservers.json'
clipper_organizations = 'clipperOrgs.json'
my_users_file = 'myUsers.json'

# Load organization mappings
org_mapping = load_organization_mapping(auth_server_file)
clipper_orgs_mapping = load_clipper_organization_mapping(clipper_organizations)

# Load excluded logins
excluded_logins = load_excluded_logins(my_users_file)

# Process data and write to CSV
process_json_to_csv(user_file, usergroup_file, group_file, csv_file, org_mapping, clipper_orgs_mapping, excluded_logins)
