#Student ID: 013116778

#import the package and hash_table files for use
from package import Package
from hash_table import HashTable

#create empty package hash table
package_table = HashTable()

#open the CSV file "WGUPS Package File.csv"
with open("WGUPS Package File.csv") as package_file:
    for line in package_file:
        if "Package ID" in line:  #start at first header row above data to be parsed
            continue
        package_data = line.strip().split(",") #remove whitespace from the ends & split at the commas

        #create Package object with deliminated package data and starter values for load time, delivery time, and status
        package = Package(package_data[0], package_data[1], package_data[2], package_data[3], package_data[4],package_data[5],package_data[6],None,None,"at the hub")

        #save the package data to the hash table
        package_table.put(package)
