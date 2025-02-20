C950 Task-1 WGUPS Algorithm Overview

(Task-1: The planning phase of the WGUPS Routing Program)


Holly Johnson
ID #010844848
WGU Email: hjoh554@wgu.edu
Date 10/03/2024

C950 Data Structures and Algorithms II

Introduction
For this project, I need to figure out the best way to deliver 40 packages in under 140 minutes around Salt Lake City. This is my planning document to explain my ideas and thought process. 
A. Algorithm Identification
I’m going to use a greedy algorithm that will pick the closest address for each proceeding step to deliver all of the packages in a timely manner. 
B. Data Structure Identification
I will store the data in a hash table. It accounts for the relationship between the data components I am storing by making the Package ID the key since it is unique to each package, and the value will be the distance from the main hub.
B1. Explanation of Data Structure
According to Zybooks Data Structures and Algorithms: “is a data structure that stores unordered items by mapping (or hashing) each item to a location in an array (or vector).” Each item is mapped to a table using a key, which should be unique for the most efficiency, though that is not always the case. 
A bucket is where the data is stored in the hash table and is found using a hash function. In many cases, that’s done using a modulo operator %, and the remainder is left after dividing the number by a specific value. For example, if the hash table has ten buckets, the modulo operator % will be 10. Therefore, if an item has a key item value of 21, you find the bucket by 21 % 10 = 1. Since 21 / 10 is 2 with a remainder of 1.

C1. Algorithm’s Logic
My Pseudocode is: 
// Function to determine the optimal route using a hash table for storing addresses.
function next_address(addresses):
    // Initialize the starting point for the first address on the list.
    start_address = addresses[0]
    
    // Create a hash table for unvisited addresses.
    unvisited = {address: coordinates for address in addresses if address != start_address}
    
    // Initialize the route with the start address.
    route = [start_address]
    
    // Set the current address to the starting address.
    current_address = start_address
    
    // Continue until all addresses have been visited.
    while unvisited is not empty:

        //Use the hash table to Find the nearest unvisited address from the current address.
        nearest_address = find_nearest_address(current_address, unvisited)
        
        // Add the nearest address to the route.
        route.append(nearest_address)
        
        // Remove the nearest address from the hash table of unvisited addresses.
        unvisited.remove(nearest_address)
        
        // Set the current address to the nearest address found.
        current_address = nearest_address
    
    // After visiting all addresses, return to the starting address to complete the route.
    route.append(start_address)
    
    // Return the complete route.
    return route

C2. Development Environment
I will be using PyCharm on an iMac desktop computer running MacOS 13.6.7. The version of Python I am using is 3.10 with the Anaconda 3 interpreter. 
C3. Space and Time complexity using Big-O notation
Time Complexity
The creation of the hash table has a time complexity of O(n) with n the number of addresses visited since it must iterate through the entire list.
The main loop has a time complexity of O(n) since it runs through the hash table each time and removes one address on each pass. 
Finding the nearest address function has an O(n) time complexity since it runs through the loop of addresses and compares them to the current address.
Updating the route and hashtable has a time complexity of O(1) since both actions take a set amount of time that does not change. 
The total time complexity of the algorithm is O(n^2) since it must iterate through the remaining addresses in the hash table on each subsequent loop. For example, there are initially n - 1 addresses on the list (n = number of addresses minus one for the starting address). Since an address is removed from the list on each iteration, the second loop runs over n - 2, the third over n - 3, and so on until the hash table is empty. 
If you calculate all the above complexities, it looks like this: 
O(n) + O(n-1) + O(n-2) + O(n-3) +…+ O(n) = O(n^2)
Space Complexity
The space complexity of the address list is O(n) since n is the number of addresses on the list. 
The start_address has a space complexity of O(1) since there is one address on that list. 
The hast table used to store the addresses has a space complexity of O(n) since there are n addresses on the list. 
The route list has a space complexity of O(n) as well since the list starts with one address and includes them all by the end of the program. 
The current_address and nearest_ address both have space complexities of O(1) since they hold one address each. 
The rest of the code doesn’t have input that increases or decreases in size, so it has a space complexity of O(1).
Overall, the space complexity of the entire code is O(n) since the three data structures in the code all grow with n.
C4. Scalability and Adaptability
Since the time complexity is quadratic, the data directly affects the number of operations the algorithm needs to run. However, unless the scale of the packages went into the high hundreds and above, the greedy algorithm is still suitable enough. It should perform well for packages up into the 300 to 400 range. 
The adaptability of the current greedy algorithm is about the same. As the number of packages grows, it would need to be modified to account for dynamic changes in the data (like a last-minute delivery note). However, a data set in the 300 to 400 range should work well.
C5. Software Efficiency and Maintainability 
This software design would be efficient and easy to maintain because of the following: 
The hash table is used for both looking up addresses and removing them, which means finding the next address is quick and helps improve performance. 
Removing the addresses reduces the size of the problem by n - 1, therefore making it more efficient. 
The software’s helper functions are modular and keep the main function clean, making it easier to understand and maintain since you can change the helper functions without touching the main algorithm.
The code’s construction allows for scalability, such as adding new requirements, without disrupting the main algorithm. For example, I can add a new helper function for different routing strategies and special package handling while the base code remains untouched.
C6. Self-Adjusting Data Structures 
According to ‘Applications, Advantages, and Disadvantages of Hash Data Structure’ on the Geeks for Geeks website, the strengths of hash tables are: 
They make it fast to look up data since the hash function maps keys to an index. 
They are efficient at both inserting data and removing it since they only need the key of the index. 
They are space-efficient since they only store key-value pairs. 
They are flexible since they can store all types of data, from strings to ints. 
They have ways to resolve collisions built in, such as chaining. 
According to ‘Applications, Advantages, and Disadvantages of Hash Data Structure’ on the Geeks for Geeks website, the weaknesses of hash tables are:
They can be inefficient if there are many keys that fit in the same index, thus increasing collisions. 
With a large amount of data, collisions are not avoidable since there will be many keys.
They have a set capacity and can fill up. 
Since they use a hash function, the order of elements isn’t maintained, and this creates issues if you need to get data in a specific order. 
C7. Data Key
The key for my hash table is the package ID since it is unique to each package and should make it easier and quicker to search the hash table. The only other item on the list that is unique is the delivery address, but it’s longer than the package ID. The other options, like delivery city, zip code, and package weight, would cause far too many collisions to be efficient. 

D. Sources

Lysecky, R., & Vahid, F. (2018, June). C950: Data Structures and Algorithms II. zyBooks.
Retrieved October 2024, from https://learn.zybooks.com/zybook/WGUC950Template2023/chapter/6/section/1
GeeksforGeeks. (2023, March). Applications, Advantages, and 			Disadvantages of Hash Data Structure. https://www.geeksforgeeks.org/applications-advantages-and-disadvantages-of-hash-data-structure/
E. Professional Communication
Nothing to write. Run your document through https://www.grammarly.com/ 
