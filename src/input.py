# TaxPrep: tax computation and form preparation software
# Copyright (C) 2013  Nicholas Musolino
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import sys
import logging as log
import shlex
import string
import re
import datetime
from decimal import Decimal
from base import Status, TAX_YEAR

log.basicConfig(stream=sys.stdout, level=log.INFO)

class InputError(Exception):
    pass
    
    
def parse_input(inputfile):
    """
    Return a dictionary representing the entries in inputfile.

    Parameter inputfile can be either a (string) filename or a file object.

    The format of the input file matches that in OpenTaxSolver version 9.
    """
    if isinstance(inputfile, str):
        inputdata = open(inputfile, "r").read()
    elif isinstance(inputfile, file):
        inputdata = inputfile

    for line in inputdata:
        if re.match("^[Tt]itle", line):
            continue
        else:
            break
            
    lex = shlex.shlex(inputdata, posix=True)
    lex.quotes = "\""
    lex.wordchars += '-' + '.' + "/" + "?" 

    taxpayer_dict = get_personal_data(lex)
    tax_data = get_tax_data(lex)
    print(taxpayer_dict)
    print(tax_data)
    return (taxpayer_dict, tax_data)


def get_personal_data(parser):
    """
    Returns a dict corresponding to the constructor parameters of Taxpayer:
      (name, date_of_birth=date.today(), ssn=None, blind=False, spouse=None)

     """
    log.debug("Getting personal data from input file.")
    re.DEBUG = True
    taxdata_pattern = re.compile('^[LDA][' + string.digits + ']+')
    log.debug("Searching for tax data with {0}"
              .format(taxdata_pattern.pattern))
        
    # Dict we will return, with default value of None for all entries.
    persondata = dict.fromkeys(['name',
                                'status',
                                'dependents',
                                'date_of_birth',
                                'ssn',                               
                                'blind'],
                                 None)
    age_category_pattern = re.compile('Under65', re.IGNORECASE)
    semicolon_pattern  = re.compile(r'^;');
    field_pattern = dict()
    for key in persondata:
        field_pattern[key] = re.compile(key, re.IGNORECASE)

    for token in comment_filter(parser):
        log.debug("Examining token {0}".format(token))
        if re.match(taxdata_pattern, token):
            ## If we have reached tax data, return
            log.debug("Matched against key for tax data.".format(key))

            parser.push_token(token)
            return persondata
        elif re.match(semicolon_pattern, token):
            pass
        elif re.match(age_category_pattern, token):
            log.debug("Matched against key age category".format(key))
            token = parser.get_token()
            if re.match("^Y", token, re.IGNORECASE):
                persondata['date_of_birth'] = datetime.date(TAX_YEAR - 65, 1, 1)
            elif re.match("^N", token, re.IGNORECASE):
                persondata['date_of_birth'] = datetime.date(TAX_YEAR, 12, 31)
            else:
                raise InputError("Unknown answer for Under65? variable [YES or NO]")
        else:
            for key in field_pattern:
                if re.match(field_pattern[key], token):
                    token = parser.get_token()
                    log.debug("Matched against key {0}".format(key))
                    if key == 'status':
                        persondata[key] = status(token)                        
                    else:
                        persondata[key] = token
                    break
            
        
    
def get_tax_data(parser):
    formvalues = dict()
    for name, value in name_value_extractor(comment_filter(parser)):
        formvalues[name] = value;

    return formvalues

        
def name_value_extractor(token_generator):
    """
    Generator to extract a name and value from input.

    Yields tuples of the form  (name, value).
    
    Input format should be of form:
        name value1 [value2 value3 ...];
    terminating with semicolon.  If multiple values are present, they are
    summed.  For the special case where "name" begins with "CapGains" (case-
    insensitive), the values extracted are 2-tuples containing a numeric value
    representing the gain, and a length of time (in days).  In the future, a 3-tuple may
    contain the gain, the length of time, and a comment.

    """
    field_name = re.compile(r'^[' + string.ascii_letters + r']')
    capgain_name = re.compile(r'cap-?gain', re.IGNORECASE)
    semicolon  = re.compile(r'^;');
    name = None
    value = Decimal(0.0)
    cap_gains_capture = False
    for token in token_generator:
        if re.match(capgain_name, token):
            log.debug("Interpreted token {0} as special cap gain field name.".format(token))
            cap_gains_capture = True
            name = token
            value = list()
        elif re.match(field_name, token):
            name = token
        elif re.match(semicolon, token):
            yield (name, value)
            if (cap_gains_capture):
                cap_gains_capture = False
            name = None
            value = Decimal(0.0)
        else:
            if (not cap_gains_capture):
                # TODO: make sure to convert string to clean number
                value += Decimal(token)
            else:
                ## Read tokens in following order:  purchase price, purchase date,
                ## 					sale price, sale date
                ## by advancing through token_generator's values
                buy_price = Decimal(token)
                buy_date = date(token_generator.__next__())
                sell_price = Decimal(token_generator.__next__())
                sell_date = date(token_generator.__next__())
                if (buy_price < 0):    # Purchase prices should be negative(cost).
                    buy_price *= -1
                if (buy_date > sell_date):
                    raise InputError(
                        "Sell date {0} occurs after buy date {1}"
                        .format(sell_date, buy_date)) 
                ## Push back a tuple of form  ( gain, days ) into the list
                value.append( (sell_price + buy_price,
                               (sell_date - buy_date).days) )


    
def comment_filter(lex):       
    """
    Generator to read meaningful (i.e. non-comment) tokens from lexical
    analyzer lex.  Yields tokens outside of comments characters.

    Raises exception InputError if a comment close character
    '}' is encountered outside of a comment.
    """
    COMMENT_OPEN_CHAR = "{"
    COMMENT_CLOSE_CHAR = "}"
    in_comment = False

    token = lex.get_token();
    while (token != lex.eof):
        if in_comment:
            if token == COMMENT_CLOSE_CHAR:
                in_comment = False
        else:
            if token == COMMENT_OPEN_CHAR:
                in_comment = True
            elif token == COMMENT_CLOSE_CHAR:
                raise InputError(
                    "Comment-closing char {0} found outside comment".format(token))
            else:
                yield token

        token = lex.get_token()

    return


def date(datestring):
    """ Read a string with format MM-DD-[YY]YY and return a date object. """
    date_list = datestring.split("-")
    if (len(date_list) != 3):
        raise InputError("Bad date read: {0}.".format(datestring))        
    month = int(date_list[0]);
    day = int(date_list[1]);
    year = int(date_list[2]);
    if (0 < year < 31):
        year += 2000;
    elif (year <= 99):
        year += 1900
    return datetime.date(year, month, day)


def status(status_string):
    status_pattern = {Status.single: "^sing",
                      Status.marriedFilingJointly: "^Mar.*Joint",
                      Status.marriedFilingSeparately: "^Mar.*Sep",
                      Status.headOfHousehold: "^Head.*House",
                      Status.widow: "^wid"}
    for status in status_pattern:
        if re.match(status_pattern[status], status_string):
            return status

    # Did not match any known status.
    raise InputError("String {0} did not match any known status."
                     .format(status_string))
