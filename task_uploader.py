import os
import argparse
import logging
from random import randint
from todoist_api_python.api import TodoistAPI
from openpyxl import load_workbook
from dotenv import load_dotenv

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

    # Get projects list
    projects = api.get_projects()

    # Search for desire Project (SCHOOL)
    for i in range(len(projects)):
        if "SCHOOL" in projects[i].name:
            school_pid = projects[i].id

    # read file
    logging.info('Reading file...')
    wb = load_workbook(fin)

    # Create new Semester Project
    logging.info('Creating new project...')
    semester = api.add_project(name='Semester ' + cal, parent_id=school_pid, color=randint(30, 49))

    for materia in wb.worksheets:
        # Create Section per Subject(Worksheet)
        subject = materia.title.split('-')  # worksheet in format: Subject-Label
        section = api.add_section(name=subject[0], project_id=semester.id)
        # label_id = 2155146353 if subject[1] == 'proyecto' else api.add_label(name=subject[1]).id
        label = api.get_label(label_id="2155146353") if subject[1] == 'proyecto' else api.add_label(name=subject[1])
        subject_count += 1
        logging.info('Creating section: ' + subject[0])
        logging.info('Creating tasks...')
        for task in materia.values:
            # Create Tasks Per Section
            try:
                # due_date must be text in excel with format: 2021-08-10 not 2021-8-10
                # description is type of activity: foro or buzon
                # label_ids are label 'INICIO' (2155113156) and section label
                api.add_task(content=task[0], description=task[2], section_id=section.id, labels=['INICIO', label.name], due_date=task[1])
                task_count += 1
            except Exception as error:
                logging.error(error)

    # Print successful message
    logging.info('Successfully created {} section(s) with {} task(s).'.format(subject_count, task_count))
    logging.info('Work done!')
    

if __name__ == "__main__":
    logging.info('Starting configuration...')
    parser = argparse.ArgumentParser(prog='task_uploader', description="Create tasks in Todoist app based on xlsx file")
    parser.add_argument("-c", "--calendar", help="Calendar Description. e.g. 2020B", required=True)
    parser.add_argument("-f", "--file", help="A file to process", required=True)  # file should be in the same path
    args = parser.parse_args()
    # Executiong string: python task_uploader.py -c 2022A -f 2022A.xlsx
    # PowerShell exe string: py task_uploader.py -c 2023A -f 2023A.xlsx
    todoist_task_uploader(args.calendar, args.file)