import csv
import json


def load_organization_mapping(auth_server_file):
    with open(auth_server_file, 'r', encoding='utf-8') as file:
        auth_servers = json.load(file)

    org_mapping = {}
    for server in auth_servers:
        organization_id = server.get("OrganizationId")
        organization_name = server.get("Name")
        if organization_id and organization_name:
            org_mapping[organization_id] = organization_name
    return org_mapping


def load_clipper_organization_mapping(clipper_orgs_file):
    with open(clipper_orgs_file, 'r', encoding='utf-8') as file:
        orgs = json.load(file)

    clipper_org_mapping = {}
    for org in orgs["value"]:
        organization_id = org.get("Id")
        organization_name = org.get("Name")
        if organization_id and organization_name:
            clipper_org_mapping[organization_id] = organization_name
    return clipper_org_mapping


def load_excluded_logins(my_users_file):
    with open(my_users_file, 'r', encoding='utf-8') as file:
        excluded_logins = json.load(file)
    return set(excluded_logins)


def extract_name_from_email(email):
    if '@' in email:
        local_part = email.split('@')[0]
        if '.' in local_part:
            first_name, last_name = local_part.split('.', 1)
            return first_name.capitalize(), last_name.upper()
    return email.split('@')[0].capitalize(), email.split('@')[0].upper()


def match_hcap_users_to_ids(hcap_users_file, users_file):
    with open(hcap_users_file, 'r', encoding='utf-8') as file:
        hcap_users = json.load(file)

    with open(users_file, 'r', encoding='utf-8') as file:
        users_data = json.load(file)

    if isinstance(users_data, dict):
        users_data = [users_data]

    login_to_id = {user.get("Login", "").strip(): user for user in users_data if "Login" in user}

    for hcap_user in hcap_users.get("value", []):
        spf_login_name = hcap_user.get("SPFLoginName", "").strip()
        matching_user = login_to_id.get(spf_login_name)
        if matching_user:
            hcap_user.update(matching_user)

    return hcap_users


def process_json_to_csv(json_file, csv_file, org_mapping, clipper_org_mapping, excluded_logins, hcap_users_file):
    hcap_users = match_hcap_users_to_ids(hcap_users_file, json_file)

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
        "Status",
        "ID"
    ]

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        for hcap_user in hcap_users.get("value", []):
            spf_login_name = hcap_user.get("SPFLoginName", "").strip()
            user_id = hcap_user.get("Id")
            

            first_name = (hcap_user.get("FirstName") or "").strip() or extract_name_from_email(spf_login_name)[0]
            last_name = (hcap_user.get("LastName") or "").strip() or extract_name_from_email(spf_login_name)[1]
            email = hcap_user.get("Email", "").strip() or spf_login_name

            admin_roles_str = hcap_user.get("AdminRoles", "")
            if "All" in admin_roles_str:
                # If "All" is present, all roles are granted
                admin_roles = {
                    "Application Admin": True,
                    "Organization Admin": True,
                    "System Admin": True,
                    "Tenant Admin": True,
                    "User Admin": True
                }
            else:
                # Parse individual roles
                admin_roles = {
                    "Application Admin": "ApplicationAdministrator" in admin_roles_str,
                    "Organization Admin": "OrganizationAdministrator" in admin_roles_str,
                    "System Admin": "SystemAdministrator" in admin_roles_str,
                    "Tenant Admin": "TenantAdministrator" in admin_roles_str,
                    "User Admin": "UserAdministrator" in admin_roles_str
                }

            groups = ','.join(hcap_user.get("GroupIds", [])) if hcap_user.get("GroupIds") else ""

            organization_id = hcap_user.get("OrganizationId", "")
            organization_name = org_mapping.get(organization_id, "")
            clipper_org_name = clipper_org_mapping.get(organization_id, "")
            final_org_name = organization_name if organization_name else clipper_org_name

            csv_row = {
                "First Name": first_name,
                "Last Name": last_name,
                "Description": hcap_user.get("Description", "").strip(),
                "Login name": spf_login_name,
                "E-mail address": email,
                "Provider Type": "Federation",
                "Status": "ACTIVE" if hcap_user.get("IsActive") else "INACTIVE",
                "Product": "SDx MT Cloud",
                "Application Admin": admin_roles["Application Admin"],
                "Organization Admin": admin_roles["Organization Admin"],
                "System Admin": admin_roles["System Admin"],
                "Tenant Admin": admin_roles["Tenant Admin"],
                "User Admin": admin_roles["User Admin"],
                "Organization": final_org_name,
                "Group": groups,
                "ID": user_id
            }

            writer.writerow(csv_row)


# File paths
json_file = 'users.json'
csv_file = 'hcap_users_with_no_ID.csv'
auth_server_file = 'authorizationservers.json'
clipper_organizations = 'clipperOrgs.json'
my_users_file = 'myUsers.json'
hcap_users_file = 'HCAPUsersWithouID.json'

# Load mappings and exclusions
org_mapping = load_organization_mapping(auth_server_file)
clipper_orgs_mapping = load_clipper_organization_mapping(clipper_organizations)
excluded_logins = load_excluded_logins(my_users_file)

# Process and write to CSV
process_json_to_csv(json_file, csv_file, org_mapping, clipper_orgs_mapping, excluded_logins, hcap_users_file)
