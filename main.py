#!/opt/bin/python3

import argparse
import sys

import taxbase

def test_input():
    """ Test of ability to read OpenTax data files. """

    argparser = argparse.ArgumentParser(description="Data file parser test.")
    argparser.add_argument("filename", type=str, help="Data file to be read.")
    programArgs = argparser.parse_args()

    dictionary = taxbase.InputParser.parse_input(programArgs.filename)
    print(dictionary)


def test_output():
    """ Test of ability to write FDF files for later completion of PDF forms. """
    

def main():
    test_input()


def print_license():
    print("""
TaxPrep  Copyright (C) 2013  Nicholas Musolino
This program comes with ABSOLUTELY NO WARRANTY; for details see
the GNU General Public License under which it is released.
This is free software, and you are welcome to redistribute it
under certain conditions.""")    
        

if __name__ == '__main__':
    print_license()
    main()
