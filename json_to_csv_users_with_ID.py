import csv
import json

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

def extract_name_from_email(email):
    if '@' in email:
        local_part = email.split('@')[0]
        if '.' in local_part:
            first_name, last_name = local_part.split('.', 1)
            return first_name.capitalize(), last_name.upper()
    return email.split('@')[0].capitalize(), email.split('@')[0].upper()  # Return the name before @ if no dot

def process_json_to_csv(json_file, csv_file, org_mapping, clipper_org_mapping, excluded_logins):
    with open(json_file, 'r', encoding='utf-8') as file:
        user_data = json.load(file)

    if isinstance(user_data, dict):
        user_data = [user_data]  

    columns = [
        # "First Name",
        # "Last Name",
        # "Description",
        "Login name",
        # "E-mail address",
        # "Provider Type",
        # "Application Admin",
        # "Organization Admin",
        # "System Admin",
        # "Tenant Admin",
        # "User Admin",
        # "Organization",
        # "Group",
        # "Product",
        # "Status",
        "Id"
    ]

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
                    extracted_first_name, extracted_last_name = extract_name_from_email(email)
                    first_name = first_name or extracted_first_name
                    last_name = last_name or extracted_last_name

                # Parse admin roles from comma-separated string
                admin_roles_str = item.get("AdminRoles", "")
                if "All" in admin_roles_str:
                    admin_roles = {
                        "Application Admin": True,
                        "Organization Admin": True,
                        "System Admin": True,
                        "Tenant Admin": True,
                        "User Admin": True
                    }
                else:
                 # Define each role individually if "ALL" is not present
                    admin_roles = {
                        "Application Admin": "ApplicationAdministrator" in admin_roles_str,
                        "Organization Admin": "OrganizationAdministrator" in admin_roles_str,
                        "System Admin": "SystemAdministrator" in admin_roles_str,
                        "Tenant Admin": "TenantAdministrator" in admin_roles_str,
                        "User Admin": "UserAdministrator" in admin_roles_str
                    }
                # Convert groups to comma-separated string if needed
                groups = ','.join(item.get("GroupIds", [])) if item.get("GroupIds") else ""
                id = item.get("Id")
                # Retrieve organization name using OrganizationId
                organization_id = item.get("OrganizationId", "")
                organization_name = org_mapping.get(organization_id, "")
                clipper_org_name = clipper_org_mapping.get(organization_id, "")
                final_org_name = organization_name if organization_name else clipper_org_name

                # Only write row if either organization_name or clipper_org_name is found
                if clipper_org_name:
                    csv_row = {
                        # "First Name": first_name,
                        # "Last Name": last_name,
                        # "Description": (item.get("Description") or "").strip(),
                        "Login name": "USR_" + login_name,
                        # "E-mail address": email,
                        # "Provider Type": "Federation",
                        # "Status": "ACTIVE" if item.get("IsActive") else "INACTIVE",
                        # "Product": "SDx MT Cloud",
                        # "Application Admin": admin_roles.get("Application Admin", False),
                        # "Organization Admin": admin_roles.get("Organization Admin", False),
                        # "System Admin": admin_roles.get("System Admin", False),
                        # "Tenant Admin": admin_roles.get("Tenant Admin", False),
                        # "User Admin": admin_roles.get("User Admin", False),
                        # "Organization": clipper_org_name,
                        # "Group": groups,
                        "Id": id
                    }

                    writer.writerow(csv_row)

# File paths
json_file = 'users.json'
csv_file = 'users_with_id.csv'
auth_server_file = 'authorizationservers.json'
clipper_organizations = 'clipperOrgs.json'
my_users_file = 'myUsers.json'

# Load organization mappings
org_mapping = load_organization_mapping(auth_server_file)
clipper_orgs_mapping = load_clipper_organization_mapping(clipper_organizations)

# Load excluded logins
excluded_logins = load_excluded_logins(my_users_file)

# Process data and write to CSV
process_json_to_csv(json_file, csv_file, org_mapping, clipper_orgs_mapping, excluded_logins)
