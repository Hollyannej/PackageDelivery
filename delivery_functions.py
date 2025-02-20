from chaining_hash_table_class import *
from Truck_class import *
from hash_table_functions import lookup_package, update_delivery_status, update_delivery_address, \
    package_id_to_address_dict
from package_functions import *
from locations_distance_table import *
from datetime import datetime, timedelta
from shared_data import *
import datetime
from package_functions import *
import time

# Define departure times for each truck
truck_departure_times = {
    1: datetime.strptime("08:00:00", "%I:%M:%S"),
    2: datetime.strptime("09:06:00", "%I:%M:%S"),
    3: datetime.strptime("11:52:20", "%H:%M:%S")
}

# Initialize departure and return times for each truck
start_time = {1: None, 2: None, 3: None}
return_time = {1: None, 2: None, 3: None}

truck_1.start_time = truck_departure_times[1]
truck_2.start_time = truck_departure_times[2]
truck_3.start_time = truck_departure_times[3]

# Updates package status without threading
def update_package_status_synchronously(package_id, new_status, formatted_time):
    # Update the status in the hash table or any other data structure
    #print(f"Package {package_id} has been delivered at {formatted_time}.")
    update_delivery_status(hash_table, package_id, new_status)

# This is the forth step in my program. The nearest neighbor algorithm creates the routes for each truck
# and marks the delivery time. There is a speed factor added in for the simulation that would be removed
# in a real time system that tracked actual trucks.

# Determines the optimal delivery route for a truck using the nearest neighbor algorithm.
def nearest_neighbor(truck_1_package_info, truck_2_package_info, truck_3_package_info, distance_table,
                     address_to_index, truck, truck_id, speed_factor=0.01):
    # NOTE: The current speed factor is set at 10x the normal speed to process it all faster.

    # Start at the hub
    route = [0]  # Hub index
    visited = {0}  # Initialize visited set with the hub
    current_delivery_time = truck.start_time  # Initialize to the truck's start time

    # Create a list to store delivery indices based on PackageInfo
    delivery_indices = []
    package_25_address_index = None  # Store address index for package 25 if found
    for package_info in (truck_1_package_info + truck_2_package_info + truck_3_package_info):
        delivery_address = package_info.delivery_address
        address_index = address_to_index.get(delivery_address)
        if address_index is not None:
            delivery_indices.append((package_info.package_id, address_index))
            if package_info.package_id == 25:
                package_25_address_index = address_index  # Capture the address index for package 25

    delivered_package_ids = []

    # If package 25 is on this truck, deliver it first
    if package_25_address_index is not None:
        route.append(package_25_address_index)
        visited.add(package_25_address_index)
        delivered_package_ids.append(25)
        # Calculate the delivery time for package 25
        distance_to_first_delivery = distance_table[0][package_25_address_index]
        travel_time_hours = distance_to_first_delivery / 18  # Truck speed is 18 mph
        travel_time = timedelta(hours=travel_time_hours)
        current_delivery_time += travel_time
        delivery_times[25] = current_delivery_time

    # Loop until all delivery addresses are visited
    while len(visited) < len(delivery_indices) + 1:
        current_address_index = route[-1]
        # Find nearest unvisited address
        nearest_address = [
            (addr_index, distance_table[current_address_index][addr_index])
            for pkg_id, addr_index in delivery_indices if addr_index not in visited
        ]
        if not nearest_address:
            break  # Exit if no addresses left

        # Select the nearest address based on minimum distance
        nearest_address_index, distance_to_nearest = min(nearest_address, key=lambda x: x[1])
        travel_time_hours = distance_to_nearest / 18  # Truck speed is 18 mph
        travel_time = timedelta(hours=travel_time_hours)

        # Process package deliveries at the nearest address
        for pkg_id, addr_index in delivery_indices:
            if addr_index == nearest_address_index and pkg_id not in delivered_package_ids:
                delivered_package_ids.append(pkg_id)
                if current_delivery_time is None:
                    current_delivery_time = datetime.strptime("08:00:00", "%I:%M:%S")  # Default start time
                delivery_times[pkg_id] = current_delivery_time + travel_time
                current_delivery_time += travel_time

                # Update the package status after delivery
                check_and_update_package_status(hash_table, delivery_times, start_time)

                if not (truck_1_package_info or truck_2_package_info or truck_3_package_info):
                    print("No packages to deliver.")
                    return [], []  # Return empty lists if no packages

        # Update the route and visited addresses
        route.append(nearest_address_index)
        visited.add(nearest_address_index)


        # Introduce a real-time delay for each step to match the simulation clock
        # Calculate the simulation time elapsed (5 minutes per real-world second)
        elapsed_simulation_time = (current_delivery_time - truck_departure_times[truck_id]).total_seconds() / 60
        elapsed_real_time = elapsed_simulation_time / 5 # 1 real second = 5 simulated minutes
        time.sleep(elapsed_real_time * speed_factor)  # Adjusted delay with speed factor

    # Return to the hub and calculate return time
    route.append(0)
    return_distance = distance_table[nearest_address_index][0]
    return_travel_time_hours = return_distance / 18
    return_travel_time = timedelta(hours=return_travel_time_hours)
    return_time[truck.truck_id] = current_delivery_time + return_travel_time

   # print(f"Truck {truck.truck_id} returned to the hub at {return_time[truck.truck_id].strftime('%I:%M:%S')}")
  #  print(delivered_package_ids)
    return delivered_package_ids, route


# Wrapper functions for running the nearest neighbor algorithm for each truck on their own
def nearest_neighbor_truck_1(truck_1_package_info, distance_table, address_to_index, truck_id=1):
    delivered_package_ids, route = nearest_neighbor(truck_1_package_info, [], [], distance_table,
                                                    address_to_index, truck_1, truck_id=1)
    return delivered_package_ids, route  # Return both values

def nearest_neighbor_truck_2(truck_2_package_info, distance_table, address_to_index, truck_id=2):
    delivered_package_ids, route = nearest_neighbor([], truck_2_package_info, [], distance_table,
                                                    address_to_index, truck_2, truck_id=2)
    return delivered_package_ids, route  # Return both values

def nearest_neighbor_truck_3(truck_3_package_info, distance_table, address_to_index, truck_id=3):
    delivered_package_ids, route = nearest_neighbor([], [], truck_3_package_info, distance_table,
                                                    address_to_index, truck_3, truck_id=3)
    return delivered_package_ids, route  # Return both values


# Flag indicating whether all deliveries are complete
delivery_complete = False

# Checks if all packages have been marked as delivered
def all_packages_delivered(delivery_times, total_packages=40):
    """Check if all packages are marked as delivered."""
    return len(delivery_times) == total_packages


#This is the fifth part of the program. It starts the delivery process for each truck.
# It also calls the function that updates the delivery status for each package.
# It manages the start and execution of the delivery process, including setting start times for trucks,
# initiating deliveries, and starting Truck 3 after Trucks 1 or 2 return to the hub.
def start_delivery():
    global delivery_complete

    # Initialize truck start times at 8 AM for Truck 1 and 9:06 AM Truck 2
    # Truck 2 has a delayed start because some of the packages on it do not arrive until 9:05 AM.
    start_time[1] = datetime.strptime("08:00:00", "%I:%M:%S")
    start_time[2] = datetime.strptime("09:06:00", "%I:%M:%S")
    truck_1.start_time = start_time[1]
    truck_2.start_time = start_time[2]

  #  print(f"Truck 1 departs at {truck_1.start_time.strftime('%H:%M:%S')}.")
  #  print(f"Truck 2 departs at {truck_2.start_time.strftime('%H:%M:%S')}.")

    # Start Truck 1 delivery process
    nearest_neighbor_truck_1(truck_1_package_info, distance_table, address_to_index)

    # Start Truck 2 delivery process
    nearest_neighbor_truck_2(truck_2_package_info, distance_table, address_to_index)

    # Truck 3 departs after Truck 1 or Truck 2 return
    if return_time[1] or return_time[2]:
        start_time[3] = max(return_time[1], return_time[2])
        truck_3.start_time = start_time[3]
     #   print(f"Truck 3 departs at {truck_3.start_time.strftime('%H:%M:%S')}.")
        # Change wrong address for package 9 to correct address. Truck 3 doesn't leave until 11:52:20 pm
        # so there is time to change the address and update the route before then since the algorithm is
        # called after the address update.
        package_id = 9
        old_address = "300 State St"
        new_address = "410 S. State St"

       # print(f"Updating Package {package_id} address to {new_address}.")

        # Update hash table
        update_delivery_address(hash_table, package_id, new_address)

        # Update address-to-index mapping
        update_address_to_index(address_to_index, old_address, new_address)

        # Update package_id_to_address_dict
        package_id_to_address_dict[package_id] = new_address

        # Check if Package 9 is updated in the hash table
       # package_9_data = hash_table.search(package_id)
       # print(f"Package {package_id} data in hash table: {package_9_data}")

        # Refresh Truck 3 package info
        truck_3_package_info = []
        populate_package_info(truck_3, truck_3_package_info, package_id_to_address_dict, address_to_index)

        # Verify the updated package info
        #print(f"Updated Truck 3 Package Info: {truck_3_package_info}")

        # Start Truck 3 delivery process
        nearest_neighbor_truck_3(truck_3_package_info, distance_table, address_to_index)
        #print(f"Truck 3 returns at {return_time[3].strftime('%H:%M:%S')}.")

        # Check and record package statuses at specified times
   # status_snapshots = check_package_status_every_five_minutes(hash_table, delivery_times, truck_departure_times)
   # format_status_snapshots(status_snapshots)

    # Final check to confirm all packages are delivered
    check_and_update_package_status(hash_table, delivery_times, start_time)



# Checks the delivery status of each package, updates it in the hash table, and prints delivery updates.
def check_and_update_package_status(hash_table, delivery_times, start_time):
    package_ids = hash_table.keys()
    global delivery_complete

    # Exit if delivery process is already complete
    if delivery_complete:
        return

    for package_id in package_ids:
        # Retrieve package data from the hash table
        package_data = hash_table.search(package_id)
        if package_data is None:
            print(f"Package ID {package_id} not found in hash table. Skipping.")
            continue  # Skip to the next package if it's not found

        # Check if the package has a recorded delivery time
        if package_id in delivery_times:
            delivery_time = delivery_times[package_id]  # Get the delivery datetime
            formatted_time = delivery_time.strftime("%I:%M:%S %p")  # Format the delivery time
            new_status = "Delivered at " + formatted_time
            update_package_status_synchronously(package_id, new_status, formatted_time)
        else:
            assigned_truck = None
            for truck_info, truck_id in [(truck_1_package_info, 1), (truck_2_package_info, 2),
                                         (truck_3_package_info, 3)]:
                for pkg in truck_info:
                    if pkg.package_id == package_id:
                        assigned_truck = truck_id
                        break

                if assigned_truck is not None:
                    break

            truck_departure_time = start_time.get(assigned_truck)
            if truck_departure_time is None:
                new_status = 'At the hub'
              #  print(f"Package {package_id} is at the hub.")
            else:
                new_status = 'En route'
             #   print(f"Package {package_id} is en route.")

            # Update package status synchronously
            update_package_status_synchronously(package_id, new_status, "")

    if all_packages_delivered(delivery_times):
        delivery_complete = True
       # print("All packages have been delivered.")


#check_and_update_package_status(hash_table, delivery_times, start_time, package_assignments)

# Dictionary to store package statuses at specific times.
# This simulates an actual real time delivery process by creating status updates for all packages
# during the entire delivery.
status_snapshots = {}


# Function to check status every minute from 8:00 AM to 1:27 PM and save the information to a dictionary
def check_package_status_every_five_minutes(hash_table, delivery_times, truck_departure_times, verbose=True):
    # Starting and ending times for snapshots
    snapshot_start_time = datetime.strptime("08:00:00", "%I:%M:%S")
    end_time = datetime.strptime("13:27:00",
                                 "%H:%M:%S")  # Simulation ends at this time so no further snapshots are needed
    interval = timedelta(minutes=1)

    # Generate snapshot times at every 1-minute interval
    snapshot_time = snapshot_start_time
    status_snapshots = {}

    while snapshot_time <= end_time:
        status_at_time = {}

        # Capture status of each package at the snapshot time
        for package_id in hash_table.keys():
            # Retrieve package info as a tuple using the appropriate method
            package_info = hash_table.search(package_id)  # Use the get method for ChainingHashTable

            # Ensure package_info is not None before trying to access its elements
            if package_info is None:
                continue
            address = package_info[0]  # Address is at index 0
            deadline = package_info[4]  # Deadline is at index 4

            # Loop through package IDs and check if they were delivered or are still in transit
            if package_id in delivery_times and delivery_times[package_id] <= snapshot_time:
                # If the package is delivered, reflect the status as delivered
                status = f"Delivered at {delivery_times[package_id].strftime('%I:%M %p')}"

                # Preserve the original truck assignment (do NOT reset assigned_truck)
                for truck_info, truck_id in [(truck_1_package_info, 1), (truck_2_package_info, 2),
                                             (truck_3_package_info, 3)]:
                    if any(pkg.package_id == package_id for pkg in truck_info):
                        assigned_truck = truck_id
                        break
            else:
                # Determine the original truck assigned to the package (static assignment)
                assigned_truck = None
                for truck_info, truck_id in [(truck_1_package_info, 1), (truck_2_package_info, 2),
                                             (truck_3_package_info, 3)]:
                    for pkg in truck_info:
                        if pkg.package_id == package_id:
                            assigned_truck = truck_id
                            break
                    if assigned_truck:
                        break

                # If no truck was found, the package is still at the hub
                if assigned_truck is None:
                    status = "At the hub"
                else:
                    # Check the truck's departure time
                    truck_departure_time = truck_departure_times.get(assigned_truck)
                    if not truck_departure_time or truck_departure_time > snapshot_time:
                        status = 'At the hub'
                    else:
                        status = 'En route'

            # Print or store the status of each package
          #  print(f"Package {package_id} Status: {status}")

            # Include truck number, address, and deadline in the status
            status_at_time[package_id] = {
                "status": status,
                "truck_number": assigned_truck,  # Correctly assign the truck number
                "address": address,
                "deadline": deadline
            }

        # Store the snapshot in status_snapshots
        status_snapshots[snapshot_time.strftime("%I:%M %p")] = status_at_time
        snapshot_time += interval

    return status_snapshots


# Function to format the status snapshots into readable text
def format_status_snapshots(status_snapshots):
    # Loop through each recorded snapshot time and print statuses
    for formatted_time, snapshot in status_snapshots.items():
        print(f"\nStatuses at {formatted_time}:")

        # Iterate through all package IDs in the snapshot
        for package_id, details in snapshot.items():
            # Extract information from the snapshot details
            status = details.get("status", "Unknown")
            truck_number = details.get("truck_number", "Unknown")
            address = details.get("address", "Unknown")
            deadline = details.get("deadline", "No deadline")

            # Print the formatted details for the current package
            print(f"Package ID: {package_id}")
            print(f"  Current Status: {status}")
            print(f"  Truck Number: {truck_number}")
            print(f"  Delivery Address: {address}")
            print(f"  Deadline: {deadline}")
            print()  # Blank line for readability


# Example call
#format_status_snapshots(status_snapshots)

# Function to show only status updates from a specific time that the user inputs.
# The status updates are taken from the status snapshot dictionary.
def show_status_at_specific_time(status_snapshots, query_time_str):
    try:
        # Convert the query string to a datetime object to match the snapshot format
        query_time = datetime.strptime(query_time_str, "%I:%M %p")  # Parse input with AM/PM
        formatted_query_time = query_time.strftime("%I:%M %p")      # Reformat to match snapshot keys

        # Fetch the corresponding snapshot
        snapshot = status_snapshots.get(formatted_query_time)

        if snapshot:
            print(f"\nStatuses at {formatted_query_time}:")
            for package_id in range(1, 41):
                status = snapshot.get(package_id, "At the hub")
                print(f"Package ID: {package_id} current status: {status}")
        else:
            print(f"No data available for {formatted_query_time}. Please choose a valid time within the simulation range.")
    except ValueError:
        print("Invalid time format. Please use HH:MM AM/PM.")

# Calculates the total mileage traveled by all trucks in a delivery route
# and provides individual mileage and route details for each truck.
def calculate_route_mileage(truck_1_package_info, truck_2_package_info, truck_3_package_info, distance_table, address_to_index):
    # Initialize total mileage
    total_mileage = 0.0
    route_data = {}

    # Get and calculate mileage for Truck 1
    _, route_1 = nearest_neighbor_truck_1(truck_1_package_info, distance_table, address_to_index)
    mileage_truck_1 = 0.0
    for i in range(len(route_1) - 1):
        mileage_truck_1 += distance_table[route_1[i]][route_1[i + 1]]
    route_data[1] = {'route': route_1, 'mileage': mileage_truck_1}
    total_mileage += mileage_truck_1

    # Get and calculate mileage for Truck 2
    _, route_2 = nearest_neighbor_truck_2(truck_2_package_info, distance_table, address_to_index)
    mileage_truck_2 = 0.0
    for i in range(len(route_2) - 1):
        mileage_truck_2 += distance_table[route_2[i]][route_2[i + 1]]
    route_data[2] = {'route': route_2, 'mileage': mileage_truck_2}
    total_mileage += mileage_truck_2

    # Get and calculate mileage for Truck 3
    _, route_3 = nearest_neighbor_truck_3(truck_3_package_info, distance_table, address_to_index)
    mileage_truck_3 = 0.0
    for i in range(len(route_3) - 1):
        mileage_truck_3 += distance_table[route_3[i]][route_3[i + 1]]
    route_data[3] = {'route': route_3, 'mileage': mileage_truck_3}
    total_mileage += mileage_truck_3

    return route_data, total_mileage

route_data, total_mileage = calculate_route_mileage(truck_1_package_info, truck_2_package_info, truck_3_package_info,
    distance_table, address_to_index)


#print("Route data for each truck:")
#for truck_id, data in route_data.items():
 #   print(f"\nTruck {truck_id} route:")
  #  print(f"Route: {data['route']}")
   # print(f"Mileage: {data['mileage']} miles")

#print(f"\nTotal mileage for all trucks: {total_mileage} miles")



#def main():
 #   print("Starting delivery...")

    # Start the delivery process
  #  start_delivery()  # Pass the screenshot times to the function

   # print(hash_table.search(9))

    # Test searching for a package
    #package_id_to_search = 9
    #package_data = hash_table.search(package_id_to_search)
    #print(f"Package {package_id_to_search}: {package_data}")





# Run the main function
#if __name__ == "__main__":
 #   main()