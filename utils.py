#!/usr/bin/python
import string

import subprocess

class Utils:
    def __init__(self):
        self.go()

    def go(self):
        call = subprocess.Popen(['git', 'fetch', '--tags', '--verbose'], 
                stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

        out, err = call.communicate()

        found = string.find(out, "[new tag]")

        if found == -1:
            print "not found"


foo = Utils()

