#Student ID: 013116778

#import the package and hash_table files for use
from package import Package
from hash_table import HashTable
from datetime import datetime, timedelta

#create empty package hash table
package_table = HashTable()

#define start time as earliest time of delivery possible
start_time = datetime.strptime("08:00 AM", "%I:%M %p")

#open the CSV file "WGUPS Package File.csv"
with open("WGUPS Package File.csv",
          encoding="utf-8-sig") as package_file:
    for line in package_file:
        package_data = line.strip().split(",") #remove whitespace from the ends & split at the commas

        #validate line being parsed actually includes package data (beings with package_id integer)
        try:
            package_id = int(package_data[0])
        except ValueError:
            continue

        #assign available time
        #assign delays via notes section of CSV
        if "Delayed" in package_data[7]:
           available_time = datetime.strptime(
               package_data[7].split("until ")[1],
               "%I:%M %p"
           )
        #code for any packages that need special delays
        elif package_data[0] == "9":
            available_time = datetime.strptime(
                "10:20 AM",
                "%I:%M %p")
        else:
            available_time = start_time

        #initialize corrector variables
        corrected_address = None
        corrected_city = None
        corrected_state = None
        corrected_zip = None

        deadline = package_data[5]

        if deadline != "EOD":
            deadline = datetime.strptime(deadline, "%I:%M %p")

        #load correct address information for any uniquely incorrect addresses
        if package_data[0] == "9":
            corrected_address = "410 S State St"
            corrected_city = "Salt Lake City"
            corrected_state = "UT"
            corrected_zip = "84111"

        #create Package object with delimited package data and starter values for load time, delivery time, and status
        package = Package(
            int(package_data[0]),
            package_data[1],
            package_data[2],
            package_data[3],
            package_data[4],
            deadline,
            package_data[6],
            package_data[7],
            None,
            None,
            available_time,
            "at the hub",
            corrected_address,
            corrected_city,
            corrected_state,
            corrected_zip)

        #save the package data to the hash table
        package_table.put(package)

    #test available_time assignment for delayed and non-delayed package
    #print(package_table.lookup(6))
    #print(package_table.lookup(7))

#to test Package object loading / creation
#print(package_table)
#print(package_table.lookup(14))

#create empty distance list
distance_data = []
start_line = False
distance_row = 0
distance_dict = {}
dict_counter = 1

#read in the distance CSV file, and parse the data
with open("WGUPS Distance Table.csv",
          encoding="utf-8-sig") as distance_file:
    previous_line = []
    for line in distance_file:
        distance_input = line.strip().split(",")

        #start reading at HUB row of file
        if len(distance_input) > 2 and "HUB" in distance_input[2]:
            hub_address = previous_line[0].strip('"')    #capture hub address
            distance_dict[hub_address] = 0               #initialize dictionary with hub address & key 0
            start_line = True

        if start_line:
            #print(distance_input) #to test distance_input data load
            distance_row += 1

            #append data to distance_data list only if distance data element (floatable)
            if distance_row % 3 == 1:
                distance_row_data = []

                #beginning with the second element to skip the zip
                for distance in distance_input[1:]:
                    #skips all non-float values, and empty strings
                    try:
                        (float(distance))
                    except ValueError:
                        continue

                    distance_row_data.append(float(distance))
                distance_data.append(distance_row_data)

#to test distance list load
#print(distance_data)

            #create dictionary for mapping between addresses and distance list & extract address portion of distance info only
            if distance_row % 3 == 0:
                address_data = distance_input[0].strip('"') #removes trailing double quotation mark from the file

                if address_data == "3575 W Valley Central Sta bus Loop":
                    address_data = "3575 W Valley Central Station bus Loop"

                distance_dict[address_data] = dict_counter #adds address to dictionary and assigns incrementing dictionary key
                dict_counter += 1 #increments for key assignment

        previous_line = distance_input

#test dictionary loading
#(distance_dict)

#test distance mapping
#print(distance_data[17][4])

#test dictionary lookup
#print(distance_dict["195 W Oakland Ave"])

#assign package ids to trucks
truck_1 = [7, 13, 14, 15, 16, 19, 20, 21, 27, 34, 39, 40]
truck_2 = [1, 3, 6, 10, 11, 12, 18, 25, 26, 29, 30, 31, 36, 37, 38]
truck_3 = [2, 4, 5, 8, 9, 17, 22, 23, 24, 28, 32, 33, 35]

#copy to preserve original list for printing Truck numbers in interface
truck_1_packages = truck_1.copy()
truck_2_packages = truck_2.copy()
truck_3_packages = truck_3.copy()

#distance retrieval code from distance_data; ensures larger index is retrieved first for matrix
def get_distance(start_index, end_index):
    if start_index > end_index:
        return distance_data[start_index][end_index]
    else:
        return distance_data[end_index][start_index]

#test distance retrieval
#print(get_distance(0, 1))
#print(get_distance(4, 2))
#print(get_distance(1, 17))

def deliver_packages(truck,start_time):
    current_location = 0
    dist_traveled = 0
    total_mileage = 0

    if isinstance(start_time, str):
        start_time = datetime.strptime(start_time, "%I:%M %p")

    current_time = start_time

   #find the next undelivered package on the truck with the closest destination
    for package_id in truck:
        package = package_table.lookup(package_id)
        package.loading_time = current_time

    #repeat loop while there are still packages left to be delivered on the truck
    while truck:

        #initialize tracker variables
        next_stop = None
        next_stop_address = None
        shortest_distance = float("inf")
        shortest_time_until_deadline = float("inf")

        for package_id in truck:
            package = package_table.lookup(package_id)

            #package 9 address correction
            if package.package_id == 9 and current_time >= package.available_time:
                delivery_address = package.corrected_address
            else:
                delivery_address = package.address

            #find package address
            if delivery_address not in distance_dict:
                print(f"Address not found: {package.address}")
            else:
                package_index = distance_dict[delivery_address]

            #check availability of package for delivery
            if current_time >= package.available_time:
                distance = get_distance(current_location, package_index)
                travel_minutes = distance / 18 * 60

                #to prioritize packages with time deadlines over EOD deadline packages
                if isinstance(package.deadline, datetime): #Time deadlines
                    time_until_deadline = (package.deadline - current_time).total_seconds() / 60
                else: #"EOD" deadlines
                    time_until_deadline = float("inf")

                if travel_minutes <= time_until_deadline:
                    if time_until_deadline < shortest_time_until_deadline:
                        shortest_time_until_deadline = time_until_deadline
                        shortest_distance = distance
                        next_stop = package
                        next_stop_address = delivery_address

                    elif time_until_deadline == shortest_time_until_deadline:
                        if distance < shortest_distance:
                            shortest_distance = distance
                            next_stop = package
                            next_stop_address = delivery_address

        #add mileage traveled to total mileage
        dist_traveled += shortest_distance

        #calculate travel time and add to total time traveled
        travel_minutes = shortest_distance / 18 * 60
        current_time += timedelta(minutes=travel_minutes)

        #"move" the truck to next location
        if next_stop is not None:
            current_location = distance_dict[next_stop_address]
            truck.pop(truck.index(next_stop.package_id))  #remove package from truck to "deliver"
            next_stop.status = "delivered" #update package's status to delivered
            next_stop.delivery_time = current_time #timestamp the delivery

            #test delivery status update
            #print(f"Delivered package {next_stop.package_id} at {current_time:%I:%M %p}")

    #print(f"Total Delivery mileage: {dist_traveled:.2f} miles")
    #print(f"Time at Final Delivery: {current_time:%I:%M %p}")

    #calculate distance back to hub, and add to total traveled miles
    back_to_hub_distance = get_distance(current_location,0)
    dist_traveled += back_to_hub_distance
    #print(f"Total mileage once back at hub: {dist_traveled:.2f} miles")

    #calculate time back to hub, and update current time
    time_to_hub = back_to_hub_distance / 18 * 60
    current_time += timedelta(minutes=time_to_hub)
    total_mileage += dist_traveled


    return current_time, dist_traveled

truck_1_end_time, truck_1_mileage = deliver_packages(truck_1,"8:00 AM")
truck_2_end_time, truck_2_mileage = deliver_packages(truck_2, "9:05 AM")
truck_3_end_time, truck_3_mileage = deliver_packages(truck_3, truck_1_end_time)

user_time = input("Enter a time to see package statuses (format as 9:00 AM): ")
user_time = datetime.strptime(user_time, "%I:%M %p")

def get_truck_number(package_id):
    if package_id in truck_1_packages:
        truck_number = "1"
    elif package_id in truck_2_packages:
        truck_number = "2"
    elif package_id in truck_3_packages:
        truck_number = "3"
    return truck_number

for bucket in package_table.table:
    for package in bucket:

        #print Package ID # & Truck assigned
        print(f"Package {package.package_id}: "
              f"Truck {get_truck_number(package.package_id)} | ")

        #print address
        if package.package_id == 9 and user_time >= package.available_time:
            display_address = package.corrected_address
            display_city = package.corrected_city
            display_zip = package.corrected_zip
        else:
            display_address = package.address
            zip_code = package.zip_code
            display_city = package.city
            display_zip = package.zip_code

        print(f"Delivery Address: {display_address}, {display_city}, {display_zip} | ")

        #print deadline, weight, notes from package file
        print(f"Delivery Deadline: {package.deadline} | "
              f"Package Weight: {package.weight} lbs. | "
              f"Package Notes: {package.notes} | ")

        #print loading time or status if not loaded
        if package.loading_time <= user_time:
              print(f"Loaded: {package.loading_time:%I:%M %p} | ")
        else:
            print("Not loaded")

        #print delivery time or status if not delivered
        if package.delivery_time <= user_time:
            print(f"Status: Delivered at {package.delivery_time:%I:%M %p}\n")
        elif package.available_time > user_time:
            print(f"Status: Delayed\n")
        elif user_time <= package.loading_time:
            print(f"Status: At the hub\n")
        else:
            print(f"Status: En Route\n")


        """ if package.delivery_time is not None and package.delivery_time <= user_time:
            print(f"Package {package.package_id}: Delivered")
        elif package.available_time is not None and package.available_time > user_time:
            print(f"Package {package.package_id}: Delayed")
        elif user_time <= package.loading_time:
            print(f"Package {package.package_id}: At the hub")
        else:
            print(f"Package {package.package_id}: En Route") """




