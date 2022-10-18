<<<<<<< HEAD
# Script for getting job status in Veeam Backup & Replication

## Usage

- Usage via command line: 
```
python veeam_check.py [backup_job_name] [backup_copy_job_name (optional)].
```

- Testing with Zabbix Agent:
```
zabbix_agentd -c C:\Program Files\Zabbix Agent\zabbix_agentd.conf -t veeam_check [backup_job_name] [backup_copy_job_name (optional)]
```
- Exit codes: 0 - Successful backup, 1 - Backup completed with warings, 2 - No successful backup found in the given find_time


## Configuration in Zabbix

- Configuration example (zabbix_agentd.conf): 
```
UserParameter=veeam_check[*],"python" "C:\scripts\veeam_check.py" $1 $2.
```
- Zabbix Item for checking backup_job_name:
```
veeam_check[backup_job_name]
```
- Zabbix Item for checking **backup_copy_job_name**:
```
veeam_check[backup_job_name, backup_copy_job_name].
```
Remember that you need to type both **backup_job_name** and **backup_copy_job_name** when checking status of **backup_copy_job_name**. This is becouse Veeam 
Backup Copy Job is always created for individual Backup Job.

## Requirements

- Python 3.x installed on the target machine. Please **DO NOT** install Python inside C:\Users\ (which is the default installation path!) becouse Zabbix Agent won't have access to it.
It is safe to to install Python in C:\ or C:\Program Files.


=======
# Script for getting job status in Veeam Backup & Replication

## Usage

- Usage via command line: 
```
python veeam_check.py [backup_job_name] [backup_copy_job_name (optional)].
```

- Testing with Zabbix Agent:
```
zabbix_agentd -c C:\Program Files\Zabbix Agent\zabbix_agentd.conf -t veeam_check [backup_job_name] [backup_copy_job_name (optional)]
```
- Exit codes: 0 - Successful backup, 1 - Backup completed with warings, 2 - No successful backup found in the given find_time


## Configuration in Zabbix

- Configuration example (zabbix_agentd.conf): 
```
UserParameter=veeam_check[*],"python" "C:\scripts\veeam_check.py" $1 $2.
```
- Zabbix Item for checking backup_job_name:
```
veeam_check[backup_job_name]
```
- Zabbix Item for checking **backup_copy_job_name**:
```
veeam_check[backup_job_name, backup_copy_job_name].
```
Remember that you need to type both **backup_job_name** and **backup_copy_job_name** when checking status of **backup_copy_job_name**. This is becouse Veeam 
Backup Copy Job is always created for an individual Backup Job.

## Requirements

- Python 3.x installed on the target machine. Please **DO NOT** install Python inside C:\Users\ (which is the default installation path!) becouse Zabbix Agent won't have access to it.
It is safe to to install Python in C:\ or C:\Program Files.


>>>>>>> 2801acadf6088ece49f2d447fb52a83ee7c792bb
