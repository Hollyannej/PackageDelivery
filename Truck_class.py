
# This represents a delivery truck with a specific ID and capacity. The Truck class tracks its current
# load, the packages it carries, its location, and the times it starts and completes its route.

class Truck:
    def __init__(self, truck_id, capacity):
        self.return_time = None
        self.start_time = None
        self.truck_id = truck_id
        self.capacity = capacity
        self.packages = []
        self.load = 0
        self.current_location = 0  # Start at hub (index 0)

    # Updates the truck's current location.
    def update_location(self, new_location):
        self.current_location = new_location

    # Attempts to add a package to the truck's load.
    def add_package(self, package_id):
        if self.load < self.capacity:
            self.packages.append(package_id)
            self.load += 1
        else:
            print(f"Truck {self.truck_id} is full.")

    # Returns the list of package IDs currently loaded on the truck.
    def get_packages(self):
        return self.packages

    #Returns the current number of packages on the truck.
    def get_load(self):
        return self.load