import os
import re
import time
import sys
import datetime

# Usage via command line: python veeam_check.py backup_job_name.
# Usage as Zabbix item: veeam_check[backup_job_name].
# Configuration example: UserParameter=veeam_check[*],python C:\scripts\veeam_check.py $1.
# Requirements: Python 3.x installed on the target.
# Exit codes: 0 - Successful backup, 1 - Backup completed with warings, 2 - No successful backup found in the given find_time

##################### edit below ################################

# Path to logs. Default: C:\\ProgramData\\Veeam\\Backup\\. Double backslashes are required by Python.
path='C:\\ProgramData\\Veeam\\Backup\\'

# find_time (hours) - time window to search successful backup job. Default 24 hours, menas
# the script will search completed backups ended in the last 24 hours.
find_time=24

### DO NOT edit below, unless you know what you're doing :) ###
###############################################################


def readFile(logfile):
# returns content of the file
    if os.path.exists(logfile):
        file1 = open(logfile, 'r')
        lines = file1.readlines()
    else:
        print(2)
        sys.exit()
    return lines


def readLine(number, logfile):
# returns line of the given number
    if os.path.exists(logfile):
        file1 = open(logfile, 'r')
        lines = file1.readlines()[number]
    else:
        print(2)
        sys.exit()
    return lines


def findLastStartedJob(text):
# returns last started backup job session id and its start time

    expr="\[\d{2}.\d{2}.\d{4} \d{2}:\d{2}:\d{2}] <..> Info.........STARTBACKUPJOB"

    jobs=[]
    count=0

    for line in text:
        found = re.search(expr, line)
        count +=1
        task_id=""
        job_name=""
        if(found):
            task_id=readLine(count+3, path)
            job_name=readLine(count+14, path)
            found = False
            found = re.search(backup_job_name, job_name)

            if(found):
                jobs.append(task_id)
            else:
                print(2)
                sys.exit()

    if not jobs:
        print(2)
        sys.exit()

    job=jobs[-1]
    elements = job.split(" ")
    backup_start_time=StripDateAndTime(job)
    session_id=elements[-1]
    session_id = session_id.strip('\n')
    answer=[session_id, backup_start_time]
    return answer


def StripDateAndTime(line):
# returns datetime object

    date_found = re.search("\d{2}.\d{2}.\d{4}", line)
    time_found = re.search("\d{2}:\d{2}:\d{2}", line)

    if(date_found):
        l=date_found.group() +" "+ time_found.group()
        d = datetime.datetime.strptime(l, '%d.%m.%Y %H:%M:%S')
        return d
    else:
        print(2)
        sys.exit()



def FindCompletedBackupJob(text, session_id, start_time):
# returns exit code

    expr="\[\d{2}.\d{2}.\d{4} \d{2}:\d{2}:\d{2}] <..> Info.+Job session '"+session_id+"' has been completed, status:.+"
    expr_warning="status: \'Warning\'"
    expr_success="status: \'Success\'"

    delta = datetime.timedelta(hours=find_time)
    now=datetime.datetime.now(tz=None)
    max_expected_backup_end_time=start_time+delta

    for line in text:
        found = re.search(expr, line)
        if(found):
            found=re.search(expr_success, line)
            if(found):
                return 0

            found=re.search(expr_warning, line)
            if(found):
                return 1

    if(max_expected_backup_end_time > now):
        return 0
    else:
        return 2


# main program
if(len(sys.argv) < 2):
    print("Missing argument. Usage: python veem_check.py [backup_job_name]")
    sys.exit()
else:
    backup_job_name=str(sys.argv[1])


# add '\' at the end of the path if missing
if(path[-1:] != "\\"):
    path=path+"\\"

# create full path to the log file
path=path+backup_job_name+'\\''Job.'+backup_job_name+'.Backup.log'

file = readFile(path)
started_job=findLastStartedJob(file)
session_id=started_job[0]
start_time=started_job[1]
completed_job=FindCompletedBackupJob(file, session_id, start_time)
print(completed_job)
