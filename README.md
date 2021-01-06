# Setting up a new project in Todoist app.
# <img src="https://d3vv6lp55qjaqc.cloudfront.net/items/1L1w0v431V0d1K410f3Y/keepAChangelog-logo-dark.svg" height=150 alt="Keep a Changelog" />

[![Keep a Changelog v1.1.0 badge][changelog-badge]][changelog] [![Version 1.1.0 Badge][version-badge]][changelog]


My personal project creation script for Todoist app.

Note, I use this script to create a project with its corresponding tasks organized in sections as Subjects in my Todoist account everytime a new semester started at school. Saving me a whole entire day of CaP'ing data.

### Install: 
```bash
git clone "https://github.com/aunermedina/task-uploader.git"
cd task-uploader
pip install -r requirements.txt
touch .env -> open the .env file and store your API Token. 
create a '.xlsx' file and enter the name of the task in the first column and the due date (YYYY-MM-DD) in the second column, third column is the label of the subject. Also enter the worksheet name since this is the subject name, for each subject a section will be created in the project. 
```

### Usage:
```bash
To run the script type in 'python3 task_uploader.py  -c <Calendar Name> -f <File path/name>'
for help on the script type in 'python3 task_uploader.py -h'
```

### Env File Format:
```bash
API_TOKEN="APITokenGoesHere"
DEBUG=True
```