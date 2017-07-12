#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from subprocess import check_output, STDOUT, CalledProcessError


def exec_bin(exe_file, exe_args):
    """
    Run an executable file with args.
    """

    result = ""
    return_code = 0

    print('\nExecuting :' + exe_file + " " + " ".join(exe_args))

    try:
        result = check_output(
            [exe_file] + exe_args,
            stderr=STDOUT,
            universal_newlines=True)
    except CalledProcessError as err:
        # ignoring this error since some process seems to have
        # non 0 return code even when everything went ok
        return_code = err.returncode

    return (result, return_code)
