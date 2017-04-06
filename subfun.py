#!/usr/bin/env python

import mock
import re
import subprocess
import unittest

def do_proc():
    """execute some external commands."""
    call = subprocess.Popen(['ls'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    out, err = call.communicate()
            
    matched = re.search(r'foobar.txt', out, flags=re.MULTILINE)
    if matched is not None:
        try:
            call = subprocess.Popen(['cat', 'foobar.txt'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            out, err = call.communicate()
        except OSError as err:
            return False
                                                                                            
    return True

class TestDoProc(unittest.TestCase):
    @mock.patch('subprocess.Popen')
    def test_one(self, popen_mock):
        pmock = mock.Mock()
        pmock.communicate.return_value = ("foobar.txt", "")

        popen_mock.return_value = pmock

        calls = [ 
                mock.call(['ls'],  stderr=subprocess.STDOUT, stdout=subprocess.PIPE),
                mock.call(['cat', 'foobar.txt'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                ]

        do_proc()
        popen_mock.assert_has_calls(calls)

    @mock.patch('subprocess.Popen')
    def test_two(self, popen_mock):
        def proc_side_effect(*args, **kargs):
            proc_cmd = args[0]

            pmock = mock.Mock()
            if proc_cmd[0] == 'ls':
                pmock.communicate.return_value = ("foobar.txt", "")
            elif proc_cmd[0] == 'cat':
                pmock.communicate.return_value = ("go away", "")
            else:
                raise OSError

            return pmock

        popen_mock.configure_mock(side_effect=proc_side_effect)
        calls = [ 
                mock.call(['ls'],  stderr=subprocess.STDOUT, stdout=subprocess.PIPE),
                mock.call(['cat', 'foobar.txt'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
                ]

        do_proc()
        popen_mock.assert_has_calls(calls)

if __name__ == "__main__":
    unittest.main()
