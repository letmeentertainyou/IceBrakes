#!/bin/python3
'''These are the custom built testing tools. Having them in a separate file
allows for the actual tests files to have very little repeated code. See 
TESTING_README.txt for much more info about tools.py .


I HAVE CHOSEN TO HAVE THIS FILE INCLUDED IN THE COVERAGE REPORT
WHICH MEANS WE HAVE TO WRITE TESTS TO TEST THE TEST TOOLS.'''
from os import listdir, system
from os.path import isfile
from pathlib import PosixPath
from sys import argv
from time import strftime
from typing import List
from subprocess import run

import pytest  # pylint: disable=unused-import

TESTS: PosixPath = PosixPath(__file__).joinpath('../tests/').resolve()
DATA: PosixPath = PosixPath(__file__).joinpath('../data').resolve()
MAIN: PosixPath = PosixPath(TESTS).joinpath('../../icebrakes.py').resolve()


def parse_argv(args: List[str]) -> None:
    '''parses the command line inputs see DOCS/TESTING_README.txt for a full 
    write up of the available command line args.'''
    tot: int = len(args)
    if tot < 1 or tot > 4:
        print('tools.py only takes one or two args. Read the TESTING_README for me.')

    mode: str = args[1]
    if tot == 2:
        if mode == '-a':
            gen_output_for_all_test_0()
        else:
            test_file = int_to_filepath(args[1])
            if isfile(f'{TESTS}/_{test_file}'):
                system(f'mv {TESTS}/_{test_file} {TESTS}/{test_file} ')     ### NEW
                print(f'Enabled {test_file}')                               ### NEW
            system(f'{MAIN} {TESTS}/{test_file} > {DATA}/perm/{test_file[:-3]}.txt')
            print(f'Generated new sample output for {test_file} .')

    if tot == 3:
        if mode == '-n':         # Make a new test based on the template.
            num = args[2]
            test_name = int_to_filepath(num)
            _test_file = f'{TESTS}/_{test_name}'
            test_file = f'{TESTS}/{test_name}'
            if not isfile(_test_file) and not isfile(test_file):
                system(f'cp {TESTS}/../template.py {_test_file}')    # BUG FIX
                system(f"sed -i 's/test_number/{num}/g' {_test_file}")
                print(f'Created _{test_name} from template.py')

            else:
                print(f'{test_name} already exists, please delete it first.')

def cleanup() -> None:
    '''Removes all the txt files in src/tests/data/tmp '''
    system(f'rm {DATA}/tmp/*.txt')


def filecmp(path_1: str, path_2: str) -> bool:
    '''This is named after the python builtin filecmp.cmp but my 
    version only checks if the lines of the two files are the 
    same and not the metadata.'''
    with open(path_1, 'r', encoding = 'utf-8') as filehandler:
        file_1: List[str] = filehandler.readlines()
    with open(path_2, 'r', encoding = 'utf-8') as filehandler:
        file_2: List[str] = filehandler.readlines()
    if file_1 == file_2:
        return True
    return False


def int_to_filepath(num: str) -> str:
    '''This function takes a single int, and 
    converts it to "test_###.py", very useful.'''
    test_number: str = str(num).rjust(4, '0')
    test_file: str = f'test_{test_number}.py'
    return test_file


def pytest_runner(num: str, get_code: bool=False) -> int:
    '''This function runs a icebrakes.py lint on the given input file,
    and sends the given output to a tmp file. A test should never be written
    with an invalid input file because the test_###.py files are 
    the test input themselves.'''
    test_file = int_to_filepath(str(num))
    filename: str = test_file[:-3]    # the -3 removes ".py" from the filename

    # This branches because the dump to file gives exit code 0.
    # Also we don't need to write files for the exit_code test anyways.
    if get_code:
        # Apparently subprocess.run is the easiest way to get an exit code.
        proc = run([ MAIN, f'{TESTS}/{test_file}' ], check=False)
        return proc.returncode

    # subprocess.run is not able to handle this command
    # with either an array or string input. I don't feel
    # like spending a bunch more time debugging subprocess.run so os.system stays.
    system(f'{MAIN} {TESTS}/{test_file} > {DATA}/tmp/{filename}.txt')
    assert isfile(f'{DATA}/perm/{filename}.txt')
    assert isfile(f'{DATA}/tmp/{filename}.txt')
    assert filecmp(f'{DATA}/perm/{filename}.txt', f'{DATA}/tmp/{filename}.txt')

    return 9999     # This number won't conflict with the existing exit codes.

def gen_output_for_all_test_0()-> None:
    '''Output data will be generated for every test with a number
    starting with zero (test_0###.py) . This could overwrite valid data with
    invalid data so make sure to only use this function when
    every test is passing!'''
    time_in_mins = strftime("%Y%m%d-%H%M")
    backup_dir = f'{DATA}/relegated/{time_in_mins}'
    system(f'cp -r {DATA}/perm/ {backup_dir}')
    system(f'rm {DATA}/perm/test_0*.txt')

    for file in listdir(TESTS):
        if file[0:6] == 'test_0' and '_999.py' not in file:
            system(f'{MAIN} {TESTS}/{file} > {DATA}/perm/{file[:-3]}.txt')
    print('Created new sample outputs for every test and backups put in relegated.')


if __name__ == "__main__":
    parse_argv(argv)


#Copyright © 2023 Lars S.
