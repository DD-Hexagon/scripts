import csv
import json

# Define mappings for application types
application_type_mapping = {
    "Web": "Web",
    "Native": "Native",
    "Browser": "Browser",  # for this app type, Refresh Token must be True
    "Service": "Service"
}

def load_organization_mapping(auth_server_file):
    """Load organization mapping from authorization server JSON."""
    with open(auth_server_file, 'r', encoding='utf-8') as file:
        auth_servers = json.load(file)
    
    # Mapping from application ID to organization name
    org_mapping = {}
    for server in auth_servers:
        organization_name = server.get("Name")
        for policy in server.get("Policies", []):
            for app_id in policy.get("Applications", []):
                org_mapping[app_id] = organization_name  # Map app_id to organization name
    return org_mapping

def process_json_to_csv(json_file, csv_file, org_mapping):
    with open(json_file, 'r', encoding='utf-8') as file:
        app_data = json.load(file)

    if isinstance(app_data, dict):
        app_data = [app_data]  

    columns = [
        "Name",
        "Description",
        "Authorization Code",
        "Client Credentials",
        "Implicit",
        "Refresh Token",
        "Resource Owner",
        "Application ID",
        "Application Admin",
        "Organization Admin",
        "System Admin",
        "Tenant Admin",
        "User Admin",
        "Identity",
        "Process Status",  # DONE
        "IDP Status",  # ACTIVE
        "Type",
        "Client ID",
        "Login URI",
        "Redirect URI",
        "Post Logout Redirect URI",
        "Organization",
        "Group",
        "Tenant",
        "Classification"
    ]

    # Set to keep track of unique application names
    written_names = set()

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        for item in app_data:
            # Parse admin roles from comma-separated string
            admin_roles_str = item.get("AdminRoles", "")
            admin_roles = {
                "Application Admin": "ApplicationAdministrator" in admin_roles_str,
                "Organization Admin": "OrganizationAdministrator" in admin_roles_str,
                "System Admin": "SystemAdministrator" in admin_roles_str,
                "Tenant Admin": "TenantAdministrator" in admin_roles_str,
                "User Admin": "UserAdministrator" in admin_roles_str,
            }

            # Parse authentication flows from comma-separated string
            auth_flows_str = item.get("AuthenticationFlows", "")
            authentication_flows = {
                "Authorization Code": "AuthorizationCode" in auth_flows_str,
                "Client Credentials": "ClientCredentials" in auth_flows_str,
                "Implicit": "Implicit" in auth_flows_str,
                "Refresh Token": "RefreshToken" in auth_flows_str,
                "Resource Owner": "ResourceOwner" in auth_flows_str
            }

            # Ensure Refresh Token is True for Browser applications
            classification = application_type_mapping.get(item.get("ApplicationType", "Web"))
            if classification == "Browser":
                authentication_flows["Refresh Token"] = True

            # Convert lists to comma-separated strings, handling None values
            redirect_uris = ','.join(uri or "" for uri in item.get("RedirectUris", []))
            post_logout_redirect_uris = ','.join(uri or "" for uri in item.get("PostLogoutRedirectUris", []))
            tenants = ','.join(tenant or "" for tenant in item.get("TenantIds", []))
            groups = ','.join(group or "" for group in item.get("GroupIds", []))

            # Find Organization name based on application ID
            organization_name = org_mapping.get(item.get("Id"), "")

            csv_row = {
                "Name": item.get("Name", ""),
                "Description": item.get("Description", ""),
                "Authorization Code": authentication_flows.get("Authorization Code", False),
                "Client Credentials": authentication_flows.get("Client Credentials", False),
                "Implicit": authentication_flows.get("Implicit", False),
                "Refresh Token": authentication_flows.get("Refresh Token", False),
                "Resource Owner": authentication_flows.get("Resource Owner", False),
                "Application ID": item.get("Id", ""),
                "Application Admin": admin_roles.get("Application Admin", False),
                "Organization Admin": admin_roles.get("Organization Admin", False),
                "System Admin": admin_roles.get("System Admin", False),
                "Tenant Admin": admin_roles.get("Tenant Admin", False),
                "User Admin": admin_roles.get("User Admin", False),
                "Identity": item.get("Identity", ""),
                "Process Status": item.get("ProcessStatus", "DONE"),
                "IDP Status": item.get("IDPStatus", "ACTIVE"),
                "Type": classification,
                "Client ID": item.get("ClientId") if item.get("ClientId") is not None else item.get("Id", ""),
                "Login URI": item.get("LoginUri", ""),
                "Redirect URI": redirect_uris,
                "Post Logout Redirect URI": post_logout_redirect_uris,
                "Organization": organization_name,  # Use organization name here
                "Group": groups,
                "Tenant": tenants,
                "Classification": classification
            }

            # Only write the row if the application name hasn't been written yet
            if csv_row["Name"] and csv_row["Name"] not in written_names:
                writer.writerow(csv_row)
                written_names.add(csv_row["Name"])  # Track the written name

# Paths to JSON files
json_file = 'applications.json'
auth_server_file = 'authorizationservers.json'
csv_file = 'applications.csv'

# Load organization mapping
org_mapping = load_organization_mapping(auth_server_file)

# Process JSON to CSV with organization mapping
process_json_to_csv(json_file, csv_file, org_mapping)