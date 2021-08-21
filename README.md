# Script for getting job status in Veeam Backup & Replication

## Usage

Usage via command line: python veeam_check.py backup_job_name backup_copy_job_name (optional).

Usage as Zabbix item: veeam_check[backup_job_name, backup_copy_job_name (optional)].

Configuration example: UserParameter=veeam_check[*],"python" "C:\scripts\veeam_check.py" $1 $2.

Requirements: Python 3.x installed on the target.

Exit codes: 0 - Successful backup, 1 - Backup completed with warings, 2 - No successful backup found in the given find_time

## Known issues

**Can't find a default Python error**

**Issue:** When this issue occurs in Windows usually this is caused by installing python inside user's profile. 

**Fix:** Install python inside C:\ ,restart Zabbix Service.

