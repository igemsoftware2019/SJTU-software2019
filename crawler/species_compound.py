file_path="/Volumes/DATA/igem/database2"

out_f=open("species_add_compound.sql","a")

sequence_list=['alyratacyc', 'aracyc', 'asparaguscyc', 'barleycyc', 'breadwheatcyc', 'cacuminatacyc', 'cannuumcyc', 'carietinum', 'carnationcyc', 'cassavacyc', 'castorbeancyc', 'chlamycyc', 'corncyc', 'csativa', 'cucumbercyc', 'flaxcyc', 'grapecyc', 'list', 'ljaponicuscyc', 'mdomesticacyc', 'mosscyc', 'mtruncatulacyc', 'ntabacum', 'oilseedrapecyc', 'oryzacyc', 'plantcyc', 'poplarcyc', 'potatocyc', 'rchinensiscyc', 'redclovercyc', 'soleraceacyc', 'sorghumbicolorcyc', 'sunflowercyc', 'sweetorangecyc', 'tomatocyc']


def delete_line_mark(list):
    out=""
    for data in list:
        data=data.replace("\n","")
        if out=="":
            out=data
        else:
            out=out+",,"+data
    return out

def spli(file):

    line_list=file.readlines()
    needed_line_list=[]
    temp=0

    for line in line_list:

        if line == "//\n":        
            needed_line_list.append(line_list.index(line,temp+1))
            temp=line_list.index(line,temp+1)
            
    list_length=len(needed_line_list)
    final_list=[]

    for i in range(list_length-1):

        if i == 0:
            tem=0

            for line in line_list:

                if line == "#\n":
                    num=line_list.index(line,tem+1)+1
                    tem=line_list.index(line,tem+1)

                    if "UNIQUE-ID - " not in line_list[num]:
                        pass

                    else:
                        start=num-1
                        break

        else:
            start=int(needed_line_list[i-1])
        
        end=int(needed_line_list[i])

        new_line=delete_line_mark(line_list[start:end])
        final_list.append(new_line)

    return final_list

def show_real(name,file):
    temp_path=file_path+"/"+file
    compound_f=open(temp_path+"/compounds.dat","r", errors='ignore')
    compound_list=spli(compound_f)
    out=name
    for compound_info in compound_list:
        
        new_name="UNIQUE-ID - "+name+",,"


        if new_name in compound_info:
            #print(name)
            #print(compound_info)

            compound_info_list=compound_info.split(",,")

            for single_compound_info in compound_info_list:
                if "COMMON-NAME" in single_compound_info:
                    #print(single_compound_info)
                    out=single_compound_info.replace("COMMON-NAME - ","")
                    
                else:
                    pass
        else:
            pass
    #print(out+"\n")
    return out




    
import os,re

n=0

for file in os.listdir(file_path):
    if "cyc" in file:
        print(file)
        n+=1

        out_line_list=[]
        out_line_list_1=[]

        temp_path=file_path+"/"+file
        pub_f=open(temp_path+"/pubs.dat","r", errors='ignore')

        for line in pub_f.readlines():
            if "SOURCE - " in line:
                out_line_list.append(line)

        for out_line in out_line_list:
            out=out_line.replace("SOURCE - ","")
            out=out.replace("\n","")
            out_line_list_1.append(out)
        
        out_species=""
        for pub in out_line_list_1:
            if out_species=="":
                out_species=str(pub)
            else:
                out_species=out_species+",,"+str(pub)

        spec_f=open(temp_path+"/species.dat","r")

        for line in spec_f.readlines():
            if "(NCBI-TAXONOMY-DB" in line:
                pattern=re.compile("\".+\"")
                out=pattern.findall(line)[0]
                out_dblinks=out.replace("\"","")
            elif "COMMON-NAME" in line:
                out=line.replace("\n","")
                out_commonname=out.replace("COMMON-NAME - ","")

            elif "NCBI-TAXONOMY-ID" in line:
                out=line.replace("\n","")
                out_ncbiid=out.replace("NCBI-TAXONOMY-ID - ","")

            else:
                pass
        
        out_f.write("insert into species value("+str(n)+", \""+out_ncbiid+"\", \""+out_commonname+"\", \""+out_dblinks+"\", \""+out_species+"\")\n")

        genes_f=open(temp_path+"/genes.dat","r", errors='ignore')
        gene_list=spli(genes_f)

        gene_number=0
        for gene_info in gene_list:
            gene_number+=1
            gene_info_list=gene_info.split(",,")

            out_uniqueid,out_commonname_gene,out_type,out_product,out_sequence="","","","",""

            for signle_gene_info in gene_info_list:

                if "UNIQUE-ID" in signle_gene_info:
                    out_uniqueid=signle_gene_info.replace("UNIQUE-ID - ","")

                elif "COMMON-NAME" in signle_gene_info:
                    out_commonname_gene=signle_gene_info.replace("COMMON-NAME - ","")

                elif "TYPES" in signle_gene_info:
                    out_type=signle_gene_info.replace("TYPES - ","")

                elif "PRODUCT" in signle_gene_info:
                    out_product=signle_gene_info.replace("PRODUCT - ","")
            out_f.write("insert into gene value("+str(gene_number)+", \""+out_uniqueid+"\", \""+out_commonname_gene+"\", \""+out_type+"\", \""+out_product+"\", \""+out_sequence+"\")\n")


        enzyme_f=open(temp_path+"/enzrxns.dat","r", errors='ignore')
        enzyme_list=spli(enzyme_f)

        enzyme_number=0
        for enzyme_info in enzyme_list:
            enzyme_number+=1
            enzyme_info_list=enzyme_info.split(",,")

            out_uniqueid_enzyme,out_ecnumber,out_sequence_enzyme,out_name,out_enzyme="","","","",""

            for signle_enzyme_info in enzyme_info_list:

                if "UNIQUE-ID" in signle_enzyme_info:
                    out_uniqueid_enzyme=signle_enzyme_info.replace("UNIQUE-ID - ","")

                elif "COMMON-NAME" in signle_enzyme_info:
                    out_name=signle_enzyme_info.replace("COMMON-NAME - ","")

                elif "ENZYME" in signle_enzyme_info:
                    out_enzyme=signle_enzyme_info.replace("ENZYME - ","")

                #elif "REACTION" in signle_enzyme_info:
                #    out_ecnumber=show_ecnumber(signle_enzyme_info.replace("REACTION - ",""),file)

            out_f.write("insert into enzyme value("+str(enzyme_number)+", \""+out_uniqueid_enzyme+"\", \""+out_ecnumber+"\", \""+out_sequence_enzyme+"\", \""+out_name+"\", \""+out_enzyme+"\")\n")


        reaction_f=open(temp_path+"/reactions.dat","r", errors='ignore')
        reaction_list=spli(reaction_f)

        reaction_number=0
        for reaction_info in reaction_list:
            reaction_number+=1
            reaction_info_list=reaction_info.split(",,")

            out_uniqueid_reaction,out_type_reaction,out_left,out_right,out_relevent="","","","",""

            for signle_reaction_info in reaction_info_list:
                if "UNIQUE-ID" in signle_reaction_info:
                    out_uniqueid_reaction=signle_reaction_info.replace("UNIQUE-ID - ","")

                elif "TYPES" in signle_reaction_info:
                    out_type_reaction=signle_reaction_info.replace("TYPES - ","")

                #elif "LEFT - " in signle_reaction_info:
                #    temp_out_left=signle_reaction_info.replace("LEFT - ","")
                #    if out_left=="":
                #        out_left=show_real(temp_out_left,file)
                #    else:
                #        out_left=out_left+",,"+show_real(temp_out_left,file)
                
                #elif "RIGHT - " in signle_reaction_info:
                #    temp_out_right=signle_reaction_info.replace("RIGHT - ","")
                #    if out_right=="":
                #        out_right=show_real(temp_out_right,file)
                #    else:
                #        out_right=out_right+",,"+show_real(temp_out_right,file)

                elif "PHYSIOLOGICALLY-RELEVANT" in signle_reaction_info:
                    out_relevent=signle_reaction_info.replace("PHYSIOLOGICALLY-RELEVANT? -","")
            out_f.write("insert into reaction value("+str(reaction_number)+", \""+out_uniqueid_reaction+"\", \""+out_type_reaction+"\", \""+out_left+"\", \""+out_right+"\", \""+out_relevent+"\")\n")

        pathway_f=open(temp_path+"/pathways.dat","r", errors='ignore')
        pathway_list=spli(pathway_f)

        pathway_number=0
        for pathway_info in pathway_list:
            pathway_number+=1
            pathway_info_list=pathway_info.split(",,")

            out_uniqueid_pathway,out_dblinks_pathway,out_predecessor,out_synonym,out_reactionlist="","","","",""

            for single_pathway_info in pathway_info_list:
                if "UNIQUE-ID" in single_pathway_info:
                    out_uniqueid_pathway=single_pathway_info.replace("UNIQUE-ID - ","")

                elif "DBLINKS" in single_pathway_info:
                    out_dblinks_pathway=single_pathway_info.replace("DBLINKS - ","")

                elif "PREDECESSORS" in single_pathway_info:
                    out_predecessor=single_pathway_info.replace("PREDECESSORS - ","")

                elif "SYNONYMS" in single_pathway_info:
                    out_synonym=single_pathway_info.replace("SYNONYMS - ","")

                elif "REACTION-LIST" in single_pathway_info:
                    temp_out_reactionlist=single_pathway_info.replace("REACTION-LIST - ","")
                    if out_reactionlist=="":
                        out_reactionlist=temp_out_reactionlist
                    else:
                        out_reactionlist=out_reactionlist+",,"+temp_out_reactionlist

            out_f.write("insert into pathway value("+str(pathway_number)+", \""+out_uniqueid_pathway+"\", \""+out_dblinks_pathway+"\", \""+out_predecessor+"\", \""+out_synonym+"\", \""+out_reactionlist+"\")\n")
        
        compound_f=open(temp_path+"/compounds.dat","r", errors='ignore')

        compound_list=spli(compound_f)

        compound_number=0
        for compound_info in compound_list:
            compound_number+=1
            compound_info_list=compound_info.split(",,")

            out_uniqueid_compound,out_smiles,out_inchi,out_inchikey,out_commonname_compound,out_dblinks_compound,out_synonym_compound="","","","","","",""

            for single_compound_info in compound_info_list:

                if "UNIQUE-ID" in single_compound_info:
                    out_uniqueid_compound=single_compound_info.replace("UNIQUE-ID - ","")

                elif "SMILES" in single_compound_info:
                    out_smiles=single_compound_info.replace("SMILES - ","")

                elif "INCHI -" in single_compound_info:
                    out_inchi=single_compound_info.replace("INCHI - InChI=","")

                elif "INCHI-KEY" in single_compound_info:
                    out_inchikey=single_compound_info.replace("INCHI-KEY - InChIKey=","")

                elif "COMMON-NAME" in single_compound_info:
                    out_commonname_compound=single_compound_info.replace("COMMON-NAME - ","")

                elif "DBLINKS" in single_compound_info:
                    temp_out_dblinks_compound=single_compound_info.replace("DBLINKS - ","")
                    if out_dblinks_compound=="":
                        out_dblinks_compound=temp_out_dblinks_compound
                    else:
                        out_dblinks_compound=out_dblinks_compound+",,"+temp_out_dblinks_compound
                
                elif "SYNONYMS" in single_compound_info:
                    temp_out_synonym_compound=single_compound_info.replace("SYNONYMS - ","")
                    if out_synonym_compound=="":
                        out_synonym_compound=temp_out_synonym_compound
                    else:
                        out_synonym_compound=out_synonym_compound+",,"+temp_out_synonym_compound

            out_f.write("insert into compound value("+str(compound_number)+", \""+out_uniqueid_compound+"\", \""+out_smiles+"\", \""+out_inchi+"\", \""+out_inchikey+"\", \""+out_commonname_compound+"\", \""+out_dblinks_compound+"\", \""+out_synonym_compound+"\")\n")
            
out_f.close()