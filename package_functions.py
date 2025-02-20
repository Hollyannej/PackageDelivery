from Package_class import *
from hash_table_functions import hash_table
from locations_distance_table import *
from dataclasses import dataclass

# This is the third step in my program. It assigns the packages to trucks based a series of criteria.
# This helps the algorithm run smoothly and helps the packages get delivered on time since which truck
# has what package is important.

# Define packages assignments based on special notes function to load the packages on the correct trucks
def assign_packages_based_on_special_notes(hash_table, truck_capacity=16):
    # Create Truck objects
    truck_1 = Truck(1, truck_capacity)
    truck_2 = Truck(2, truck_capacity)
    truck_3 = Truck(3, truck_capacity)

    # Track assigned packages
    assigned_packages = set()

    # Ensure packages 13, 14, 15, 16, 19, and 20 are grouped together on truck 1
    special_packages = [13, 14, 15, 16, 19, 20]

    # Assign special packages to truck 1
    for package_id in special_packages:
        truck_1.add_package(package_id)
        assigned_packages.add(package_id)  # Mark as assigned

    # Ensure packages only loaded on truck 2
    truck_2_only = [3, 18, 32, 36]
    # Assign special packages to truck 2
    for package_id in truck_2_only:
        truck_2.add_package(package_id)
        assigned_packages.add(package_id)  # Mark as assigned

    # Now, assign other packages based on special notes
    for i in range(len(hash_table.table)):
        for key_value in hash_table.table[i]:
            package_id = key_value[0]
            package_data = key_value[1]

            # Skip already assigned packages
            if package_id in assigned_packages:
                continue

            special_note = package_data[6]
            deadline = package_data[4]
            assigned = False

            # Assign packages based on conditions
            if "Can only be on truck 2" in special_note:
                truck_2.add_package(package_id)
                assigned = True
            elif "Delayed on flight---will not arrive to depot until 9:05 am" in special_note:
                truck_2.add_package(package_id)
                assigned = True
            elif "10:30" in deadline:
                truck_1.add_package(package_id)
                assigned = True
            elif "Wrong address listed" in special_note:
                truck_3.add_package(package_id)
                assigned = True

            # Mark the package as assigned if it was added
            if assigned:
                assigned_packages.add(package_id)

    # Finally, assign remaining packages
    for i in range(len(hash_table.table)):
        for key_value in hash_table.table[i]:
            package_id = key_value[0]
            package_data = key_value[1]

            if package_id in assigned_packages:
                continue

            # Assign remaining packages to available trucks
            if truck_1.get_load() < truck_capacity:
                truck_1.add_package(package_id)
            elif truck_2.get_load() < truck_capacity:
                truck_2.add_package(package_id)
            elif truck_3.get_load() < truck_capacity:
                truck_3.add_package(package_id)

            # Mark the package as assigned
            assigned_packages.add(package_id)

    # Debugging: Final truck loads
   # print(f"Truck 1 packages: {truck_1.get_packages()}, Load: {truck_1.get_load()}")
   # print(f"Truck 2 packages: {truck_2.get_packages()}, Load: {truck_2.get_load()}")
   # print(f"Truck 3 packages: {truck_3.get_packages()}, Load: {truck_3.get_load()}")

    # Return the truck objects
    return truck_1, truck_2, truck_3


# Call the function with the default truck capacity
truck_1, truck_2, truck_3 = assign_packages_based_on_special_notes(hash_table)


# After the trucks have their assigned packages, a new dictionary is created to store a
# truncated amount of information for the algorithm. This is where the dictionary is created.
# This is the least amount of data needed per package for the algorithm to run properly:
# the package id, delivery address and address to index.

# Represents information about a delivery package.
@dataclass
class PackageInfo:
    package_id: int
    delivery_address: str
    address_index: int

# List to store populated PackageInfo objects--needed for the nearest neighbor algorithm
package_info_list = []


# Function to populate PackageInfo for a truck's packages
def populate_package_info(truck, package_info_list, package_id_to_address_dict, address_to_index):
    # Get the packages in the desired order
    package_ids = truck.get_packages()

    # Debugging: Print package IDs for verification
   # print(f"Package IDs for Truck {truck.truck_id}: {package_ids}")

    for package_id in package_ids:
        # Get the delivery address for the package
        delivery_address = package_id_to_address_dict.get(package_id)  # Use .get() for safer access

        if delivery_address:  # Check if delivery_address was found
            # Get the address index
            address_index = address_to_index.get(delivery_address)

            if address_index is not None:  # Ensure the address index exists
                # Create PackageInfo instance
                package_info = PackageInfo(package_id=package_id, delivery_address=delivery_address,
                                           address_index=address_index)
                package_info_list.append(package_info)


# Define separate lists to store PackageInfo for each truck
truck_1_package_info = []
truck_2_package_info = []
truck_3_package_info = []


# Populate PackageInfo objects for each truck's packages and store them in separate lists
populate_package_info(truck_1, truck_1_package_info, package_id_to_address_dict, address_to_index)
populate_package_info(truck_2, truck_2_package_info, package_id_to_address_dict, address_to_index)
populate_package_info(truck_3, truck_3_package_info, package_id_to_address_dict, address_to_index)

# Updates the address to index with a new address
def update_address_to_index(address_to_index, old_address, new_address):
    if old_address in address_to_index:
        index = address_to_index.pop(old_address)
        address_to_index[new_address] = index
      #  print(f"Address-to-index mapping updated: {new_address} -> {index}")

# Refreshes the truck package info to update any new data, if needed.
def refresh_truck_package_info(hash_table, truck_package_info):
    refreshed_info = []
    for package_id in truck_package_info:
        package_data = hash_table.lookup(package_id)
        if package_data:
            refreshed_info.append(package_data)
        else:
            print(f"Warning: Package {package_id} not found during refresh.")
    return refreshed_info


#print(f"Truck 1 Package Info: {truck_1_package_info}")
#print(f"Truck 2 Package Info: {truck_2_package_info}")
#print(f"Truck 3 Package Info: {truck_3_package_info}")