import os
import re
import time
import sys
import datetime

# Usage via command line: python veeam_check.py backup_job_name backup_copy_job_name (optional).
# Usage as Zabbix item: veeam_check[backup_job_name, backup_copy_job_name (optional)] .
# Configuration example: UserParameter=veeam_check[*],python C:\scripts\veeam_check.py $1 $2.
# Requirements: Python 3.x installed on the target.
# Exit codes: 0 - Successful backup, 1 - Backup completed with warings, 2 - No successful backup found in the given find_time

##################### edit below ################################

# backup_path to backup .zip files.
backup_path='C:\\SQL_Backup\\'
# files_max_age in hours. When there are no files newer than n hours in the backup_path the script exits with 2 code.
files_max_age=30

# Path to logs. Default: C:\\ProgramData\\Veeam\\Backup\\. Double backslashes are required by Python.
base_path='C:\\ProgramData\\Veeam\\Backup\\'
# find_time (hours) - time window to search successful backup job. Default 24 hours, menas
# the script will search completed backups ended in the last 24 hours.
find_time=30
max_duration=5

# diag - set it to 'True' for troubleshooting.
diag=False

### DO NOT edit below, unless you know what you're doing :) ###
###############################################################

def CheckFileModTime():

    global backup_path
    global files_max_age
    
    os.chdir(backup_path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    flist=[]
    extensions = (".zip")
    for file in files:
        if file.endswith(extensions):
            flist.append(file)

    oldest = flist[0]
    newest = flist[-1]

    m_time=os.path.getmtime(backup_path+newest)
    delta = datetime.timedelta(hours=files_max_age)

    if(m_time+delta.total_seconds() < datetime.datetime.now(tz=None).timestamp()):
        print(2)
        sys.exit()

def readFile(logfile):
	
# returns content of the file
	if os.path.exists(logfile):
		file1 = open(logfile, 'r')
		lines = file1.readlines()
	else:
		if(diag):
			print('Cannot open the logfile: '+logfile)
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


def findLastStartedJob(path, text, expr):
# returns last started backup job session id and its start time

	jobs=[]
	count=0

	for line in text:
		found = re.search(expr, line)
		count +=1
		task_id=""
		job_name=""
		if(found):
			task_id=readLine(count+3, path)
			jobs.append(task_id)

	if not jobs:
		return [0,0]

	job=jobs[-1] # take the last one (the newest)
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


def FindCompletedBackupJob(text, session_id, start_time, expr):
# returns exit code
# Job session '38129ee8-e20f-4912-ae5e-f0176077f0f9' has been completed, status: 'Success'

	if(diag):
		print('\nexpr_success: '+expr)

	expr_warning="status: \'Warning\'"
	expr_success="status: \'Success\'"
	expr_failed="status: \'Failed\'"

	delta = datetime.timedelta(hours=find_time+max_duration)
	now=datetime.datetime.now(tz=None)
	max_expected_backup_end_time=start_time+delta
	#print('max_expected_backup_end_time',max_expected_backup_end_time)

	for line in text:
	
		found = re.search(expr, line)
		if(found):
			job_complete_time=StripDateAndTime(found.group(0))
			if(max_expected_backup_end_time > job_complete_time):
			
				found=re.search(expr_success, line)
				if(found):
					if(diag):
						print('\nexpr_success found')
						
					return 0  # return this if expr_success found

				found=re.search(expr_warning, line)
				if(found):
					if(diag):
						print('\nexpr_warning found')
					return 1  # return this if expr_warning found
					
				found=re.search(expr_failed, line)
				if(found):
					if(diag):
						print('\nexpr_failed found')
					return 2  # return this if expr_failed found
			else:
				if(diag):
						print('\nmax_expected_backup_end_time is exceeded ')
						print('\nstart time: '+start_time.strftime("%d/%m/%Y, %H:%M:%S"))
						print('\nmax_expected_backup_time: ' + max_expected_backup_end_time.strftime("%d/%m/%Y, %H:%M:%S"))
				return 2  # return this if max_expected_backup_end_time is exceeded
	if(diag):
		print('none')

	return 2  # return this is none of above is satisfied



def BackupJobOption():
	global base_path
	
	# add '\' at the end of the path if missing
	if(os.name != 'posix'):
		if(base_path[-1:] != "\\"):
			base_path=base_path+"\\"
	# create full path to the log file
	if(os.name != 'posix'):
		path=base_path+backup_job_name+'\\'+'Job.'+backup_job_name+'.Backup.log'
	else:
		path=base_path+backup_job_name+'/'+'Job.'+backup_job_name+'.Backup.log'
		
	
	if not os.path.isfile(path):
		if(os.name != 'posix'):
			path=base_path+backup_job_name+'\\'+'Job.'+backup_job_name+'.log'
		else:
			path=base_path+backup_job_name+'/'+'Job.'+backup_job_name+'.log'
		

	file = readFile(path)
	expr="\[\d{2}\.\d{2}\.\d{4} \d{2}\:\d{2}\:\d{2}] <\d{2}> Info\s+START.+"
	# [06.06.2022 22:00:21] <01> Info         [Session] Id '38129ee8-e20f-4912-ae5e-f0176077f0f9', State 'Working'.
	started_job=findLastStartedJob(path, file, expr)
	if(diag):
		print('\nLastStartedJob: '+started_job[0] + ' at: '+started_job[1].strftime("%d/%m/%Y, %H:%M:%S"))
	session_id=started_job[0]
	start_time=started_job[1]
	expr="\[\d{2}\.\d{2}\.\d{4} \d{2}\:\d{2}\:\d{2}] <\d{2}> Info\s+Job session '"+session_id+"' has been completed, status:.+"
	
	completed_job=FindCompletedBackupJob(file, session_id, start_time, expr)
  
	print(completed_job)    


def BackupCopyJobOption():
	global base_path
	
	# add '\' at the end of the path if missing
	if(base_path[-1:] != "\\"):
		base_path=base_path+"\\"

	# create full path to the log file
	print(os.name == "posix")
	if(os.name != "posix"):
		path=base_path+backup_copy_job_name+'\\'+backup_job_name+'\\'+'Job.'+backup_job_name+'.BackupSync.log'
	else:
		path=base_path+backup_copy_job_name+'//'+backup_job_name+'//'+'Job.'+backup_job_name+'.BackupSync.log'

	file = readFile(path)
	# [14.08.2021 17:35:23] <01> Info       START  
	expr="\[\d{2}\.\d{2}\.\d{4} \d{2}\:\d{2}\:\d{2}] <\d{2}> Info\s+START.+"
	started_job=findLastStartedJob(path, file, expr)
	session_id=started_job[0]
	start_time=started_job[1]
	# [18.08.2021 18:02:45] <01> Info         Job session '16a6046b-eac7-4f4f-909e-3830ee2815d7' has been completed, status: 'Success'
	expr="\[\d{2}\.\d{2}\.\d{4} \d{2}\:\d{2}\:\d{2}] <\d{2}> Info\s+Job session '"+session_id+"' has been completed, status:.+"
	completed_job=FindCompletedBackupJob(file, session_id, start_time, expr)
	print(completed_job) 


# main program

CheckFileModTime()

if(len(sys.argv) < 2):
	print("Missing argument. Usage: python veem_check.py [backup_job_name]")
	sys.exit()
elif(len(sys.argv) == 3):
	# find backup copy job
	backup_job_name=str(sys.argv[1])
	backup_copy_job_name=str(sys.argv[2])
	BackupCopyJobOption()
	
elif(len(sys.argv) == 2):
	# find backup job
	backup_job_name=str(sys.argv[1])
	BackupJobOption()
	


