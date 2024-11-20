import json

with open('backup.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

keys_to_extract = ["Applications", "Groups", "Users", "AuthorizationServers"]

for key in keys_to_extract:
    if key in data:
        with open(f'{key.lower()}.json', 'w', encoding='utf-8') as f:
            json.dump(data[key], f, indent=4)
        print(f"Created {key.lower()}.json with {key} data.")

print("Extraction complete.")