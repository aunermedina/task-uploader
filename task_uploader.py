import os
import argparse
from todoist.api import TodoistAPI
from openpyxl import load_workbook
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def todoist_task_uploader(cal, fin):
    """Method to upload/create tasks with Todoist API"""
    school_pid = ''
    subject_count = 0
    task_count = 0
    # Connect with Todoist API
    api = TodoistAPI(os.getenv('API_TOKEN'))
    print('Connection established!')
    api.sync()

    # Search for desire Project (SCHOOL)
    for project in api.state['projects']:
        if 'SCHOOL' in project['name']:
            school_pid = project['id']

    # read file
    print('Reading file...')
    wb = load_workbook(fin)
    print('Creating new project, sections, tasks...')
    # Create new Semester Project
    semester = api.projects.add('Semester ' + cal, parent_id=school_pid, color=41)

    for materia in wb.worksheets:
        # Create Section per Subject(Worksheet)
        section = api.sections.add(materia.title, semester['id'])
        subject_count += 1
        for task in materia.values:
            # Create Tasks Per Section
            api.items.add(task[0],
                          due={"date": datetime.strftime(task[1], '%Y-%m-%d')},
                          project_id=school_pid,
                          section_id=section['id'])
            task_count += 1

    # Commit Changes and Sync
    #api.commit()
    #api.sync()

    # Print successful message
    print('Successfully created {} section(s) with {} task(s).'.format(subject_count, task_count))
    print('Work done!')
    

if __name__ == "__main__":
    # Define or gather the options and file to use
    parser = argparse.ArgumentParser(prog='task_uploader', description="Create tasks in Todoist app based on xlsx file")
    parser.add_argument("-c", "--calendar", help="Calendar Description. e.g. 2020B", required=True)
    parser.add_argument("-f", "--file", help="A file to process", required=True)
    args = parser.parse_args()

    todoist_task_uploader(args.calendar, args.file)