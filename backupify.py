#!/usr/bin/env python3
import cmd
import datetime
import json
import os
import re
import sys
from subprocess import Popen, call


VERSION = "1.0"


class UserLoop(cmd.Cmd):
    """Class for dynamic interpreter of user"""
    def __init__(self):
        super(UserLoop, self).__init__()
        self.prompt = "Backupify> "
        self.intro = "Welcome to Backupify {}!\nPlease type help or ? to see available commands and their " \
                     "settings.\nType documentation for further information about Backupify".format(VERSION)
        self.macros = {"@daily", "@weekly", "@monthly"}
        if os.path.exists(sys.path[0] + "/backupifyConf.json"):
            self.load()
        else:
            self.period = "@daily"
            self.destination = "{}/backups/".format(os.environ['HOME'])
            self.targets = set()
            self.latest = None
            self.count = 0
            if not os.path.isdir(self.destination):
                os.makedirs(self.destination)
            with open("/etc/anacrontab", "r") as tab:
                if "Backupify" in tab.read():
                    loc = re.sub("/", "\\/", sys.path[0] + "/backupScript.py")
                    newEntry = "{0}\t0\tBackupify\t{1}".format(self.period, loc)
                    p = Popen(['sed', '-i', "s/.*Backupify.*/{}/g".format(newEntry), "/etc/anacrontab"])
                    p.wait()
                else:
                    with open("/etc/anacrontab", "a") as anacron:
                        newEntry = "{0}\t0\tBackupify\t{1}".format(self.period, sys.path[0] + "/backupScript.py")
                        anacron.write(newEntry + '\n')
            self.save()
            print("First time configuration, all values are default, you can configure all the settings with available "
                  "commands.")

    def emptyline(self):
        pass

    def do_setDestination(self, args):
        """Method for setting destination folder"""
        if args:
            if not os.path.isdir(args):
                print("No direcrory named {} seems to exist. Do you create it and proceed? [Y/n]".format(args), end=" ")
                proceed = str(input())
                if not(proceed == "" or proceed == "Y" or proceed == "y"):
                    return
                os.makedirs(args)
            temp = self.destination
            if args[-1] != '/':
                args += '/'
            self.destination = args
            call("mv {0}* {1}".format(temp, args), shell=True)
            os.rmdir(temp)
            self.save()
            print("Changed destination folder to {0} and successfully moved all backups under {1} to "
                  "{0}".format(args, temp))
        else:
            print("Please enter a valid path.")

    def do_setPeriod(self, args):
        """Method for setting backup period for backup script"""
        if args in self.macros or args.isdigit():
            self.period = args
            loc = re.sub("/", "\\/", sys.path[0] + "/backupScript.py")
            newEntry = "{0}\t0\tBackupify\t{1}".format(self.period, loc)
            p = Popen(['sed', '-i', "s/.*Backupify.*/{}/g".format(newEntry), "/etc/anacrontab"])
            p.wait()
            self.save()
        else:
            print("Please enter a valid Backup Period (in days).")

    def do_list(self, args=None):
        """Method for listing current configuration"""
        if self.latest:
            print("Last backup was at {}".format(self.latest))
        print("{} backups were taken up to now".format(self.count))
        if self.period not in self.macros:
            print("Current Backup Period: Once in {} days".format(self.period))
        else:
            print("Current Backup Period: {}".format(self.period))
        print("Destination folder {}".format(self.destination))
        print("Current Backup targets are:", end="")
        for path in self.targets:
            print(path, end=" ")
        print()

    def do_add(self, args):
        """Method for adding target to targetList"""
        if os.path.exists(args):
            hierarchy = args.split('/')
            searchPath = ""
            flag = False
            for path in hierarchy:
                if not path:
                    continue
                searchPath += path + '/'
                if searchPath in self.targets or searchPath[:-1] in self.targets:
                    flag = True
                    break
            if not flag:
                self.targets.add(args)
                self.save()
            else:
                print("A parent directory named {} is already in targets, so this path will not be added to "
                      "targets.".format(searchPath))
        else:
            print("No such file or directory named {}".format(args))

    def do_rm(self, args):
        """Method for removing target from targetList"""
        if args in self.targets:
            self.targets.remove(args)
            self.save()
        elif args + '/' in self.targets:
            self.targets.remove(args + '/')
            self.save()
        elif args == '*':
            self.targets = set()
            self.save()
        else:
            print("No such file or directory named {} in current targetList".format(args))

    def save(self, args=None):
        """Method for saving current configuration"""
        paths = ""
        for path in self.targets:
            if not path:
                continue
            paths += path + " "
        with open(sys.path[0] + "/backupifyConf.json", "w") as conf:
            data = {"period": self.period, "latest": self.latest, "count": self.count, "destination": self.destination,
                    "targets": paths[:-1]}
            json.dump(data, conf, indent=2)

    def load(self):
        """Method for loading current configuration from persistent storage"""
        with open(sys.path[0] + "/backupifyConf.json", "r") as conf:
            data = json.load(conf)
            self.period = data["period"]
            self.latest = data["latest"]
            self.count = data["count"]
            self.destination = data["destination"]
            paths = data["targets"]
            self.targets = set(paths.split(" "))

    def do_EOF(self, args=None):
        print()
        exit(0)

    def do_documentation(self, args=None):
        print("\nBackupify {}".format(VERSION))
        print("==================================\n")
        print("Backupify is a Command Line Interface Application for getting periodic backups of specific targets.")
        print("It provides an Interpreter for user to configure app settings via various commands (type help to see "
              "them)")
        print("\nConfigurable settings are:\n\t\tBackup Targets(adding and removing them)\n"
              "\t\tBackup destination\n\t\tBackup period\n\t\tConfigurations then saved into a Json file named "
              "'backupifyConf.json' and loaded/saved from there.\n")
        print("Backupify uses 'anacron' for scheduling periodic backups. 'anacron' is a program that executes "
              "commands periodically, with a frequency specified in 'days'. Unlike 'cron' it does not assume that the "
              "machine is running continuously (for more information visit manual page of 'anacron'). Thanks to this"
              "feature of anacron, Backupify is able to get backups periodically no matter machine runs or not.\n")
        print("Since anacrontab needs to be configured only with sudo privileges, Backupify needs to be executed "
              "with sudo.\n")
        print("'anacron' is provided with 'backupScript' and whenever anacron executes it, script reads the current "
              "configuration from 'backupifyConf.json' file compresses all targets into a '.tgz' with timestamp"
              " into configured destination. Therefore it is "
              "VITAL for backupifyConf.json to exist and somehow if it gets deleted it will be reproduced with default "
              "values and all configuration will be discarded.\n")
        print("All backup and error logs will be reported into log file named 'backupify.log' ('anacron' also logs "
              "activity to /var/log/syslog, so logs can also be seen from there).\n")
        print("Visit for Original Repository github.com/ysyesilyurt/Backupify\nMIT © ysyesilyurt 2019\n")

    def do_help(self, arg):
        print("\tAvailable Commands")
        print("====================================")
        print("\nadd\t--\tAdds new path(target) to backup list.")
        print("\t\tIf any parent directory of given target is present in backup list already, then new path "
              "will not be added to backup list.")
        print("\nrm\t--\tRemoves an existing path(target) from backup list.")
        print("\t\tWildcard '*' removes all existing paths.")
        print("\nlist\t--\tLists current configuration and general information about old backups.")
        print("\nsetDestination\t--\tSets the new destination folder for backups.")
        print("\t\t\tMoves all old backups from old destination directory to new one and then removes the old.")
        print("\t\t\tIf destination directory with given name does not exist it creates an empty directory "
              "with given name.")
        print("\t\t\tDefault value -- {}".format("{}/backups/".format(os.environ['HOME'])))
        print("\nsetPeriod\t--\tSets the new backup period for backups.")
        print("\t\t\tBackup period needs to be a digit corresponding to once in <digit> days or one of "
              "@daily, @weekly, @monthly macros.\n\t\t\tSee manual page of 'anacron' for further information.")
        print("\t\t\tDefault value -- @daily")
        print("\nTo gather further information about Backupify type documentation "
              "or visit github.com/ysyesilyurt/Backupify\n")


if __name__ == "__main__":
    try:
        if os.geteuid():
            print("It seems like you did not run Backupify with sudo privileges.\nTo be able to set backup period"
                  " to anacron, Backupify needs sudo privileges. Please run Backupify again with sudo.")
            exit(1)
        else:
            UserLoop().cmdloop()
    except KeyboardInterrupt:
        print()
        exit(1)
    except Exception as e:
        print("An error occured, logging to logfile..")
        with open(sys.path[0] + "/backupify.log", "a") as log:
            log.write("Error from backupify.py at {}".format(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")) +
                      ": " + str(e) + '\n')
        exit(2)
