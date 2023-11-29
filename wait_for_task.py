# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 10:32:26 2023

@author: rnv
"""
import time
import ray

def wait_for_tasks(sleep_time_init=10, sleep_time_loop=5):
    """
    Function to wait for all tasks in Ray graph to finish executing.

    See:
    https://stackoverflow.com/questions/54583710/standard-way-to-wait-for-all-tasks-to-finish-before-exiting

    Sleeps before the loop starts for a longer period of time than the loop
    sleeps itself to make sure all the tasks have been fully started by the
    schedulers. Otherwise, the loop exit condition might be met when processing
    is not actually finished.

    :param sleep_time_init: Time to sleep before beginning loop (secs).
    :param sleep_time_loop: Time to wait before checking for all task completion
        condition being met.
    """

    time.sleep(sleep_time_init)

    while (ray.cluster_resources() !=
           ray.available_resources()):

        time.sleep(sleep_time_loop)
