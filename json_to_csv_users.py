import csv
import json

def load_organization_mapping(auth_server_file):
    #Load organization mapping from authorization server JSON.
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

def process_json_to_csv(json_file, csv_file, org_mapping):
    with open(json_file, 'r', encoding='utf-8') as file:
        user_data = json.load(file)

    if isinstance(user_data, dict):
        user_data = [user_data]  

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

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        for item in user_data:
            if isinstance(item, dict):
                # Parse admin roles from comma-separated string
                admin_roles_str = item.get("AdminRoles", "")
                admin_roles = {
                    "Application Admin": "ApplicationAdministrator" in admin_roles_str,
                    "Organization Admin": "OrganizationAdministrator" in admin_roles_str,
                    "System Admin": "SystemAdministrator" in admin_roles_str,
                    "Tenant Admin": "TenantAdministrator" in admin_roles_str,
                    "User Admin": "UserAdministrator" in admin_roles_str,
                }

                # Convert groups to comma-separated string if needed (assuming GroupIds exist)
                groups = ','.join(item.get("GroupIds", [])) if item.get("GroupIds") else ""

                # Retrieve organization name using OrganizationId
                organization_id = item.get("OrganizationId", "")
                organization_name = org_mapping.get(organization_id, "")

                # Only write row if organization name is found
                if organization_name:
                    csv_row = {
                        "First Name": item.get("FirstName", ""),
                        "Last Name": item.get("LastName", ""),
                        "Description": item.get("Description", ""),
                        "Login name": item.get("Login", ""),
                        "E-mail address": item.get("Email", ""),
                        "Provider Type": "Federation",
                        "Status": "ACTIVE" if item.get("IsActive") else "INACTIVE",
                        "Product": "SDx MT Cloud",
                        "Application Admin": admin_roles.get("Application Admin", False),
                        "Organization Admin": admin_roles.get("Organization Admin", False),
                        "System Admin": admin_roles.get("System Admin", False),
                        "Tenant Admin": admin_roles.get("Tenant Admin", False),
                        "User Admin": admin_roles.get("User Admin", False),
                        "Organization": organization_name,  # Set organization name here
                        "Group": groups,
                    }

                    writer.writerow(csv_row)

json_file = 'users.json'
csv_file = 'users.csv'
auth_server_file = 'authorizationservers.json'

# Load organization mapping
org_mapping = load_organization_mapping(auth_server_file)
process_json_to_csv(json_file, csv_file, org_mapping)

