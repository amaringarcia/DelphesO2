#! /usr/bin/env python3

"""
Common header for AOD python scripts
"""

import argparse
import multiprocessing
import sys
try:
    import tqdm
except ImportError as e:
    print("Module tqdm is not imported. Progress bar will not be available (you can install tqdm for the progress bar)")


# Global running flags
verbose_mode = False


def set_verbose_mode(parser):
    global verbose_mode
    verbose_mode = parser.verbose


def get_default_parser(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--verbose", "-v",
                        action="store_true", help="Verbose mode.")
    parser.add_argument("--njobs", "-j", type=int,
                        default=10,
                        help="Number of concurrent jobs, by default 10.")
    return parser


class bcolors:
    # Colors for bash
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    BOKBLUE = BOLD + OKBLUE
    OKGREEN = "\033[92m"
    BOKGREEN = BOLD + OKGREEN
    WARNING = "\033[93m"
    BWARNING = BOLD + WARNING
    FAIL = "\033[91m"
    BFAIL = BOLD + FAIL
    ENDC = "\033[0m"


def verbose_msg(*args, color=bcolors.OKBLUE):
    if verbose_mode:
        print("** ", color, *args, bcolors.ENDC)


def msg(*args, color=bcolors.BOKBLUE):
    print(color, *args, bcolors.ENDC)


def fatal_msg(*args, fatal_message="Fatal Error!"):
    msg("[FATAL]", *args, color=bcolors.BFAIL)
    raise RuntimeError(fatal_message)


def warning_msg(*args):
    msg("[WARNING]", *args, color=bcolors.BWARNING)


def run_in_parallel(processes, job_runner, job_arguments, job_message):
    """
    In parallel processer of functions with a nice progress printing
    """
    with multiprocessing.Pool(processes=processes) as pool:
        msg(job_message)
        if "tqdm" not in sys.modules:
            for i in enumerate(pool.imap(job_runner, job_arguments)):
                msg(f"Done: {i[0]+1},", len(job_arguments)-i[0]-1, "to go")
        else:
            r = list(tqdm.tqdm(pool.imap(job_runner, job_arguments),
                               total=len(job_arguments),
                               bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'))