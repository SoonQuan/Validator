from __future__ import division
import os
import logging
import yaml
from datetime import datetime
import shutil
import argparse
from Utility.valid import *

# CREATING ARGUMENTS ON CMD
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                description=('''\
    Validation
    ----------
    Remember to update validator_yaml.yaml before using this file
    Usage example: ''' +__file__+ ''' --mode I --entity IFRS
    '''))
parser.add_argument("-m", "--mode", type=str, required=False, metavar=" ", help= "I = Incremental; F = Full")
parser.add_argument("-e", "--entity", type=str, required=False, metavar=" ", help= "Project Name in YAML file")
group = parser.add_mutually_exclusive_group()
group.add_argument("--debug", action="store_true", help="Log in DEBUG level")
args = parser.parse_args()

# CHECK YAML FILE
def yaml_loader(filepath):
    with open(filepath, "r") as file_descriptor:
        data = yaml.load(file_descriptor, Loader=yaml.FullLoader)
    return data

def validator(mode, entity):
    filepath = "validator_yaml.yaml"
    data = yaml_loader(filepath)
    if mode == 'F':
        # VALIDATE ALL FILE
        for project in data:
            project_name = project
            input_dir = data[project]['INPUT_DIR']
            log_dir = data[project]['LOG_DIR']
            backup_dir = data[project]['BACKUP_DIR']
            header = data[project]["HEADER_CHECK"]
            delimiter = data[project]["DELIMITER"]
            del_check = data[project]["DEL_CHECK"]

            # SET WORKING DIRECTORY
            os.chdir(input_dir)

            # CREATE LOG FILE
            logger = logging.getLogger(project_name)
            logger.setLevel(logging.INFO)

            LOG_OUTPUT = datetime.now().strftime(log_dir + r"\prophet_valdation_" + "%Y-%m-%d %H_%M_%S"+ r".log")
            LOG_FORMAT = logging.Formatter("%(levelname)s %(name)s %(asctime)s: %(message)s")
            
            file_handler = logging.FileHandler(LOG_OUTPUT)
            file_handler.setFormatter(LOG_FORMAT)

            logger.addHandler(file_handler)

            # CODES
            output,count,final = paircheck(logger, project_name, input_dir)
            final = validity(logger, header, output, delimiter, final)
            if del_check == True:
                final = headcount(logger, output, final, delimiter)
            backup(logger, input_dir, log_dir, backup_dir, final, count, project_name)

    elif mode == 'I':
        if entity in data:
            # VALIDATE TARGETTED ENTITY
            project_name = entity
            input_dir = data[entity]['INPUT_DIR']
            log_dir = data[entity]['LOG_DIR']
            backup_dir = data[entity]['BACKUP_DIR']
            header = data[entity]["HEADER_CHECK"]
            delimiter = data[entity]["DELIMITER"]
            del_check = data[entity]["DEL_CHECK"]

            # SET WORKING DIRECTORY
            os.chdir(input_dir)

            # CREATE LOG FILE
            logger = logging.getLogger(project_name)
            logger.setLevel(logging.INFO)

            LOG_OUTPUT = datetime.now().strftime(log_dir + r"\prophet_valdation_" + "%Y-%m-%d %H_%M_%S"+ r".log")
            LOG_FORMAT = logging.Formatter("%(levelname)s %(name)s %(asctime)s: %(message)s")
            
            file_handler = logging.FileHandler(LOG_OUTPUT)
            file_handler.setFormatter(LOG_FORMAT)

            logger.addHandler(file_handler)

            # CODES
            output,count,final = paircheck(logger, project_name, input_dir)
            final = validity(logger, header, output, delimiter, final)
            if del_check == True:
                final = headcount(logger, output, final, delimiter)
            backup(logger, input_dir, log_dir, backup_dir, final, count, project_name)

        elif entity == None:
            print("Please input entity")

        elif not entity in data:
            # DOES NOT HAVE PROJECT IN YAML
            print("Project Name:" + str(entity) +" is not in YAML file")
        
    else:
        print "Type '" + __file__ + " --help' for help"

if __name__ == "__main__":
        validator(args.mode, args.entity)
            