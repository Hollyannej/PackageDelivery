import csv
from chaining_hash_table_class import ChainingHashTable
import time
from shared_data import delivery_times



#This is the next step in my program. The CSV file is inserted into the hash table
 #and the various functions are created to search, update and extract data from the hash table for
 #program functionality.

# Function to load data from CSV and insert into the hash table
def load_data_into_hash_table(csv_filename, hash_table):
    try:
        with open(csv_filename, mode='r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                package_id = int(row['Package ID'].strip())
                package_data = (
                    row['Delivery Address'].strip(),
                    row['Delivery City'].strip(),
                    row['Delivery State'].strip(),
                    row['Delivery Zip'].strip(),
                    row['Delivery Deadline'].strip(),
                    row['Weight'].strip(),
                    row['Notes'].strip(),
                    row['Delivery Status'].strip()
                )
                hash_table.insert(package_id, package_data)
    except FileNotFoundError:
        print(f"Error: The file {csv_filename} was not found.")
    except Exception as e:
        print(f"An error occurred while loading data: {e}")

# Lookup function to return package details
def lookup_package(package_id, hash_table, delivery_times):
    package_data = hash_table.search(package_id)

    if package_data:
        delivery_address, delivery_city, delivery_state, delivery_zip, deadline, weight, notes, status = package_data

        # Determine delivery time based on status and delivery_times dictionary
        if status == "Delivered" and package_id in delivery_times:
            delivery_time = delivery_times[package_id]
            formatted_time = delivery_time.strftime("%I:%M:%S %p")  # Format the delivery time
            delivery_time = "Delivered at " + formatted_time
        elif status == "En route":
            delivery_time = "En route"
        else :
            delivery_time = "At the hub"


        return f"""
        Package ID: {package_id}
        Delivery Address: {delivery_address}
        City: {delivery_city}, {delivery_state}
        Zip Code: {delivery_zip}
        Delivery Deadline: {deadline}
        Package Weight: {weight} lbs
        Notes: {notes}
        Delivery Status: {status}

        """
    else:
        return f"Package ID {package_id} not found."

# Updates delivery status in hash table
def update_delivery_status(hash_table, package_id, new_status):
    # Retrieve current package data from hash table
    package_data = hash_table.search(package_id)

    if package_data:
        # Update the delivery status in the package data
        updated_package_data = package_data[:-1] + (new_status,)

        # Re-insert the updated package data into the hash table
        hash_table.insert(package_id, updated_package_data)
       # print(f"Package ID {package_id} updated to status '{new_status}'")


# Updates delivery address in hash table
def update_delivery_address(hash_table, package_id, new_address):
    # Retrieve current package data from hash table
    package_data = hash_table.search(package_id)

    if package_data:
        # Convert package data to a list for mutation
        updated_package_data = list(package_data)
        # Replace the delivery address (assuming it's the first element)
        updated_package_data[0] = new_address
        # Re-insert the updated package back into the hash table
        hash_table.insert(package_id, tuple(updated_package_data))
       # print(f"Package {package_id} updated in hash table: {updated_package_data}")
    else:
        print(f"Package {package_id} not found in hash table.")


# Function to populate the address_to_package_id dictionary--needed for the nearest neighbor algorithm
def populate_address_to_package_id(hash_table):
    address_to_package_id = {}
    for bucket in hash_table.table:
        if bucket:  # Check if the bucket has entries
            for package_id, package_data in bucket:
                address = package_data[0]  # Extract the address from package data

                # If the address is already in the dictionary, append the package ID to the list
                if address in address_to_package_id:
                    address_to_package_id[address].append(package_id)
                else:
                    # Otherwise, create a new list for this address
                    address_to_package_id[address] = [package_id]
    return address_to_package_id


# Function to populate the package_id_to_address dictionary--needed for the nearest neighbor algorithm
def populate_package_id_to_address(hash_table):
    package_id_to_address = {}

    for bucket in hash_table.table:
        if bucket:  # Check if the bucket has entries
            for package_id, package_data in bucket:
                address = package_data[0]  # Extract the address from package data
                package_id_to_address[package_id] = address  # Map package_id to address

    return package_id_to_address


# Create hash table from ChainingHashTable
hash_table = ChainingHashTable()

# Load data from CSV into the hash table
csv_filename = '../pythonProjectnew/WGUPS Package File.csv'
load_data_into_hash_table(csv_filename, hash_table)

# Lookup package by ID
package_id = 9  # Example package ID
#print(lookup_package(package_id, hash_table, delivery_times))


# Populate a dictionary mapping addresses to package IDs
address_to_package_id_dict = populate_address_to_package_id(hash_table)
#print(address_to_package_id_dict)

# Populate a dictionary mapping package IDs to addresses
package_id_to_address_dict = populate_package_id_to_address(hash_table)
#print(package_id_to_address_dict)


# Test searching for a package
#package_id_to_search = 9
#package_data = hash_table.search(package_id_to_search)
#print(f"Package {package_id_to_search}: {package_data}")
