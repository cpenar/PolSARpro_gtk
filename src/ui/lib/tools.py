#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def exec_bin(exe_file, exe_args, async=False, callback=None):
    """
    Can launch an exucutable file with args.
    Can be async, then should specify a callback (and a progress bar ?)
    """

    from subprocess import check_output, STDOUT, CalledProcessError

    result = ""
    return_code = 0

    if async and not callable(callback):
        msg = 'A callback FUNCTION should be given for async calls'
        print('ERROR: ' + msg)
        raise TypeError(msg)

    cmd_line = exe_file
    for args_duo in exe_args:
        cmd_line += " " + " ".join(args_duo)

    if async:
        # TODO: to be written
        pass
    else:
        try:
            result = check_output(
                cmd_line,
                shell=True,
                stderr=STDOUT,
                universal_newlines=True)
        except CalledProcessError as err:
            # ignoring this error since some process seems to have
            # non 0 return code even when everything went ok
            return_code = err.returncode

        return (result, return_code)
