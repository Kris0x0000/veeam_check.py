Script for getting job status in Veeam Backup & Replication


Usage via command line: python veeam_check.py backup_job_name.

Usage as Zabbix item: veeam_check[backup_job_name].

Configuration example: UserParameter=veeam_check[*],python C:\scripts\veeam_check.py $1.

Requirements: Python 3.x installed on the target.

Exit codes: 0 - Successful backup, 1 - Backup completed with warings, 2 - No successful backup found in the given find_time