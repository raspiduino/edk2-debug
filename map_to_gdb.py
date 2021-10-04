# map_to_gdb.py - generate gdb script for loading debug symbols.
# Copyright 2021 Giang Vinh Loc
# Under MIT license

# Usage:
# [python3] ./map_to_gdb.py path/to/package.map gdb_script_name
# Example:
# python3 ./map_to_gdb.py edk2/Build/ArmVirtQemu-AARCH64/DEBUG_GCC5/ArmVirtQemu.map my_gdb_script

import sys

# Read map file
map_file = open(sys.argv[1])
debug_list = map_file.read().split("\n")
map_file.close()

# Insert one "" to the index 0 so that we can match the line 1 in .map file with index 1 in the list 
debug_list.insert(0, "")

# File and addr place holder list
addr = []
file = []

# Get addr and file path
for line in debug_list:
    if line != "":
        if debug_list.index(line) % 2 == 0:
            # Base address line
            # For example we will get "0x0000001800" the string "(GUID=469FC080-AEC1-11DF-927C-0002A5D5C51B .textbaseaddress=0x0000001800 .databaseaddress=0x0000006000)"
            addr.append(line[60:72])
        if debug_list.index(line) % 3 == 0:
            # File path line
            # For example we will get "/tmp/sources/edk2/Build/ArmVirtQemu-AARCH64/DEBUG_GCC5/AARCH64/ArmPlatformPkg/PrePeiCore/PrePeiCoreUniCore/DEBUG/ArmPlatformPrePeiCore" from the string "(IMAGE=/tmp/sources/edk2/Build/ArmVirtQemu-AARCH64/DEBUG_GCC5/AARCH64/ArmPlatformPkg/PrePeiCore/PrePeiCoreUniCore/DEBUG/ArmPlatformPrePeiCore.efi)"
            # Then add the ".debug" extension for it
            file.append(line[7:-5] + ".debug")

# Simple check if the number of address and the number of file patch matchr
if len(addr) != len(file):
    print("Something went wrong! Got " + str(len(addr)) + " addresses but " + str(len(file)) + " files!")
    print(addr)
    print(file)
    exit(1)

# If everything fine, go ahead and write a gdb script
# Open gdb script file to write
script_file = open(sys.argv[2], "w")

# Write
for i in range(len(addr)):
    script_file.write("add-symbol-file " + file[i] + " " + addr[i] + "\n")

# Done, close it
script_file.close()
