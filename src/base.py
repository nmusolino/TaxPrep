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

import datetime
TAX_YEAR = 2012

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

Status = enum('single',
              'marriedFilingJointly',
              'marriedFilingSeparately',
              'headOfHousehold',
              'widow')

class Person(object):
    def __init__(name, date, ssn=None, blind=False):
        self.name = name
        self.blind = blind
        if isinstance(value, date):
            self.date_of_birth = date_of_birth
        else:
            raise TypeError("Python date class needed for date of birth.")

    @property
    def over_sixtyfive(self):
        return (date_of_birth < date(TAX_YEAR+1-64, 1, 2))


class Taxpayer(Person):
    def __init__(name="", status=Status.single, dependents=0,
                 date_of_birth=None, ssn=None, blind=False, spouse=None):
        self.name = name
        self.blind = blind
        if isinstance(value, date):
            self.date_of_birth = date_of_birth
        else:
            raise TypeError("Python date class needed for date of birth.")

        if (isinstance(spouse, Person)):
            self.spouse = spouse
        else:
            raise TypeError("Person class needed for spouse.")

    @property
    def special_deductions(self):
        """ Number of boxes taxpayer would check on US 1040 line 39a. """
        number_deductions = 0
        if self.blind:
            number_deductions += 1
        if self.over_sixtyfive:
            number_deductions += 1
        if self.spouse:
            if self.spouse.blind:
                number_deductions += 1
            if self.spouse.over_sixtyfive:
                number_deductions += 1
        return number_deductions
            
