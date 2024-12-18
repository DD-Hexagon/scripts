# Clipper Migration Scripts

## Overview
This repository contains a collection of Python scripts designed to facilitate the migration of data from the Clipper system.

## Purpose
Migrating data from legacy systems like Clipper, convert from JSON to CSV

## Scripts and Their Functions

### 1. **Application Data Processing (`json_to_csv_application.py`)**
- **Purpose**: Processes JSON data related to applications, including authentication flows, admin roles, tenants, and organization names.
- **Input**:
  - `applications.json`: Contains detailed application data.
  - `authorizationservers.json`: Maps application IDs to organization names.
- **Output**: `applications.csv` file with structured application information and consolidated tenant data.

### 2. **User Data Processing (`json_to_csv_user.py`)**
- **Purpose**: Extracts and processes user data, matching it with relevant organization names.
- **Input**:
  - `users.json`: Includes user details such as roles, email, and organization IDs.
  - `authorizationservers.json`: Used to map organization IDs to their respective names.
- **Output**: `users.csv` file containing user details, admin roles, and organization names.

### 3. **Group Data Processing (`json_to_csv_group.py`)**
- **Purpose**: Processes group data and organizes it for use in the new environment.
- **Input**:
  - `groups.json`: Contains data on user groups, including membership and associated details.
- **Output**: `groups.csv` file with structured group data ready for migration.

### 4. **Authorization Server Data Processing (`json_to_csv_orgs.py`)**
- **Purpose**: Extracts information related to authorization servers, including policies, applications, and scopes.
- **Input**:
  - `authorizationservers.json`: Comprehensive data on authorization servers and their configurations.
- **Output**: `auth_servers.csv` file containing processed data on authorization servers and their relationships with applications.

### 5. **Tenant Data Integration (`json_to_csv_tenants.py`)**
- **Purpose**: Matches tenant IDs with their names and integrates this information into application data.
- **Input**:
  - `tenants.json`: Contains tenant details such as names and IDs.
  - `applications.json` and other related files to link tenant data with applications.
- **Output**: CSV files that consolidate application data with relevant tenant names.

## Key Features
- **Comprehensive Data Handling**: The scripts cover applications, users, groups, and authorization servers, ensuring that no data type is left behind in the migration.
- **Customizable Outputs**: Each script is flexible, allowing modifications to meet specific requirements, such as adding or removing columns, changing default values, or adjusting mappings.
- **Error Handling**: The scripts include checks for data inconsistencies, such as `None` values or unexpected types, to prevent errors during processing.
- **Concatenated Data**: For applications and tenants, the scripts can concatenate multiple values into a single column, simplifying data review.

## How to Use the Scripts
1. **Ensure Python is installed** on your system.
2. **Place the necessary input JSON files** in the same directory as the script you wish to run.
3. **Run the script** using:
   ```bash
   python script_name.py
