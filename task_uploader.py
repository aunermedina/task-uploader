import os
import argparse
import logging
from todoist.api import SyncError, TodoistAPI
from openpyxl import load_workbook
from datetime import datetime
from dotenv import load_dotenv
from random import randint

load_dotenv()

log_cli_format = "%(asctime)s [%(levelname)8s] %(message)s" # (%(filename)s:%(lineno)s)"
log_cli_date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(format=log_cli_format, datefmt=log_cli_date_format, level=logging.INFO)

def todoist_task_uploader(cal, fin):
    """    
    Method to upload/create tasks with Todoist API

    Args:
        cal (string): [name of the project or calendar]
        fin (string): [path to the file]
    """
    school_pid = ''
    subject_count = 0
    task_count = 0
    # Connect with Todoist API
    api = TodoistAPI(os.getenv('API_TOKEN'))
    logging.info('Connection established!')
    api.sync()

    # Search for desire Project (SCHOOL)
    for project in api.state['projects']:
        if 'SCHOOL' in project['name']:
            school_pid = project['id']

    # read file
    logging.info('Reading file...')
    wb = load_workbook(fin)
    logging.info('Creating new project...')
    # Create new Semester Project
    semester = api.projects.add('Semester ' + cal, parent_id=school_pid, color=randint(30, 49))

    for materia in wb.worksheets:
        # Create Section per Subject(Worksheet)
        subject = materia.title.split('-')
        section = api.sections.add(subject[0], semester['id'])
        new_label = api.labels.add(subject[1])
        label_id = 2155146353 if subject[1] == 'proyecto' else new_label['id']
        subject_count += 1
        logging.info('Creating section: ' + subject[0])
        logging.info('Creating tasks...')
        for task in materia.values:
            # Create Tasks Per Section
            api.items.add(task[0],
                          due={"date": datetime.strftime(task[1], '%Y-%m-%d')},
        #                   project_id=school_pid,
                          section_id=section['id'],
                          labels=[2155113156, label_id])  # label 'INICIO' and section label
            task_count += 1

    # Commit Changes and Sync
    api.commit()
    api.sync()

    # Print successful message
    logging.info('Successfully created {} section(s) with {} task(s).'.format(subject_count, task_count))
    logging.info('Work done!')
    

if __name__ == "__main__":
    # if os.getenv('DEBUG') == 'true':
    #     logging.debug('Debugging')
    #     api = TodoistAPI(os.getenv('API_TOKEN'))
    #     logging.debug('Connection established!')
    #     api.sync()
    #     # playground down here
    #     # Search for desire Project (SCHOOL)
    #     for project in api.state['projects']:
    #         if 'SCHOOL' in project['name']:
    #             school_pid = project['id']
        
    #     semester = api.projects.add('Semester test', parent_id=school_pid, color=randint(30, 49))
    #     api.commit()
    #     api.sync()

    # else:    
        # Define or gather the options and file to use
    logging.info('Starting configuration...')
    parser = argparse.ArgumentParser(prog='task_uploader', description="Create tasks in Todoist app based on xlsx file")
    parser.add_argument("-c", "--calendar", help="Calendar Description. e.g. 2020B", required=True)
    parser.add_argument("-f", "--file", help="A file to process", required=True)
    args = parser.parse_args()

    todoist_task_uploader(args.calendar, args.file)