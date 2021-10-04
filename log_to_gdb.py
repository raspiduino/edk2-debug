# log_to_gdb.py - generate gdb script for loading debug symbols.
# Copyright 2021 Giang Vinh Loc
# Under MIT license

# Before using this script, get the log from qemu
# Example:
# qemu-system-aarch64 -M virt -cpu cortex-a53 -m 1024 -pflash flash0.img -pflash flash1.img -nic none -serial file:qemu-log.txt

# Usage:
# [python3] ./log_to_gdb.py /path/to/qemu/console/log.txt gdb_script_name
# Example:
# python3 ./log_to_gdb.py qemu-log.txt my_gdb_script

import sys

# Read serial dump
serial_dump = open(sys.argv[1])
dump_line = serial_dump.read().split("\n")
serial_dump.close()

# Open gdb script to write
gdb = open(sys.argv[2], "w")

# Find the lines begin with "add-symbol-file"
for line in dump_line:
    if "add-symbol-file" in line:
        split = line.split(".dll")
        gdb.write(split[0] + ".debug" + split[1] + "\n")

gdb.close()
