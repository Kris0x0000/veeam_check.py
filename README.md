Script for getting job status in Veem Backup & Replication

# Usage via command line: python veem_check.py backup_job_name.
# Usage as Zabbix item: veem_check[backup_job_name].
# Configuration example: UserParameter=veem_check[*],python C:\scripts\veem_check.py $1.
# Requirements: Python 3.x installed on the target.
# Exit codes: 0 - Successful backup, 1 - Backup completed with warings, 2 - No successful backup found in the given find_time