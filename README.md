TaxPrep
=======

Compute taxes and complete PDF tax forms.

Version 0.0.2
At this time, TaxPrep can parse OpenTaxSolver's input files.

TODO:
  * Add computations for US Form 1040  
  * Consolidate/organize files as a Python package 
  * Add facility to write output to JSON file for later addition 
     to PDF with fillable fields
  * Add additional forms: 1040A, which should be similar to 1040,
     and 1040 Schedule C.
  * Add graphical user interface using PyQt or PySide


Legal 
======
Copyright 2013, Nicholas Musolino

This program is distributed in the hope that it will be useful,	but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  

This software is designed to generate completed tax forms in PDF
format, based on a text file in a particular format supplied by the
user.  TaxPrep is written in Python 3, and is designed to work like
OpenTaxSolver, a tax computation package written in C
<http://http://opentaxsolver.sourceforge.net/>.

This software is free software released under the GNU General
License, version 3.
