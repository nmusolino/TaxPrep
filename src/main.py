#!/opt/bin/python3

import argparse
import sys

import input
import base

def main():
    """ Test of ability to read OpenTax data files. """

    argparser = argparse.ArgumentParser(description="Data file parser test.")
    argparser.add_argument("filename", type=str, help="Data file to be read.")
    args = argparser.parse_args()

    dictionary = input.parse_input(args.filename)
    print(dictionary)

def print_license()
    print("""
TaxPrep  Copyright (C) 2013  Nicholas Musolino
This program comes with ABSOLUTELY NO WARRANTY; for details see
the GNU General Public License under which it is released.
This is free software, and you are welcome to redistribute it
under certain conditions.""")    
        
if __name__ == '__main__':
    print_license()
    main()
