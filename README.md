# Script for getting job status in Veeam Backup & Replication

## Usage

- Usage via command line: 
```
python veeam_check.py backup_job_name backup_copy_job_name (optional).
```

- Usage as Zabbix item: 
```
veeam_check[backup_job_name, backup_copy_job_name (optional)].
```

- Exit codes: 0 - Successful backup, 1 - Backup completed with warings, 2 - No successful backup found in the given find_time


## Configuration in Zabbix

- Configuration example: 
```
UserParameter=veeam_check[*],"python" "C:\scripts\veeam_check.py" $1 $2.
```

- Requirements: Python 3.x installed on the target machine. Please **DO NOT** install Python inside C:\Users\ (which is the default installation path!) becouse Zabbix Agent won't have access to it.
It is safe to to install Python in C:\ or C:\Program Files.


