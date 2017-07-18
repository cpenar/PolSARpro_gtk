#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from subprocess import Popen, PIPE
from threading import Thread
from time import sleep


class Async_exec:
    def __init__(self, exe_file, exe_args, callback, builder):
        """
        Callback signature :
            The new created process as argument
        """

        self.builder = builder
        self.process_queue = []
        self.add(exe_file, exe_args, callback)

    def add(self, exe_file, exe_args, callback):
        print('process stacking: ' + exe_file)
        self.process_queue.append([exe_file, exe_args, callback])

    def run(self):
        # manage the process queue in a non blocking subthread

        def run_processes():
            self.builder.get_object('menubar1').set_sensitive(False)
            for p in self.process_queue:
                exe_file, exe_args, callback = p

                print('\n#### STARTING: ')
                print(exe_file)
                print('#### with arguments:')
                print(exe_args)

                self.process = Popen(
                    [exe_file] + exe_args,
                    universal_newlines=True,
                    stderr=PIPE,
                    stdout=PIPE)

                # A thread for the user callback
                thread = Thread(target=callback, args=(self.process,))
                thread.daemon = True
                thread.start()

                # non blocking wait for the main thread as we allready are
                # in a subthread
                self.process.wait()
                sleep(0.2)
                print('FINISHED : ' + exe_file)

            self.builder.get_object('menubar1').set_sensitive(True)



        thread = Thread(target=run_processes)
        thread.daemon = True
        thread.start()
