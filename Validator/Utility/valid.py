import os
import shutil
import logging
from datetime import datetime


def paircheck(logger, project_name, input_dir):
    print("-----------------------------------------------------------------------")
    # SEARCH FOR FILE WITH DAT AND CTL EXTENSION IN SOURCE DIRECTORY
    print("Validating {}".format(project_name))
    print("--------------------------------")
    logger.debug("# Check for dat and ctl files")
    count = {}
    filenames = []
    for file in os.listdir(input_dir):
        filenames.append(os.path.splitext(file))
    for key, val in filenames:
        count.setdefault(key,[]).append(val)

    output = []
    for key in sorted(count):
        ext = ['.ctl' , '.dat']
        if count[key] == ext:
            item = [(key+count[key][0]),(key+count[key][1])]
            output.append(item) 
            print("{} {} has a pair".format(project_name, key))
        else:
            miss = list(set(ext) - set(count[key]))[0]
            print("{} {} is missing a {} file".format(project_name, key, miss))
    
    final = {}
    for item in os.listdir(input_dir):
        final[item] = False
    
    return output,count,final

def validity(logger, header, output, delimiter, final):
    # READ FILES AND CHECK COUNT AND ENTRY -> OUTCOME
    logger.debug("# Check count and entry")
    if header == True:
        for pair in output:
            c = open(os.path.abspath(pair[0]), 'r')
            d = open(os.path.abspath(pair[1]), 'r')
            col = c.read()
            counter = int(col.split(delimiter)[0])
            entry = int(len(d.readlines()))-1
            if counter == entry:
                final[pair[0]] = True
                final[pair[1]] = True
                # logger.info("Validation Test for {} {}: Success".format(project_name, os.path.splitext(pair[0])[0]))
                # print "Validation Test for {} {}: Success".format(project_name, os.path.splitext(pair[0])[0])
            # else:
            #     logger.warning("Validation Test for {} {}: Failure".format(project_name, os.path.splitext(pair[0])[0]))
            #     print "Validation Test for {} {}: Failure".format(project_name, os.path.splitext(pair[0])[0])
            c.close()
            d.close()
    else:
        for pair in output:
            c = open(os.path.abspath(pair[0]), 'r')
            d = open(os.path.abspath(pair[1]), 'r')
            col = c.read()
            counter = int(col.split(delimiter)[0])
            entry = int(len(d.readlines()))
            if counter == entry:
                final[pair[0]] = True
                final[pair[1]] = True
            #     logger.info("Validation Test for {} {}: Success".format(project_name, os.path.splitext(pair[0])[0]))
            #     print "Validation Test for {} {}: Success".format(project_name, os.path.splitext(pair[0])[0])
            # else:
            #     logger.warning("Validation Test for {} {}: Failure".format(project_name, os.path.splitext(pair[0])[0]))
            #     print "Validation Test for {} {}: Failure".format(project_name, os.path.splitext(pair[0])[0])
            c.close()
            d.close()    
    return final

# MOVE FILE TO RESPECTIVE LANDING
def headcount(logger, output, final, delimiter):
    for pair in output:
        c = open(os.path.abspath(pair[0]), 'r')
        d = open(os.path.abspath(pair[1]), 'r')

        # CHECK IF NUMBER OF COLUMN IS CORRECT TO PROVIDED
        col = c.read()
        column = int(col.split(delimiter)[1])
        dat = d.read()
        tempo = 0
        for item in dat.split('\n'):
            if int(len(item.split(delimiter))) == column:
                tempo += 1
                # print item 
            else:
                print("Error in {} : {}".format(pair[1], item.split(delimiter)))
                break
        if tempo != len(dat.split('\n')):
            final[pair[0]] = final[pair[0]] and False
            final[pair[1]] = final[pair[0]] and False
        c.close()
        d.close()
    return final

def backup(logger, input_dir, log_dir, backup_dir, final, count, project_name):
    # CHECK IF ALL SUCCESS THEN MOVE DATA TO BACKUP
    os.chdir(backup_dir)
    if not os.path.exists("Success"):
        os.makedirs("Success")
    if not os.path.exists("Failure"):
        os.makedirs("Failure")
    os.chdir(input_dir)
    for file in sorted(final):
        if final[file]:
            logger.info("Validation Test for {} {}: Success".format(project_name, file))
            print "Validation Test for {} {}: Success".format(project_name, file)
            # shutil.move(file, os.path.join(backup_dir,"Success"))
            logger.debug("File: {} has been backed up to {}".format(file, os.path.join(backup_dir,"Success")))
        else:
            logger.warning("Validation Test for {} {}: Failure".format(project_name, file))
            print "Validation Test for {} {}: Failure".format(project_name, file)
            # shutil.move(file, os.path.join(backup_dir,"Failure"))
            logger.debug("File: {} has been backed up to {}".format(file, os.path.join(backup_dir,"Failure")))

    print ("-----------------------------------------------------------------------")

