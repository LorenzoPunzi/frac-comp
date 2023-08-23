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

import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from utils.inout import frextract, reswrite
from utils.residuals import makeresids, fitconst




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

# !!! check that they are in range and otherwise ask again
parser.add_argument('-sbrng', '--subrange', nargs=2, default=[0.32,0.96], metavar=('MIN_QQ','MAX_QQ'),
                    help='Subrange of Q^2 on which the analysis should be performed. Left and right ends of the range should be indicated and must be within the total default range 0.32-0.96 GeV^2')

# !!! Needs work on defaults considering the directory system implemented in cmepda 
parser.add_argument('-savefig', default='.', metavar='SAVEFIG_DIRECTORY',
                    help='Save the fraction plots generated by the program. Argument specifies the directory in which to save the figures')
# !!! Needs work on defaults considering the directory system implemented in cmepda
parser.add_argument('-svdir', '--savedir', default='.', metavar='SAVE_DIRECTORY',
                    help='Specifies the directory in which to save the .dat file with residuals and their errors.')

parser.add_argument('-fit', action='store_true',
                    help='Fits the residuals of each channel with a constant and prints the chi squared to command line')

parser.add_argument('-test', metavar='SEARCH_DIRECTORY',
                        help='Activates search mode: lists txt and dat files in the given directory')

# Add mutually exclusive group of options for locating the input column files

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

    # Need to solve problem when inputing non integer string in search mode !!!

    while cond:
        resp = input("\nChoose the first fraction file to use by entering the relative number, or enter 'q' or 'quit' to exit the program: ")
        if resp in ('q','quit'):
            print("\nExiting the program...\n")
            sys.exit(0)
        if int(resp)-1 in range(len(files)):
            filename1 = files[int(resp)-1][3:]
            print(f"\nYou chose {filename1} as the first file")
            cond = False
        else:
            print("\nError: the input number is out of range! Choose again...")
    cond = True
    while cond:
        resp = input("\nChoose the second fraction file to use by entering the relative number, or enter 'q' or 'quit' to exit the program: ")
        if resp in ('q','quit'):
            print("\nExiting the program...\n")
            sys.exit(0)
        if int(resp)-1 in range(len(files)):
            filename2 = files[int(resp)-1][3:]
            print(f"\nYou chose {filename2} as the second file")
            cond = False
        else:
            print("\nError: the input number is out of range! Choose again...")
    
    if not searchdir.endswith('/'):
        searchdir = searchdir + '/'

    filepath1 , filepath2 = searchdir + filename1 , searchdir + filename2
    


print(f"\nProcessing files {filepath1} and {filepath2}...")
var = args.variable
    
fracts1 , fracts2 = frextract(filepath1,var,args.subrange) , frextract(filepath2,var,args.subrange)

# Needs to be tested !!!
if not (fracts1[:,0] == fracts2[:,0]).all():
    print(f"\nError: the input files have different binning in {'QQ'+var+var}!")
    sys.exit(0)

resids , dresids = makeresids(fracts1,fracts2)

reswrite(fracts1, resids, dresids, filepath1, filepath2, var)

if args.fit is not None:
    q, dq, chisq = fitconst(resids , dresids)
    print("\n****************************** FIT RESULTS ******************************\n")
    print(f"PPG channel : q = {q[0]:.3} +- {dq[0]:.3}  ,  chisq/ndof = {chisq[0]:.3} / {dresids.shape[0]}")
    print(f"MMG channel : q = {q[1]:.3} +- {dq[1]:.3}  ,  chisq/ndof = {chisq[1]:.3} / {dresids.shape[0]}")
    print(f"EEG channel : q = {q[2]:.3} +- {dq[2]:.3}  ,  chisq/ndof = {chisq[2]:.3} / {dresids.shape[0]}")
    print(f"PPP channel : q = {q[3]:.3} +- {dq[3]:.3}  ,  chisq/ndof = {chisq[3]:.3} / {dresids.shape[0]}")
    print("*************************************************************************\n")


'''

if args.cornerplot is True:
    if args.variables == default_vars():
        overlaid_cornerplot(vars=args.variables[:5], figpath=respath)
        overlaid_cornerplot(vars=args.variables[7:], figpath=respath)
        overlaid_cornerplot(
            vars=('M0_p',)+args.variables[7:9], figpath=respath)
    elif len(args.variables) >= 6:
        msg = "***WARNING*** \nNumber of variables to print in the corner plot \
exceeds the maximum suggested (5). Running the \'cornerplot\' function on \
groups of five contiguous variables in the list\n*************\n"
        warnings.warn(msg, stacklevel=2)
        ind = 0
        while ind+5 <= len(args.variables):
            overlaid_cornerplot(
                vars=args.variables[ind:ind+4], figpath=respath)
            ind += 5
        overlaid_cornerplot(vars=args.variables[ind:], figpath=respath)
    else:
        overlaid_cornerplot(vars=args.variables, figpath=respath)


# Starts the analysis on the selected methods
if hasattr(args, "methods"):
    fractions_list = []
    SINGULAR_ROCS = True

    # If args.var_cut contains a single element (type str), it is
    # changed into a list
    vcuts = [args.var_cut] if type(
        args.var_cut) is str else args.var_cut
    if type(args.vcut_inverse) is int:
        inverse_vcut = [bool(args.vcut_inverse)]
    else:
        inverse_vcut = [bool(inv) for inv in args.vcut_inverse]

    # Initialize a list with the  requested methods of analysis (removing
    # duplicates if present.
    if 'all' in args.methods:
        analysis = ['all']
        SINGULAR_ROCS = False
    else:
        analysis = []
        [analysis.append(item) for item in args.methods
            if item not in analysis]
        roc_analysis = ["dnn", "dtc", "vcut"]
        flag = len([a for a in analysis if a in roc_analysis])
        if flag >= 2 or len(vcuts) > 1:
            SINGULAR_ROCS = False

    # Initializing lists if multiple rocs are plotted together
    if SINGULAR_ROCS is not True:
        rocx_array, rocy_array = [], []
        roc_labels, roc_linestyles, roc_colors = [], [], []
        x_pnts, y_pnts, point_labels = [], [], []

    # Running the selected analyses
    for opt in analysis:

        if opt in ["vcut", "all"]:
            # ~~~~~~~~ Setup of the var_cut - free to edit ~~~~~~~~~~~~~~~~~~~
            SPECIFICITY = False
            figure_cut = args.figures
            figure_roc = bool(args.figures*SINGULAR_ROCS)
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            method_title = 'Cut on Variables Distribution'
            with open(results_file, encoding='utf-8', mode='a') as file_vcut:
                file_vcut.write(f'\n\n  {method_title}: \n')
            print(f'\n  {method_title} - working...\n')

            rocx_vcut, rocy_vcut, labels_vcut = [], [], []

            vars = zip(vcuts, inverse_vcut)

            # Performs the analysis on every specified variable in args.var_cut
            for vc in vars:
                fr, stats, eval_arr = var_cut(
                    rootpaths=filepaths, tree=tree, cut_var=vc[0],
                    eff=args.efficiency, error_optimization=True,
                    inverse_mode=vc[1], specificity_mode=SPECIFICITY,
                    savefig=figure_cut, figpath=respath)

                fractions_list.append(fr)

                rocx, rocy, auc = roc(
                    eval_arr[0], eval_arr[1], eff=round(stats[0], 4), inverse_mode=vc[1],
                    makefig=figure_roc, name=f'{respath}/ROC_{vc[0]}_cut')

                if SINGULAR_ROCS is not True:
                    rocx_array.append(rocx)
                    rocy_array.append(rocy)
                    roc_labels.append(f'{vc[0]}_cut')
                    if args.err_opt is True:
                        x_pnts.append(stats[1])
                        y_pnts.append(stats[0])
                        point_labels.append(f'Optimized point {vc[0]}_cut')

                add_result(
                    "K fraction", f'{round(fr[0],4)} +- {round(fr[1],4)} (stat) +- {round(fr[2],4)} (syst)', vc[0])
                add_result("Efficiency", stats[0], vc[0])
                add_result("Misid", stats[1], vc[0])
                add_result("Cut", stats[2], vc[0])
                add_result("AUC", auc, vc[0])

            print(f"\n  {method_title} - ended successfully! \n\n")

        if opt in ["dnn", "all"]:
            # ~~~~~~~~ Setup of the DNN - free to edit ~~~~~~~~~~~~~~~~~~~~~~~
            LAYERS = (75, 60, 45, 30, 20)
            VALIDATION_FRACTION = 0.5
            BATCH_SIZE = 128
            EPOCHNUM = 600
            LEARNING_RATE = 1e-4
            DROPOUT = 0
            VERBOSE = 2
            MODEL_FILE = 'cmepda-PiKclassifier/machine_learning/deepnn.json'
            WEIGHTS_FILE = 'cmepda-PiKclassifier/machine_learning/deepnn.h5'
            figs = args.figures
            PLOT_ROC = bool(args.figures*SINGULAR_ROCS)
            fignames = ("DNN_history.png", "eval_Pions.png", "eval_Kaons.png",
                        "eval_Data.png")
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            method_title = 'Deep Neural Network'
            with open(results_file, encoding='utf-8', mode='a') as file_dnn:
                file_dnn.write(f'\n\n  {method_title}: \n')
            print(f'\n  {method_title} - working...\n')

            settings = DnnSettings(layers=LAYERS, val_fraction=VALIDATION_FRACTION,
                                   epochnum=EPOCHNUM, learning_rate=LEARNING_RATE,
                                   batch_size=BATCH_SIZE, dropout=DROPOUT, verbose=VERBOSE)

            fr, stats, eval_test = dnn(
                source=('root', filepaths), root_tree=tree,
                vars=args.variables, settings=settings, load=args.load_dnn,
                trained_filenames=(MODEL_FILE, WEIGHTS_FILE),
                efficiency=args.efficiency, error_optimization=args.err_opt,
                savefigs=figs, figpath=respath, fignames=fignames)

            fractions_list.append(fr)

            rocx_dnn, rocy_dnn, auc_dnn = roc(
                eval_test[0], eval_test[1], eff=stats[2],
                makefig=PLOT_ROC, name=f'{respath}/ROC_dnn')

            if SINGULAR_ROCS is not True:
                rocx_array.append(rocx_dnn)
                rocy_array.append(rocy_dnn)
                roc_labels.append("DNN")
                if args.err_opt is True:
                    x_pnts.append(stats[1])
                    y_pnts.append(stats[0])
                    point_labels.append(f'Optimized point DNN')

            add_result(
                "K fraction", f'{round(fr[0],4)} +- {round(fr[1],4)} (stat) +- {round(fr[2], 4)} (syst)')
            add_result("Efficiency", stats[0])
            add_result("Misid", stats[1])
            add_result("Cut", stats[2])
            add_result("AUC", auc_dnn)

            print(f"\n  {method_title} - ended successfully! \n\n")

        if opt in ["dtc", "all"]:
            # ~~~~~~~~ Setup of the DTC - free to edit ~~~~~~~~~~~~~~~~~~~~~~~
            TEST_SIZE = 0.3
            ML_SAMP = 1
            CRIT = 'gini'
            PRINTED_TREE_FILE = 'DTC_printed.txt'
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            method_title = 'Decision Tree Classifier'
            with open(results_file, encoding='utf-8', mode='a') as file_dtc:
                file_dtc.write(f'\n\n  {method_title}: \n')
            print(f'\n  {method_title} - working...\n')

            fr, stats = dt_classifier(
                root_tree=args.tree, vars=args.variables, test_size=TEST_SIZE,
                min_leaf_samp=ML_SAMP, crit=CRIT,
                print_tree=f'{respath}/{PRINTED_TREE_FILE}', figpath=respath)

            fractions_list.append(fr)

            if SINGULAR_ROCS is not True:
                x_pnts.append(stats[1])
                y_pnts.append(stats[0])
                point_labels.append("DTC")

            add_result(
                "K fraction", f'{round(fr[0],4)} +- {round(fr[1],4)} (stat) +- {round(fr[2], 4)} (syst)')
            add_result("Efficiency", stats[0])
            add_result("Misid", stats[1])

            print(f'\n  {method_title} - ended successfully! \n\n')

        if opt in ["tfit", "all"]:
            # ~~~~~~~~ Setup of the template fit - free to edit ~~~~~~~~~~~~~~
            NBINS_HISTO = 1000
            histo_lims = (5.0, 5.6)  # Limits of the histograms
            fit_range = (5.02, 5.42)  # Range where the templates are fitted
            p0_pi = (1e5, 0.16, 5.28, 0.08, 5.29, 0.04)
            p0_k = (1e5, 0.97, 1.6, 0.046, 5.30, 1.1, 5.27, 0.00045)
            figures = args.figures
            FIGNAME_TEMPL_PI = 'Template_fit_Pi.png'
            FIGNAME_TEMPL_K = 'Template_fit_K.png'
            FIGNAME_GLOBAL = 'Template_fit_Data.png'
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            method_title = 'Template fit with ROOT'
            with open(results_file, encoding='utf-8', mode='a') as file_tfit:
                file_tfit.write(f'\n\n  {method_title}: \n')
            print(f'\n {method_title} - working...\n')
            var = args.var_fit

            templ_pars_pi = fit_mc_template(
                filepaths[0], args.tree, var,
                DoubleGaussian(fit_range, pars=p0_pi),
                Nbins=NBINS_HISTO, histo_lims=histo_lims,
                histo_title=f'{var} distribution (B0->PiPi MC)',
                savefig=figures, img_name=f'{respath}/{FIGNAME_TEMPL_PI}')
            templ_pars_k = fit_mc_template(
                filepaths[1], args.tree, var,
                GaussJohnson(fit_range, pars=p0_k),
                Nbins=NBINS_HISTO, histo_lims=histo_lims,
                histo_title=f'{var} distribution (B0s->KK MC)',
                savefig=figures, img_name=f'{respath}/{FIGNAME_TEMPL_K}')

            res = global_fit(filepaths[2], args.tree, var, Nbins=NBINS_HISTO,
                             pars_mc1=templ_pars_k, pars_mc2=templ_pars_pi,
                             histo_lims=histo_lims, savefig=figures,
                             img_name=f'{respath}/{FIGNAME_GLOBAL}')

            fr = (res.Parameters()[1], res.Errors()[1], 0.002)
            fractions_list.append(fr)

            add_result(
                "K fraction", f'{res.Parameters()[1]} +- {res.Errors()[1]}')
            add_result("Chi2", res.Chi2())
            add_result("Probability", res.Prob())

            print(f'  {method_title} - ended successfully')

    # If there are two or more lines/points to draw in the misid-efficiency plot,
    # they are plotted in the same figure
    if SINGULAR_ROCS is not True:
        for i in range(len(roc_labels)):
            roc_colors.append('#%06X' % randint(0, 0xFFFFFF))
            roc_linestyles.append('-')

        # If error_optimization is enabled, the efficiency line is not shown;
        # instead are highlited the points on the roc curves corresponding to
        # the chosen working point
        if args.err_opt is True:
            roc_labels = [f'{lab} roc' for lab in roc_labels]
            plot_rocs(tuple(rocx_array), tuple(rocy_array), tuple(roc_labels),
                      tuple(roc_linestyles), tuple(roc_colors),
                      x_pnts=x_pnts, y_pnts=y_pnts, point_labels=point_labels,
                      eff=0, figtitle='ROCs', figname=f'{respath}/ROCs.png')
        else:
            plot_rocs(tuple(rocx_array), tuple(rocy_array), tuple(roc_labels),
                      tuple(roc_linestyles), tuple(roc_colors),
                      x_pnts=x_pnts, y_pnts=y_pnts, point_labels=point_labels,
                      eff=args.efficiency, figtitle='ROCs',
                      figname=f'{respath}/ROCs.png')

    # Plots the fraction estimations, with uncertainties, in a joint plot
    if args.figures is True:
        if 'all' in analysis:
            analysis = ['vcut', 'dnn', 'dtc', 'tfit']
        variables = [f'{vcut}_cut' for vcut in vcuts]
        analysis = variables + analysis[1:]
        npts = len(fractions_list)
        y = np.linspace(0.2, 0.8, npts)
        idx = 0
        fig = plt.figure("fractions")
        plt.title("K fraction estimates")
        plt.xlabel("Fraction")
        plt.ylim(0, 1)
        plt.yticks(y, analysis)
        plt.xlim(0.375, 0.475)

        for fr in fractions_list:

            lwdth_stat = 2 if fr[2] <= fr[1] else 3
            lwdth_syst = 2 if fr[1] <= fr[2] else 3

            plt.plot(fr[0], y[idx], color='black', marker='o')
            plt.errorbar(fr[0], y[idx], 0, fr[1], fmt='',
                         ecolor='blue', elinewidth=lwdth_stat)
            plt.errorbar(fr[0], y[idx], 0, fr[2], fmt='',
                         ecolor='green', elinewidth=lwdth_syst)
            idx += 1
        plt.plot([], [], marker='', linestyle='-',
                 color='blue', label="Stat. error bars")
        plt.plot([], [], marker='', linestyle='-',
                 color='green', label="Syst. error bars")
        plt.axvline(x=0.42, linestyle='--', color='red',
                    label='True K fraction')

        plt.draw()
        plt.legend()
        plt.savefig(f'{respath}/fractions.png')


print("END OF FILE")

'''