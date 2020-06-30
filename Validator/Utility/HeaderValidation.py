from __future__ import division
import os
import logging
import logging.config
import yaml
from datetime import datetime
import shutil
import argparse
import csv


# CHECK YAML FILE
def yaml_loader(filepath):
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor, Loader=yaml.FullLoader)
    return data

if __name__ == "__main__":
    filepath = "validator_yaml.yaml"
    data = yaml_loader(filepath)

    dic = data.get("IFRS")
    project_name = "IFRS"
    input_dir = dic['INPUT_DIR']
    log_dir = dic['LOG_DIR']
    backup_dir = dic['BACKUP_DIR']

    header = dic["HEADER_CHECK"]
    delimiter = dic["DELIMITER"]
    del_check = dic["DEL_CHECK"]


# SET WORKING DIRECTORY
os.chdir(input_dir)

output = [['datafile1.ctl', 'datafile1.dat'], ['datafile2.ctl', 'datafile2.dat'], ['datafile4.ctl', 'datafile4.dat']]
# READ FILES AND CHECK COUNT AND ENTRY -> OUTCOME
final = {'datafile2.dat': True, 'datafile4.ctl': True, 'datafile2.ctl': True, 'datafile1.dat': True, 'datafile4.dat': True, 'datafile1.ctl': True}
# def checkcol(output):
# print dict(final)
# for pair in output:
#     c = open(os.path.abspath(pair[0]), 'r')
#     d = open(os.path.abspath(pair[1]), 'r')

#     # CHECK IF NUMBER OF COLUMN IS CORRECT TO PROVIDED
#     col = c.read()
#     column = int(col.split(delimiter)[1])
#     dat = d.read()
#     tempo = 0
#     for item in dat.split('\n'):
#         if int(len(item.split(delimiter))) == column:
#             tempo += 1
#             print item 
#         else:
#             print("There is an error here: {} for {}".format(item.split(delimiter), pair[1]))
#             break
#     if tempo != len(dat.split('\n')):
#         final[pair[0]] = final[pair[0]] and False
#         final[pair[1]] = final[pair[0]] and False
#     c.close()
#     d.close()
# for i in sorted(final):
#     print i , final[i]
# print dict(final)
# # DELIMITER CHECKS
# def checkdel(dat):
#     sniffer = csv.Sniffer()
#     dialect = sniffer.sniff(dat)
#     print dialect.delimiter
#     returns ','


count = {}
filenames = []
for file in os.listdir(input_dir):
    filenames.append(os.path.splitext(file))
for key, val in filenames:
    count.setdefault(key,[]).append(val)
# {'datafile4': ['.ctl', '.dat'], 'datafile3': ['.dat'], 
# 'datafile2': ['.ctl', '.dat'], 'datafile1': ['.ctl', '.dat']}

for key in sorted(count):
        if '.ctl' in count[key] and '.dat' in count[key]:
            print(project_name + " " + key + " has a pair")
        elif '.ctl' in count[key] and not '.dat' in count[key]:
            print(project_name + " " + key + " is missing '.dat' file")
            # logger.warning("{} {} is missing a '.dat' file".format(project_name, key))
        elif not '.ctl' in count[key] and '.dat' in count[key]:
            print(project_name + " " + key + " is missing '.ctl' file")
            # logger.warning("{} {} is missing a '.ctl' file".format(project_name, key))

output = []
for key in sorted(count):
    ext = ['.ctl' , '.dat']
    if count[key] == ext:
        print(key + " has a pair")
        item = [(key+count[key][0]),(key+count[key][1])]
        output.append(item) 
        
    else:
        miss = list(set(ext) - set(count[key]))[0]
        print(key + " is missing a {} file".format(miss))

# print output


#output 
#[['datafile1.ctl', 'datafile1.dat'], ['datafile2.ctl', 'datafile2.dat'], 
# ['datafile4.ctl', 'datafile4.dat']]
# print count
# count
# {'datafile4': ['.ctl', '.dat'], 'datafile3': ['.dat'], 
# 'datafile2': ['.ctl', '.dat'], 'datafile1': ['.ctl', '.dat']}