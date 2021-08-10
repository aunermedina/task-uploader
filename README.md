# Setting up a new project in Todoist app.

[![changelog](https://img.shields.io/badge/changelog-v1.3.0-blue.svg)](CHANGELOG.md)


My personal project creation script for Todoist app.

Note, I use this script to create a project with its corresponding tasks organized in sections as Subjects in my Todoist account everytime a new semester started at school. Saving me a whole entire day of CaP'ing data.

### Install: 
```
git clone "https://github.com/aunermedina/task-uploader.git"
cd task-uploader
pip install -r requirements.txt
touch .env -> open the .env file and store your API Token. 
```
Create a '.xlsx' file and enter the name of the task in the first column and the due date (YYYY-MM-DD) in the second column, third column is the type of activity. 
Also, enter the worksheet name since this is the subject name, for each subject a section will be created in the project then a hyphen and the label you want to use for this subject/section. 

### Usage:

To run the script type in 
```
python3 task_uploader.py  -c <Calendar Name> -f <File path/name> 
```
for help on the script type in 
```
python3 task_uploader.py -h
```

### Env File Format:
```bash
API_TOKEN="APITokenGoesHere"
DEBUG=True
```