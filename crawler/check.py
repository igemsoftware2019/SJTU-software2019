#!/usr/bin/env python

f=open("/Volumes/DATA/combine/species_final_divided.sql","r")
for line in f.readlines():
    if "!" in line:
        if "insert into species value" in line:
            pass
        else:
            print(line)