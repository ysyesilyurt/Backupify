#!/usr/bin/env python3
import datetime
import json
import os


def load():
    with open("btConf.json", "r") as conf:
        data = json.load(conf)
    return data


def save(data):
    with open("btConf.json", "w") as conf:
        json.dump(data, conf, indent=2)


if __name__ == "__main__":
    confData = load()
    DESTINATION = confData["d"]
    TARGETS = confData["targets"]
    today = datetime.date.today().strftime("%Y-%m-%d")

    #TODO: Get the backup

    confData["latest"] = today
    save(confData)


