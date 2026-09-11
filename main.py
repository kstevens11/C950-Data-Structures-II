#Student ID: 013116778

#import the package and hash_table files for use
from package import Package
from hash_table import HashTable

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
    for line in distance_file:
        distance_input = line.strip().split(",")

        #start reading at HUB row of file
        if len(distance_input) > 2 and "HUB" in distance_input[2]:
            start_line = True

        #row counter for tracking
        if start_line:
            #print(distance_input) #to test distance_input data load
            distance_row += 1

            #append data to distance_data list only if distance element
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

#test dictionary loading
#print(distance_dict)

