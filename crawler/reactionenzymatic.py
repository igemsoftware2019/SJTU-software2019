#!/usr/bin/env python

f=open("/Volumes/DATA/final/species_real_final.sql","r")
f_out=open("/Volumes/DATA/final/species_final.sql","w")
for line in f.readlines():
    if "insert into reactionenzymetic value" in line:
        line=line.replace("insert into reactionenzymetic value","insert into reactionenzymatic value")
        f_out.write(line)

    else:
        f_out.write(line)