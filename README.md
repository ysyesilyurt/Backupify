# Backupify
Command Line Interface Application for getting periodic backups of specific targets.

[1]: https://github.com/ysyesilyurt/Backupify/blob/master/images/1.png  
[2]: https://github.com/ysyesilyurt/Backupify/blob/master/images/2.png
[3]: https://github.com/ysyesilyurt/Backupify/blob/master/images/3.png

## Overview
Backupify provides an Interpreter for user to configure app settings via various commands and with the help of ```anacron```, it gets periodic backups of user-chosen
targets with user-configured settings.

![alt text][1]

Users can _add/remove targets(paths)_, _set/change backup destinations_, _set/change backup periods_ via commands defined for user. Users can display available commands and documentation by `help` command and `documentation`
command respectively. 

![alt text][2]![alt text][3]

All the configurations for the app are saved in and loaded from `backupifyConf.json` file. 

Backupify uses `anacron` for scheduling periodic backups. `anacron` is a program that executes commands periodically, with a frequency 
specified in _days_. Unlike `cron` it does not assume that the machine is running continuously (for more information visit manual page of `anacron`).
Thanks to this feature of `anacron`, Backupify is able get backups periodically no matter machine runs or not. Since `anacrontab` needs to be configured 
only with `sudo` privileges, Backupify needs to be executed with `sudo`.

`anacron` is provided with `backupScript` and whenever `anacron` executes it, script reads the current configuration from `backupifyConf.json` file and compresses 
all targets with `.tgz` with timestamp into configured destination. Therefore it is **VITAL** for `backupifyConf.json` to exist and somehow if it gets deleted it will be reproduced with 
default values(for default values see manuals for commands with `help`) and all configuration will be discarded.
              
All backup and error logs will be reported into log file named `backupify.log` (`anacron` also logs activity to /var/log/syslog, so logs can also be seen
from there).

## Requirements
* Python3.6+
* anacron

## Installation and Usage
Make sure that your system has specified requirements. Then clone the repository
```
git clone https://github.com/ysyesilyurt/Backupify/
```
You can either make scripts executable(`Shebangs` are defined no problems there) or run with `python3`, I prefer directly executing the script
```
chmod +x backupify.py
chmod +x backupScript.py
```
and run
```
sudo ./backupify.py
```
On first time run, Backupify will create `backupifyConf.json` with initial default configuration and an entry with to `anacrontab` will be appended regarding
Backupify.

## Contribution
Feel free to open an issue if you spot a bug. On the other hand for enhancements and other stuff, some issues for several reasons may remain open,
 if that is the case and your reasoning aren't listed in there feel free to open an issue about that too. 
 
 **Always keep in mind that a backup may save you from a lot of nasty stuff, I learnt it from the hard way once, dont be like me :blush:.** 