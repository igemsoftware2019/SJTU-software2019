file_name="/Users/sion/Desktop/database/Protein_domains.csv"

f=open(file_name,"r")
next(f)

out_file="Protein_domains.sql"

def out_put_file(out_file,count,line):
    out_f=open(out_file,"a")
    out_f.write("insert into Protein_domains value("+count+","+line+");\n")

i=1

for line in f:
    count= str(i)
    i = i+1
    out_put_file(out_file,count,line)


