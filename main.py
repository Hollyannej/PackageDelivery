from datetime import datetime, timedelta
import time
from hash_table_functions import *
from shared_data import delivery_times
from delivery_functions import *


# Delivery app UI class and methods to simulate the delivery process and manage interactions.
# It's a very simple UI since external libraries aren't allowed.
class DeliveryApp:
    def __init__(self):
        self.simulation_time = datetime.strptime("08:00:00", "%H:%M:%S")  # Initialize the simulation with a start time of 08:00:00
        self.package_ids = []
        self.delivery_in_progress = False  # Deliveries are not ongoing during menu interactions
        self.total_mileage = 0
        self.truck_routes = {}
        self.status_snapshots = {}  # Store package statuses at key times
        self.load_package_ids()
        self.run_delivery_silently()  # Run deliveries once, silently

    # Load all package IDs from the hash table into the list
    def load_package_ids(self):
        self.package_ids = [package_id for package_id in hash_table.keys()]

    # Run the delivery process silently during initialization
    def run_delivery_silently(self):
        start_delivery()  # Execute the delivery process
        check_and_update_package_status(hash_table, delivery_times, self.simulation_time)

        # Calculate routes and mileage after delivery
        self.truck_routes, self.total_mileage = calculate_route_mileage(
            truck_1_package_info,
            truck_2_package_info,
            truck_3_package_info,
            distance_table,
            address_to_index
        )

        # Pre-fetch package statuses at specified times
        self.status_snapshots = check_package_status_every_five_minutes(hash_table, delivery_times, truck_departure_times)

    # Look up the package details based on the given package ID
    def lookup_package(self, package_id):
        if package_id.isdigit():
            package_data = lookup_package(int(package_id), hash_table, delivery_times)
            print(f"Package Data: {package_data}")
        else:
            print("Error: Invalid package ID.")

    # Show package statuses at a specific time
    def show_package_status_at_time(self):
        try:
            input_time = input("Enter a specific time (HH:MM AM/PM): ")
            query_time = datetime.strptime(input_time, "%I:%M %p")
            formatted_time = query_time.strftime("%I:%M %p")

            if formatted_time in self.status_snapshots:
                show_status_at_specific_time(self.status_snapshots, formatted_time)
            else:
                print("No data available for the given time.")
        except ValueError:
            print("Invalid time format. Please use HH:MM.")

    # Display mileage of all trucks
    def show_total_mileage(self):
        print("\n=== Total Mileage ===")
        for truck_id, data in self.truck_routes.items():
            print(f"Truck {truck_id}:")
            print(f"  Mileage: {data['mileage']:.2f} miles")
        print(f"\nTotal Mileage for All Trucks: {self.total_mileage:.2f} miles")


# Function to format the status snapshots into readable text
def format_status_snapshots(status_snapshots):
    for formatted_time, snapshot in status_snapshots.items():
        print(f"\nStatuses at {formatted_time}:")
        for package_id in range(1, 41):
            status = snapshot.get(package_id, "At the hub")
            print(f"Package ID: {package_id} current status: {status}")

# Command-line interface for user interaction
def main():
    app = DeliveryApp()  # Instantiate the DeliveryApp object

    print("\n=== Delivery Simulation ===")

    # Display the main menu to the user
    while True:
        print("\n=== Main Menu ===")
        print("1. Look Up Package Status")
        print("2. Show Package Statuses at a Specific Time")
        print("3. Show Total Mileage for All Trucks")
        print("4. Exit")

        # Get the user's choice
        choice = input("Choose an option: ")

        if choice == '1':  # Look up a package
            package_id = input("Enter Package ID: ")
            app.lookup_package(package_id)
        elif choice == '2':  # Show package statuses at a specific time
            app.show_package_status_at_time()
        elif choice == '3':  # Show total mileage
            app.show_total_mileage()
        elif choice == '4':  # Exit the simulation
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


# Start the main function when the script is run
if __name__ == "__main__":
    main()
