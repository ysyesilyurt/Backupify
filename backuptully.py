#!/usr/bin/env python3
import cmd
import json
import os
import sys

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
            self.d = "{}/backups".format(os.environ['HOME'])
            self.targets = set()
            self.latest = None
            self.do_save()
            if not os.path.isdir(self.d):
                os.makedirs(self.d)
        self.updated = False

    def emptyline(self):
        pass

    def do_SetDestination(self, args):
        """Method for setting destination folder"""
        # temp = self.d
        self.d = args
        self.updated = True
        if not os.path.isdir(args):
            os.makedirs(args)
            # TODO: move old content

    def do_SetBackupPeriod(self, args):
        """Method for setting backup period for backup script"""
        if args in self.macros or args.isdigit():
            self.bp = args
            self.updated = True
            # TODO: Handle anacron
        else:
            print("Please enter a valid Backup Period (in days)")

    def do_help(self, arg):
        # TODO: Implement this method
        pass

    def do_list(self, args=None):
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
            hierarchy = args.split('/')
            searchPath = ""
            flag = False
            for path in hierarchy:
                searchPath += path + '/'
                if searchPath in self.targets or searchPath[:-1] in self.targets:
                    flag = True
                    break
            if not flag:
                self.targets.add(args)
                self.updated = True
            else:
                print("A parent directory named {} is already in targets, so this path will not be added to "
                      "targets.".format(searchPath))
        else:
            print("No such file or directory named {}".format(args))

    def do_rm(self, args):
        """Method for removing target from targetList"""
        if args in self.targets:
            self.targets.remove(args)
            self.updated = True
        elif args + '/' in self.targets:
            self.targets.remove(args + '/')
            self.updated = True
        elif args == '*':
            self.targets = set()
            self.updated = True
        else:
            print("No such file or directory named {} in current targetList".format(args))

    def do_save(self, args=None):
        """Method for saving current configuration"""
        self.updated = False
        paths = ""
        for path in self.targets:
            paths += path + " "
        with open("btConf.json", "w") as conf:
            data = {"bp": self.bp, "latest": self.latest, "d": self.d, "targets": paths[:-1]}
            json.dump(data, conf, indent=2)

    def load(self):
        """Method for loading current configuration from persistent storage"""
        with open("btConf.json", "r") as conf:
            data = json.load(conf)
            self.bp = data["bp"]
            self.latest = data["latest"]
            self.d = data["d"]
            paths = data["targets"]
            self.targets = set(paths.split(" "))

    def do_EOF(self, args=None):
        if self.updated:
            print("You have unsaved changes in your configuration, do you want to save them before you proceed? [Y/n]",
                  end=" ")
            proceed = str(input())
            if proceed == "" or proceed == "Y" or proceed == "y":
                self.do_save(args)
        print()
        exit(0)


if __name__ == "__main__":
    try:
        UserLoop().cmdloop()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
    except Exception as e:
        with open("btError.log", "w+") as errFile:
            print(e)
        exit(2)
