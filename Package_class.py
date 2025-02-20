from chaining_hash_table_class import *
from Truck_class import *
from datetime import datetime, timedelta

from hash_table_functions import package_id_to_address_dict
from package_functions import *
from locations_distance_table import *

# Represents information about a delivery package.
class PackageInfo:
    def __init__(self, package_id: int, delivery_address: str, address_index: int):
        self.package_id = package_id
        self.delivery_address = delivery_address
        self.address_index = address_index

    def __repr__(self):
        return f"PackageInfo(package_id={self.package_id}, delivery_address={self.delivery_address}, address_index={self.address_index})"

    def __eq__(self, other):
        if isinstance(other, PackageInfo):
            return (self.package_id == other.package_id and
                    self.delivery_address == other.delivery_address and
                    self.address_index == other.address_index)
        return False


# List to store populated PackageInfo objects--needed for the nearest neighbor algorithm
package_info_list = []

# Populate the PackageInfo instances
for package_id, delivery_address in package_id_to_address_dict.items():
    if delivery_address in address_to_index:
        address_index = address_to_index[delivery_address]
        package_info = PackageInfo(package_id=package_id, delivery_address=delivery_address, address_index=address_index)
        package_info_list.append(package_info)

# Display the populated list of PackageInfo objects
# for info in package_info_list:
#    print(info)
