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
        if TARGETS:
            today = datetime.date.today().strftime("%Y-%m-%d")
            p = Popen(['tar', '-czPf', "{0}BT~{1}.tgz".format(DESTINATION, today), TARGETS])
            p.wait()
            confData["latest"] = today
            confData["count"] += 1
            save(confData)
        exit(0)
    except Exception as e:
        print("An error occured, logging to logfile..")
        with open("btError.log", "a") as errFile:
            errFile.write("From backuptully at {}".format(datetime.datetime.now().strftime("%Y,%m,%d,%H,%M,%S")) + ": "
                          + str(e) + '\n')
        exit(2)



