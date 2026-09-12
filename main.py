#Student ID: 013116778

#import the package and hash_table files for use
from package import Package
from hash_table import HashTable
from datetime import datetime, timedelta

#create empty package hash table
package_table = HashTable()

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

        #create Package object with delimited package data and starter values for load time, delivery time, and status
        package = Package(
            int(package_data[0]),
            package_data[1],
            package_data[2],
            package_data[3],
            package_data[4],
            package_data[5],
            package_data[6],
            None,
            None,
            "at the hub")

        #save the package data to the hash table
        package_table.put(package)

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
                distance_dict[address_data] = dict_counter #adds address to dictionary and assigns incrementing dictionary key
                dict_counter += 1 #increments for key assignment

        previous_line = distance_input

#test dictionary loading
#(distance_dict)

#test distance mapping
#print(distance_data[17][4])

#test dictionary lookup
#print(distance_dict["195 W Oakland Ave"])

#manually create empty truck lists
truck_1 = []
truck_2 = []
truck_3 = []

#assign package ids to trucks
truck_1_packages = [7, 13, 14, 15, 16, 19, 20, 21, 27, 28, 34, 39, 40]
truck_2_packages = [1, 3, 6, 10, 11, 12, 18, 25, 26, 29, 30, 31, 36, 37, 38]
truck_3_packages = [2, 4, 5, 8, 9, 17, 22, 23, 24, 32, 33, 35]

#load truck lists with assignments (Package objects)
for package_id in truck_1_packages:
    truck_1.append(package_table.lookup(package_id))

for package_id in truck_2_packages:
    truck_2.append(package_table.lookup(package_id))

for package_id in truck_3_packages:
    truck_3.append(package_table.lookup(package_id))

#test package loading
#print(truck_1)
#print(truck_2)
#print(truck_3)

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

current_location = 0
next_stop = None
shortest_distance = float("inf")
dist_traveled = 0

#specify that while there are still packages left to be delivered
while any(package.status != "delivered" for package in truck_1_packages):

#find the package on the truck with the closest destination
    for package in truck_1_packages:
        if package.status != "delivered":
            package_index = distance_dict[package.address]
            distance = get_distance(current_location, package_index)

            if distance < shortest_distance:
                shortest_distance = distance
                next_stop = package

        #add mileage traveled to total mileage
        dist_traveled += shortest_distance

        #"move" the truck to next location
        if next_stop is not None:
            current_location = distance_dict[next_stop.address]

        next_stop.status = "delivered" #mark package delivered



