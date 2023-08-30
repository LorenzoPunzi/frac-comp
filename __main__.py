#!/usr/bin/env python
# Copyright (C) 2023 - Lorenzo Punzi (lorenzo.punzi@sns.it),
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
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

"""
import traceback
import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from utils.inout import frextract, reswrite
from utils.residuals import makeresids, fitconst
from utils.exceptions import FileFormatError




print(" ----------------------------------------------- ")
print("|  Welcome to the Fraction Comparison program!  |")
print("|                                               |")
print("|  Author: Lorenzo Punzi                        |")
print("|  Release: 1.0  -  September 2023              |")
print(" ----------------------------------------------- ")



parser = argparse.ArgumentParser(prog='frac-comp',
                                 description='Program used to compare fractions in two column files, calculate their differences and errors, fit the differences with a constant and plot the results. ',
                                 epilog='See subparser\'s help or README.md for more options and informations')


# ~~~~~~~~ Generic arguments for the main parser ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

parser.add_argument('variable', nargs='?', default='pi',
                    help="Whether the comparison is done as a function of QQpipi ('pi') or QQmumu ('mu')",
                    choices=('pi','mu'))

parser.add_argument('-sbrg', '--subrange', nargs=2, default=[0.32,0.96], metavar=('MIN_QQ','MAX_QQ'),
                    help='Subrange of Q^2 on which the analysis should be performed. Left and right ends of the range should be indicated (first number not greater than second) and must be within the total default range 0.32-0.96 GeV^2')
 
parser.add_argument('-svfg','--savefig', metavar='SAVEFIG_DIRECTORY', nargs='?', const=os.getcwd(),
                    help='Save the fraction plots generated by the program. Argument specifies the directory in which to save the figures')

parser.add_argument('-svdr', '--savedir', metavar='SAVE_DIRECTORY', default=os.getcwd(),
                    help='Specifies the directory in which to save the .dat file with residuals and their errors.')

parser.add_argument('-fit', action='store_true',
                    help='Fits the residuals of each channel with a constant and prints the chi squared to command line')

parser.add_argument('-fig','--figure', action='store_true',
                    help='Show plots comparing the fractions of file 1 (blue) and file 2 (red) as a function of Q^2. The figures also show the residuals as a function of Q^2.')

# Mutually exclusive group of options for locating the input column files

optgroup = parser.add_mutually_exclusive_group(required=True)

optgroup.add_argument('-infiles', nargs=2, metavar=('FILEPATH_1','FILEPATH_2'),
                      help='List the two paths to the input column files')

optgroup.add_argument('-search', metavar='SEARCH_DIRECTORY', nargs='?', const=os.getcwd(),
                        help='Activates search mode: lists txt and dat files in the given directory. When this option is specified without any argument given it defaults to the current working directory')


# Parse from command line
args = parser.parse_args()

#respath = os.path.join(os.getcwd(), args.resdir)
if args.infiles is not None:
    filepath1 , filepath2 = args.infiles

if args.search is not None:
    searchdir =  args.search
    files = [name for name in os.listdir(searchdir) if ('.txt' in name or '.dat' in name)]
    for i in range(len(files)):
        files[i] = f'{i+1}) '+ files[i]
    if len(files) == 0:
        print("\nError: given search directory contains no files with '.txt' or '.dat' extensions!\n")
        sys.exit(0)
    print(*files, sep = '\n')
    cond = True

    while cond:
        resp = input("\nChoose the first fraction file to use by entering the relative number, or enter 'q' or 'quit' to exit the program: ")
        if resp in ('q','quit'):
            print("\nExiting the program...\n")
            sys.exit(0)
        try:
            if int(resp)-1 in range(len(files)):
                filename1 = files[int(resp)-1][3:]
                print(f"\nYou chose {filename1} as the first file")
                cond = False
            else:
                print("\nError: the input number is out of range! Choose again...")
        except ValueError:
            print("\nError: the input is not a number! Choose again...")
    cond = True
    while cond:
        resp = input("\nChoose the second fraction file to use by entering the relative number, or enter 'q' or 'quit' to exit the program: ")
        if resp in ('q','quit'):
            print("\nExiting the program...\n")
            sys.exit(0)
        try:
            if int(resp)-1 in range(len(files)):
                filename2 = files[int(resp)-1][3:]
                print(f"\nYou chose {filename2} as the first file")
                cond = False
            else:
                print("\nError: the input number is out of range! Choose again...")
        except ValueError:
            print("\nError: the input is not a number! Choose again...")
    

    filepath1 , filepath2 = os.path.join(searchdir, filename1) , os.path.join(searchdir, filename2)

var = args.variable

try:
    if float(args.subrange[0]) < 0.32 or float(args.subrange[1]) > 0.96 or float(args.subrange[0]) > float(args.subrange[1]):
        cond = True
        print("\nError: the chosen subrange is either wrongly formatted (first number grater than second) or outside of the default range 0.32-0.96 GeV^2.\n")
        while cond:
            resp = input("Please input the left and right endpoints of the subrange again, separated by a space:")
            endpoints = resp.split()
            try:
                if len(endpoints) == 2 and 0.32 <= float(endpoints[0]) <= float(endpoints[1]) <= 0.96:
                    print(f"\nYou chose the range [{endpoints[0]},{endpoints[1]}] GeV^2")
                    cond = False
                else:
                    print("\nError: the input does not consist in two valid numbers within the range! Choose again...")
            except ValueError:
                print("\nError: the input are not numbers! Choose again...")
        args.subrange = endpoints
except ValueError:
    print("\nError: the input for Q^2 subrange are not numbers!\n")
    sys.exit(0)

print(f"\nProcessing files {filepath1} and {filepath2}, in variable {'QQ'+var+var} and range [{args.subrange[0]},{args.subrange[1]}]...\n")

try:
    fracts1 , fracts2 = frextract(filepath1,var,args.subrange) , frextract(filepath2,var,args.subrange)
except FileFormatError as err:
    print(type(err).__name__, ":", err,"\n")
    sys.exit(0)

if fracts1.shape != fracts2.shape:
    print(f"\nError: the input files have different numbers of rows/columns in {'QQ'+var+var}!\n")
    sys.exit(0)  

if not (fracts1[:,0] == fracts2[:,0]).all():
    print(f"\nError: the input files have different binning in {'QQ'+var+var}!\n")
    sys.exit(0)

resids , dresids = makeresids(fracts1,fracts2)

ressavedir = os.path.join(args.savedir,'residuals.dat')
reswrite(fracts1, resids, dresids, filepath1, filepath2, var, ressavedir)

filename1 = filepath1.split('/')[-1]
filename2 = filepath2.split('/')[-1]

if args.fit:
    q, dq, chisq = fitconst(resids , dresids)
    print("****************************** FIT RESULTS ******************************\n")
    print(f"PPG channel : q = {q[0]:.3} +- {dq[0]:.3}  ,  chisq/ndof = {chisq[0]:.3} / {dresids.shape[0]}")
    print(f"MMG channel : q = {q[1]:.3} +- {dq[1]:.3}  ,  chisq/ndof = {chisq[1]:.3} / {dresids.shape[0]}")
    print(f"EEG channel : q = {q[2]:.3} +- {dq[2]:.3}  ,  chisq/ndof = {chisq[2]:.3} / {dresids.shape[0]}")
    print(f"PPP channel : q = {q[3]:.3} +- {dq[3]:.3}  ,  chisq/ndof = {chisq[3]:.3} / {dresids.shape[0]}")
    print("*************************************************************************\n")

if args.figure:
    titles = ['ppg','mmg','eeg','ppp']
    names = ['ppg_fractions.pdf','mmg_fractions.pdf','eeg_fractions.pdf','ppp_fractions.pdf']
    for i in range(1):
        plt.figure(i)
        currfigure = plt.gcf()
        currfigure.set_size_inches(13, 7)
        plt.subplot(211)
        plt.grid(axis = 'both', linestyle = '--', alpha = 0.4)
        plt.ylabel('Fraction')
        ax = plt.gca()
        ax.xaxis.set_tick_params(labelbottom=False)
        plt.title(f"{titles[i]} fractions as a function of {'QQ'+var+var}")
        plt.errorbar(fracts1[:,0], fracts1[:,1+2*i], yerr=fracts1[:,2+2*i], ecolor='b', capsize = 2, linestyle='', label=filename1)
        plt.errorbar(fracts1[:,0], fracts2[:,1+2*i], yerr=fracts2[:,2+2*i], ecolor='r', capsize = 2, linestyle='', label=filename2)
        plt.legend()

        plt.subplot(212)
        plt.grid(axis = 'both', linestyle = '--', alpha = 0.4)
        plt.xlabel(f'QQ'+var+var+' [GeV^2]')
        plt.ylabel('Residuals')
        plt.axhline(linestyle = '--', color = 'k', linewidth = 1, label = 'zero')
        plt.title(f"{titles[i]} residuals as a function of {'QQ'+var+var}")
        plt.errorbar(fracts1[:,0], resids[:,i], yerr=dresids[:,i], ecolor='g', capsize = 2, linestyle='')
        if args.fit:
            #plt.fill_between(x=time_x, y1=upper_th, y2=lower_th, color='red',  interpolate=True, alpha=.75)
            plt.axhline(y = q[i], linestyle = '-', linewidth = 1, color = 'r',label = f'Best fit: {q[i]:.2} +- {dq[i]:.2}')
            #plt.axhline(y = q[i]+dq[i], linestyle = '-', linewidth = 0.5, color = 'r')
            #plt.axhline(y = q[i]-dq[i], linestyle = '-', linewidth = 0.5, color = 'r')
        plt.legend()
        if args.savefig is not None:
            plt.savefig(os.path.join(args.savefig,names[i]), format = 'pdf')


        
plt.show()
