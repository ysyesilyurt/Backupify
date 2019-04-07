#!/usr/bin/env python3
import datetime
import json
from subprocess import Popen


def load():
    with open("btConf.json", "r") as conf:
        data = json.load(conf)
    return data


def save(data):
    with open("btConf.json", "w") as conf:
        json.dump(data, conf, indent=2)


if __name__ == "__main__":
    try:
        confData = load()
        DESTINATION = confData["d"]
        TARGETS = confData["targets"]
        today = datetime.date.today().strftime("%Y-%m-%d")
        p = Popen(['tar', '-czPf', "{0}BT~{1}.tgz".format(DESTINATION, today), TARGETS])
        p.wait()
        confData["latest"] = today
        save(confData)
        exit(0)
    except Exception as e:
        with open("btError.log", "a") as errFile:
            errFile.write("From backupScript at {}".format(datetime.date.today().strftime("%Y-%m-%d")) + ": "
                          + str(e) + '\n')
        exit(2)



