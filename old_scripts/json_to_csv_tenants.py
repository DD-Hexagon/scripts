import csv
import json

# Load the tenant data from the JSON file
with open('Clipper Dev ring Tenant list 1.json', 'r') as file:
    tenant_data = json.load(file)

# Load the organization data from the JSON file
with open('Clipper Dev ring Org list 1.json', 'r') as file:
    org_data = json.load(file)

# Create a dictionary to map organization IDs to organization names
org_dict = {org['Id']: org['Name'] for org in org_data}

columns = [
    "Tenant ID","Name", "Description", "Organization", "Product", "Product Version",
    "Hosting Group", "Type", "Production", "Golden Tenant", "Demo Tenant",
    "Note", "Provision Status", "Subscription End Date"
]

with open('tenants.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()

    for tenant in tenant_data:
        region = tenant.get("Region", "")
        hosting_group = ""
        if region == "Central US":
            hosting_group = "Azure-HXGN-Sandbox-CUS"
        if region == "West Europe":
            hosting_group = "Azure-HXGN-Sandbox-WEU"
        if region == "Southeast Asia":
            hosting_group = "Azure-HXGN-Sandbox-SA"
        if region == "UAE North":
            hosting_group = "Azure-HXGN-Sandbox-UAE"

        # Get the organization name using the organization ID from the tenant data
        organization_id = tenant.get("OrganizationId", "")
        organization_name = org_dict.get(organization_id, "Unknown Organization")

        csv_row = {
            "Tenant ID": tenant.get("Id", ""), 
            "Name": tenant.get("Name", ""),
            "Description": tenant.get("Description", ""),
            "Organization": organization_name,
            "Product": "SDx MT Cloud",
            "Product Version": "1",
            "Hosting Group": hosting_group,
            "Type": "",           
            "Production": "True",
            "Golden Tenant": "FALSE",
            "Demo Tenant": "FALSE",
            "Note": "",
            "Provision Status": "ACTIVE",
            "Subscription End Date": ""
        }
        writer.writerow(csv_row)