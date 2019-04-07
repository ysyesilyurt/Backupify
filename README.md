# BackupTully
Command Line Interface Application for getting periodic backups of specific targets.

## Overview
BackupTully provides an Interpreter for user to configure app settings via various commands and with the help of ```anacron```, it gets periodic backups of user-chosen
targets with user-configured settings.

Users can _add/remove targets(paths)_, _set/change backup destinations_, _set/change backup periods_ via commands defined for user. Users can display available commands and documentation by `help` command and `documentation`
command respectively. 

All the configurations for the app are saved in and loaded from `btConf.json` file. 

BackupTully uses `anacron` for scheduling periodic backups. `anacron` is a program that executes commands periodically, with a frequency 
specified in _days_. Unlike `cron` it does not assume that the machine is running continuously (for more information visit manual page of `anacron`).
Thanks to this feature of `anacron`, BackupTully is able get backups periodically no matter machine runs or not. Since `anacrontab` needs to be configured 
only with `sudo` privileges, BackupTully needs to be executed with `sudo`.

`anacron` is provided with `backupScript` and whenever `anacron` executes it, script reads the current configuration from `btConf.json` file and compresses 
all targets with `.tgz` with timestamp into configured destination. Therefore it is **VITAL** for `btConf.json` to exist and somehow if it gets deleted it will be reproduced with 
default values(for default values see manuals for commands with `help`) and all configuration will be discarded.
              
All backup and error logs will be reported into log file named `bt.log` (`anacron` also logs activity to /var/log/syslog, so logs can also be seen
from there).

## Requirements
* Python3.6+
* anacron

## Installation and Usage
Make sure that your system has specified requirements. Then clone the repository
```
git clone https://github.com/ysyesilyurt/BackupTully/
```
You can either make scripts executable(`Shebangs` are defined no problems there) or run with `python3`, I prefer directly executing the script
```
chmod +x backupTully.py
chmod +x backupScript.py
```
and run
```
sudo ./backupTully.py
```
On first time run, BackupTully will create `btConf.json` with initial default configuration and an entry with to `anacrontab` will be appended regarding
BackupTully.

## Contribution
Feel free to open an issue if you spot a bug. On the other hand for enhancements and other stuff, some issues for several reasons may remain open,
 if that is the case and your reasoning aren't listed in there feel free to open an issue about that too. 
 
 **Always keep in mind that a backup may save you from a lot of nasty stuff, I learnt it from the hard way once, dont be like me :blush:.** 