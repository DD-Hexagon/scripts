import csv
import json

# Define the columns for the CSV
columns = [
    "Organization ID", "Name", "Description", "External IDP ID", "Alias", "Type", "Active",
    "IsHexagon", "Provision Status"
]

# Load the data from the JSON file
with open('Clipper Dev ring Org list 1.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Open the CSV file to write data
with open('orgs.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=columns)
    writer.writeheader()

    # Loop through each organization in the data
    for org in data:
        csv_row = {
            "Organization ID": org.get("Id", ""),
            "Name": org.get("Name", ""),
            "Description": org.get("Description", ""),
            "External IDP ID": org.get("Id", ""),
            "Alias": "",  # Assuming this field may require additional info
            "Type": "Paying Customer",  # Static value as requested
            "Active": "Yes" if org.get("IsActive", False) else "No",
            "IsHexagon": "No",  # Static value as requested
            #"Provision Status": "ACTIVE" if org.get("IsActive", False) else "INACTIVE",
            "Provision Status": "ACTIVE",
        }
        writer.writerow(csv_row)