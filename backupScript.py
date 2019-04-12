#!/usr/bin/env python3
import datetime
import json
import os
import sys
from subprocess import Popen


def load():
    with open(sys.path[0] + "/backupifyConf.json", "r") as conf:
        data = json.load(conf)
    return data


def save(data):
    with open(sys.path[0] + "/backupifyConf.json", "w") as conf:
        json.dump(data, conf, indent=2)


if __name__ == "__main__":
    try:
        confData = load()
        DESTINATION = confData["destination"]
        TARGETS = confData["targets"].split(" ")
        if TARGETS:
            today = datetime.date.today().strftime("%Y-%m-%d")
            p = Popen(['tar', '-czPf', "{0}BACKUPIFY~{1}.tgz".format(DESTINATION, today)] + TARGETS)
            retCode = p.wait()
            if not retCode:
                confData["latest"] = today
                confData["count"] += 1
                save(confData)
                with open(sys.path[0] + "/backupify.log", "a") as log:
                    log.write("Backup taken at {0} to {1}".format(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
                                                                  DESTINATION) + '\n')
                if (confData["count"] % int(confData["arcPeriod"])) == 0:
                    backups = os.listdir(DESTINATION)
                    backups = [DESTINATION + backup for backup in backups]
                    oldestBackup = min(backups, key=os.path.getctime)
                    os.remove(oldestBackup)
                    with open(sys.path[0] + "/backupify.log", "a") as log:
                        log.write(
                            "Oldest backup {0} removed at {1} from {2}".format(oldestBackup,
                                datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), DESTINATION) + '\n')
            else:
                with open(sys.path[0] + "/backupify.log", "a") as log:
                    log.write("tar error from backupScript.py at {}".format(
                        datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")) + " tar returned {} "
                                                                                 "code".format(retCode) + '\n')
                exit(2)
        exit(0)
    except Exception as e:
        with open(sys.path[0] + "/backupify.log", "a") as log:
            log.write("Error from backupScript.py at {}".format(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")) +
                      ": " + str(e) + '\n')
        exit(2)
