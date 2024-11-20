import csv
import json

def process_json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        grp_data = json.load(file)

    if isinstance(grp_data, dict):
        grp_data = [grp_data]  

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

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writeheader()

        for item in grp_data:
            if isinstance(item, dict):
                applications = ','.join(item.get("ApplicationIds", [])) if item.get("ApplicationIds") else ""
                users = ','.join(item.get("UserIds", [])) if item.get("UserIds") else ""

                csv_row = {
                    "Name": item.get("Name", ""),
                    "Description": item.get("Description", ""),
                    "Group ID": item.get("Id", ""),
                    "Process Status": item.get("ProcessStatus", "DONE"),
                    "IDP Status": item.get("IDPStatus", "ACTIVE"),
                    "Organization": item.get("OrganizationId", ""),
                    "User": users,
                    "Application": applications,
                }

                writer.writerow(csv_row)

json_file = 'groups.json'
csv_file = 'groups.csv'
process_json_to_csv(json_file, csv_file)
