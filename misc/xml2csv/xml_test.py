"""
Created on Wed Sep 27 16:03:25 2017

@author: Rohit Mohan
"""

import lxml.etree as ET
import csv


name_of_final_csv = "data.csv"
name_of_input_file = "xml_test.xml"
header_tags_to_ignore = ["Document"]
tags_to_skip = ["GrpHdr"]
tag_for_new_entry = "PmtInf"



def unwanted_header_tags_present(recent, tags_to_ignore):
    if recent in tags_to_ignore : return True
    else : False


def skip_till_tag_is_closed(flag, event, recent, tags_to_skip) : 
    if recent in tags_to_skip and event == "start" : 
        return recent 
    elif recent == flag and event == "end" : 
        return None
    
    else: return flag 



data = list()
tag_path = ""
i = 0
index = -1
flag = None
for event, elem in ET.iterparse(name_of_input_file, events=["start", "end"]):
    recent = elem.tag.split('}')[1]
    
    if unwanted_header_tags_present(recent,header_tags_to_ignore) : continue
    
    flag = skip_till_tag_is_closed(flag, event, recent, tags_to_skip)
    if flag : continue 
    
    
    if event == "start":
        if tag_path : tag_path += '.' + recent
        else : tag_path = recent
        
        if tag_for_new_entry == tag_path : 
            index += 1
            data.append(dict())
    
        value = elem.text if elem.text else None
        if value : 
            data[index][tag_path]= value
    
    
    
    
    elif event == "end" :
        tag_path = '.'.join(tag_path.split('.')[:-1])
    
# extracting unique names for columns : 
S = set()
for datum in data : 
    for key in datum :
        S.add(key)
keys = list(S)


# prepare the final table
for datum in data:
    for key in keys : 
        if key not in datum : datum[key] = None


# to CSV
with open(name_of_final_csv, 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    for datum in data:
        dict_writer.writerow(datum)






