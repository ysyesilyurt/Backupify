#!/usr/bin/env python3
import cmd
import json
import os

# TODO: Inform user about default values
# TODO: Make a colored CLI -- user friendly
# TODO: Establish an autocompleting structure in rm and add
# TODO: Improve functionality?


class UserLoop(cmd.Cmd):
    """Class for dynamic interpreter of user"""
    def __init__(self):
        super(UserLoop, self).__init__()
        self.prompt = "> "
        self.intro = "Welcome to Backuptully!\nPlease type help to see available commands."
        self.macros = {"@daily", "@weekly", "@monthly"}
        if os.path.exists("btConf.json"):
            self.load()
        else:
            self.bp = "@daily"
            self.d = "~/backups"
            self.targets = set()
            self.latest = None

    def emptyline(self):
        pass

    def do_SetDestination(self, args):
        """Method for setting destination folder"""
        if os.path.isdir(args):
            self.d = args
        else:
            print("No such directory named {}".format(args))

    def do_SetBackupPeriod(self, args):
        """Method for setting backup period for backup script"""
        if args in self.macros or args.isdigit():
            self.bp = args
        else:
            print("Please enter a valid Backup Period (in days)")

    def do_help(self, arg):
        # TODO: Implement this method
        pass

    def do_list(self, args):
        """Method for listing current configuration"""
        if self.latest:
            print("Last backup was at {}".format(self.latest))
        else:
            print("No backup has been taken yet")
        if self.bp not in self.macros:
            print("Current Backup Period: Once in {} days".format(self.bp))
        else:
            print("Current Backup Period: {}".format(self.bp))
        print("Destination folder {}".format(self.d))
        print("Current Backup targets are:", end=" ")
        for path in self.targets:
            print(path, end=" ")
        print()

    def do_add(self, args):
        """Method for adding target to targetList"""
        if os.path.exists(args):
            self.targets.add(args)
        else:
            print("No such file or directory named {}".format(args))

    def do_rm(self, args):
        """Method for removing target from targetList"""
        if args in self.targets:
            self.targets.remove(args)
        else:
            print("No such file or directory named {} in current targetList".format(args))

    def do_save(self, args):
        """Method for saving current configuration"""
        paths = ""
        for path in self.targets:
            paths += path + " "
        with open("btConf.json", "w") as conf:
            data = {"bp": self.bp, "latest": self.latest, "d": self.d, "targets": paths[:-1]}
            json.dump(data, conf, indent=2)

    def load(self):
        """Method for loading current configuration from persistent storage - JSON file"""
        with open("btConf.json", "r") as conf:
            data = json.load(conf)
            self.bp = data["bp"]
            self.latest = data["latest"]
            self.d = data["d"]
            paths = data["targets"]
            self.targets = set(paths.split(" "))

    def do_EOF(self, args):
        print()
        exit(0)


if __name__ == "__main__":
    UserLoop().cmdloop()
