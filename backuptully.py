#!/usr/bin/env python3
import cmd


class UserLoop(cmd.Cmd):
    """Class for dynamic interpreter of user"""
    def __init__(self):
        super(UserLoop, self).__init__()
        pass

    def emptyline(self):
        pass

    def do_set(self, args):
        """Method for setting configurations"""
        pass

    def do_help(self, arg):
        pass

    def do_list(self):
        """Method for listing current configuration"""
        pass

    def do_add(self, args):
        """Method for adding target to backupList"""
        pass

    def do_rm(self, args):
        """Method for removing target from backupList"""
        pass

    def do_EOF(self, arg):
        print()
        exit(0)


if __name__ == "__main__":
    UserLoop().cmdloop()
