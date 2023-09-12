#!/bin/python3
'''These are the custom built testing tools. Having them in a seperate file
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

import pytest  # pylint: disable=unused-import

TESTS: PosixPath = PosixPath(__file__).joinpath('../').resolve()
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
            _test_file = int_to_filepath(args[1])
            system(f'{MAIN} {TESTS}/tests/{_test_file} > {DATA}/perm/{_test_file[:-3]}.txt')
            print(f'Created new sample output for {_test_file} .')

    if tot == 3:
        if mode == '-n':         # Make a new test based on the template.
            num = args[2]
            test_name = int_to_filepath(num)
            _test_file = f'{TESTS}/tests/_{test_name}'
            test_file = f'{TESTS}/tests/{test_name}'
            if not isfile(_test_file) and not isfile(test_file):
                system(f'cp {TESTS}/template.py {_test_file}')
                system(f"sed -i 's/test_number/{num}/g' {_test_file}")
                print(f'Created {test_name} from template.py')

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


def pytest_runner(num: str) -> None:
    '''This function runs a icebrakes.py lint on the given input file,
    and sends the given output to a tmp file. A test should never be written
    with an invalid input file because the test_###.py files are 
    the test input themselves.'''
    test_file = int_to_filepath(str(num))
    filename: str = test_file[:-3]    # the -3 removes ".py" from the filename
    system(f'{MAIN} {TESTS}/tests/{test_file} > {DATA}/tmp/{filename}.txt')
    assert isfile(f'{DATA}/perm/{filename}.txt')
    assert isfile(f'{DATA}/tmp/{filename}.txt')
    #assert filecmp(f'{DATA}/perm/{filename}.txt', f'{DATA}/tmp/{filename}.txt')


def gen_output_for_all_test_0()-> None:
    '''Output data will be generated for every test with a number
    starting with zero (test_0###.py) . This could overwrite valid data with
    invalid data so make sure to only use this function when
    every test is passing!'''
    time_in_mins = strftime("%Y%m%d-%H%M")
    backup_dir = f'{DATA}/relegated/{time_in_mins}'
    system(f'cp -r {DATA}/perm/ {backup_dir}')
    system(f'rm -r {DATA}/perm/ && mkdir {DATA}/perm')

    for file in listdir(f'{TESTS}/tests'):
        if file[0:6] == 'test_0' and '_999.py' not in file:
            system(f'{MAIN} {TESTS}/tests/{file} > {DATA}/perm/{file[:-3]}.txt')
    print('Created new sample outputs for every test and backups put in relegated.')


if __name__ == "__main__":
    parse_argv(argv)


#Copyright © 2023 Lars S.
